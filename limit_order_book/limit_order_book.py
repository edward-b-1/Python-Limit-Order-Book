#!/bin/python3

import math
import os
import random
import re
import sys
from functools import reduce

from limit_order_book.validate import *
from limit_order_book.order import Order
from limit_order_book.partial_order import PartialOrder
from limit_order_book.trade import Trade

from limit_order_book.limit_order_book_price_level import LimitOrderBookPriceLevel



'''
    Hashmap like operations:

    - insert
    - update (special operation) (can change price and volume)
    - delete
    - _get (for testing)
    - _find/_filter (for validation/logic consistency checking)

    - _find (is always by order_id)
    - _get (is always by order_id)

    Note: Changing price or volume causes order to lose priority, unless the only change
    is to decrease the volume.
'''

'''
 Run the matching engine for a list of input operations and returns the trades and orderbooks in a
 csv-like format. Every command starts with either "INSERT", "UPDATE" or "CANCEL" with additional
 data in the columns after the command.

 In case of insert the line will have the format:
 INSERT,<order_id>,<symbol>,<side>,<price>,<volume>
 e.g. INSERT,4,FFLY,BUY,23.45,12

 In case of update the line will have the format:
 UPDATE,<order_id>,<price>,<volume>
 e.g. UPDATE,4,23.12,11

 In case of cancel the line will have the format:
 CANCEL,<order_id>
 e.g. CANCEL,4

 Side will always be "BUY" or "SELL".
 A price is a string with a maximum of 4 digits behind the ".", so "2.1427" and "33.42" would be
 valid prices but "2.14275" would not be a valid price since it has more than 4 digits behind the
 comma.
 A volume will be an integer

 The expected output is:
 - List of trades in chronological order with the format:
   <symbol>,<price>,<volume>,<taker_order_id>,<maker_order_id>
   e.g. FFLY,23.55,11,4,7
   The maker order is the one being removed from the order book, the taker order is the incoming one nmatching it.
 - Then, per symbol (in alphabetical order):
   - separator "===<symbol>==="
   - bid and ask price levels (sorted best to worst by price) for that symbol in the format:
     SELL,<ask_price>,<ask_volume>
     SELL,<ask_price>,<ask_volume>
     BUY,<bid_price>,<bid_volume>
     BUY,<bid_price>,<bid_volume>
     e.g. SELL,25.67,102
          SELL,25.56,34
          BUY,25.52,23
          BUY,25.51,11
          BUY,25.43,4
'''

#
# Complete the 'runMatchingEngine' function below.
#
# The function is expected to return a STRING_ARRAY.
# The function accepts STRING_ARRAY operations as parameter.
#

'''
    ****************************************************************************

    IMPROVEMENTS:

    - Use typeguard
    - Implement an AST + Parser to handle incoming stream of text based
      instructions for order book
    - Use pytest or other testing framework (obviously doesn't work with
      HackerRank)
    - Split into multiple modules, packages (again does not work with
      HackerRank)
    - Add TTL for orders (time based order expiry)


    ****************************************************************************
'''

# TODO:
# decide on the set of operations which are common (public and private) to all data structures
# there should be some common operations between DoubleSidedLimitOrderBook, LimitOrderBook,
# LimitOrderBookPriceLevel and PriceLevel
# TODO: for DoubleSidedLimitOrderBook write complex logic to test the depth
# by inserting sequences of orders and checking after every insert,
# this logic should test all code paths



class LimitOrderBook:

    def __init__(self):
        # TICKER -> PRICE_LEVEL -> list of orders and volumes
        self.limit_order_book: dict[str, LimitOrderBookPriceLevel] = {}

    def _initialize_ticker(self, ticker: str):
        if not validate_ticker(ticker):
            raise ValueError(f'ticker \'{ticker}\' is not a valid ticker')

        if not ticker in self.limit_order_book:
            self.limit_order_book[ticker] = LimitOrderBookPriceLevel()

    def _insert_order(self, partial_order: PartialOrder):
        ticker = partial_order.to_ticker()
        self.limit_order_book[ticker].order_insert(partial_order)

    # Note: will actually remove all orders with order_id
    def _remove_orders_by_order_id(self, order_id: int) -> list[Order]:
        removed_orders = (
            list(
                reduce(
                    list.__add__,
                    map(
                        lambda limit_order_book_price_level: limit_order_book_price_level._remove_orders_by_order_id(order_id),
                        self.limit_order_book.values(),
                    ),
                    [],
                )
            )
        )
        return removed_orders

    def _find_order_ticker_by_order_id(self, order_id: int) -> int:

        def select_ticker(key_value: tuple[int, LimitOrderBookPriceLevel]) -> int:
            return key_value[0]

        def filter_by_order_id(key_value: tuple[int, LimitOrderBookPriceLevel]) -> bool:
            limit_order_book_price_level = key_value[1]
            return limit_order_book_price_level.order_id_exists(order_id)

        tickers = (
            set(
                map(
                    select_ticker,
                    filter(
                        filter_by_order_id,
                        self.limit_order_book.items(),
                    )
                )
            )
        )

        if len(tickers) == 0:
            raise RuntimeError(f'order_id not found in limit_order_book')
        elif len(tickers) > 1:
            raise RuntimeError(f'order_id duplicated in multiple limit_order_book')

        [ticker] = tickers
        return ticker

    def _get_order_by_order_id(self, order_id: int) -> Order:
        def filter_empty_list(list: list) -> bool:
            return len(list) > 0

        def extract_single_element_from_list(list: list):
            assert len(list) == 1, f'extract_single_element_from_list failed'
            return list[0]

        matching_orders = (
            list(
                reduce(
                    list.__add__,
                    map(
                        lambda limit_order_book_price_level: limit_order_book_price_level._filter_orders_by_order_id(order_id),
                        self.limit_order_book.values(),
                    ),
                    [],
                )
            )
        )
        assert len(matching_orders) == 1, f'_get_order_by_order_id failed'

        existing_order: Order = matching_orders[0]
        return existing_order

    def order_id_exists(self, order_id: int):
        return (
            any(
                filter(
                    lambda limit_order_book_price_level: limit_order_book_price_level.order_id_exists(order_id),
                    self.limit_order_book.values(),
                )
            )
        )

    def order_id_count(self, order_id: int) -> int:
        return (
            sum(
                map(
                    lambda limit_order_book_price_level: limit_order_book_price_level.order_id_count(order_id),
                    self.limit_order_book.values(),
                )
            )
        )

    def depth(self, ticker: str) -> int:
        self._initialize_ticker(ticker)
        return self.limit_order_book[ticker].depth()

    def depth_aggregated(self) -> int:
        return (
            sum(
                map(
                    lambda limit_order_book_price_level: limit_order_book_price_level.depth_aggregated(),
                    self.limit_order_book.values(),
                )
            )
        )

    # def order_insert(self, order_id: int, ticker: str, order_side: str, int_price: int, volume: int):
    def order_insert(self, order_id: int, ticker: str, order_side: str, int_price: int, volume: int):
        self._initialize_ticker(ticker)

        # check the order id doesn't exist
        if self.order_id_exists(order_id):
            raise RuntimeError(f'cannot insert order with existing order_id {order_id}')

        self._insert_order(
            PartialOrder()
            .with_order_id(order_id)
            .with_ticker(ticker)
            .with_order_side(order_side)
            .with_int_price(int_price)
            .with_volume(volume)
        )
    # def order_insert(self, order_id: int, ticker: str, int_price: int, volume: int):
    #     # assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
    #     # assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
    #     # assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR
    #     # ^ removed, done by PartialOrder

    #     self._initialize_ticker(ticker)

    #     # check the order id doesn't exist
    #     if self.order_id_exists(order_id):
    #         raise RuntimeError(f'cannot insert order with existing order_id {order_id}')

    #     # TODO: might make more sense to just construct this in a single place (here) and then
    #     # extract values from it rather than passing all the values down the call stack
    #     # or just duplicate them
    #     partial_order = PartialOrder().with_order_id(order_id).with_ticker(ticker).with_volume(volume)
    #     self._insert_order(partial_order)

        # TODO:
        # @static_vars(counter=0)
        # def count_order_id(order_id_volume_tuple: tuple[int, int]):
        #     assert len(order_id_volume_tuple) == 2, 'invalid order_id volume tuple'
        #     order_id_ = order_id_volume_tuple[0]
        #     if order_id_ == order_id
        #         count_order_id.counter += 1

        # consume(
        #     map(
        #         lambda price_level_order_book: consume(map(count_order_id, price_level_order_book)),
        #         ticker_order_book.values(),
        #     )
        # )

        # consume(
        #     map(
        #         count_order_id,
        #         ticker_order_book_price_level,
        #     )
        # )

        # insert the order into the lob

    def order_update(self, order_id: int, int_price: int, volume: int):
        # assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
        # assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR
        # ^ removed, done by PartialOrder

        # TODO: implement the below, copied from above

        # check the order id exists, and only once
        if self.order_id_count(order_id) == 0:
            raise RuntimeError(f'cannot update order with missing order_id {order_id}')
        elif self.order_id_count(order_id) > 1:
            raise RuntimeError(f'cannot update order with duplicate order_id {order_id}')

        ticker = self._find_order_ticker_by_order_id(order_id)
        self.limit_order_book[ticker].order_update(order_id, int_price, volume)

    def order_cancel(self, order_id: int):
        # check the order id exists, and only once
        if self.order_id_count(order_id) == 0:
            raise RuntimeError(f'cannot cancel order with missing order_id {order_id}')
        elif self.order_id_count(order_id) > 1:
            raise RuntimeError(f'cannot cancel order with duplicate order_id {order_id}')

        # remove matching order
        removed_orders = self._remove_orders_by_order_id(order_id)
        assert len(removed_orders) == 1, f'unexpected number of orders removed in order_cancel'
        order: Order = removed_orders[0]
        return order.to_partial_order()



# TODO
#if __name__ == '__main__':
#    run_all_tests()