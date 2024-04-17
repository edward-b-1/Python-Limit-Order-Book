#!/bin/python3

import math
import os
import random
import re
import sys

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


    ****************************************************************************
'''

# TODO:
# decide on the set of operations which are common (public and private) to all data structures
# there should be some common operations between DoubleSidedLimitOrderBook, LimitOrderBook,
# LimitOrderBookPriceLevel and PriceLevel
# TODO: prices can have 4 decimal places! use a fixed integer conversion factor of 1000
# 1000 * digits before `.` + digits after `.`, just split on `.` convert to int
# multiply and add
# TODO: for DoubleSidedLimitOrderBook write complex logic to test the depth
# by inserting sequences of orders and checking after every insert,
# this logic should test all code paths

def consume(iterable):
    for _ in iterable:
        pass

# a count functional like `filter`, `map`, `reduce`
def count(iterable) -> int:
    return sum(1 for _ in iterable)

VALIDATE_ORDER_ID_ERROR_STR = 'order_id cannot be negative'
VALIDATE_TICKER_ERROR_STR = 'ticker cannot be empty string'
VALIDATE_ORDER_SIDE_ERROR_STR = 'invalid order side'
VALIDATE_INT_PRICE_ERROR_STR = 'int_price must be non-negative'
VALIDATE_VOLUME_ERROR_STR = 'volume must be positive'

def validate_order_id(order_id: int) -> bool:
    return order_id >= 0

def validate_ticker(ticker: str) -> bool:
    return len(ticker) > 0

def validate_order_side(order_side: str) -> bool:
    return order_side == 'BUY' or order_side == 'SELL'

def validate_int_price(int_price: int) -> bool:
    return int_price >= 0

def validate_volume(volume: int) -> bool:
    return volume > 0

# TODO: needs 5 dp
def parse_price_string_and_convert_to_int_price(price_str: str) -> int:

    split_price_str = price_str.split('.')

    try:
        if len(split_price_str) == 1:
            int_price = 100 * int(price_str)
            return int_price
        elif len(split_price_str) == 2:
            integer_part_price_str = split_price_str[0]
            fractional_part_price_str = split_price_str[1]

            if len(fractional_part_price_str) == 1:
                int_price = 100 * int(integer_part_price_str) + 10 * int(fractional_part_price_str)
                return int_price
            elif len(fractional_part_price_str) == 2:
                int_price = 100 * int(integer_part_price_str) + int(fractional_part_price_str)
                return int_price
            else:
                raise ValueError(f'{price_str} is not a valid string formatted price')
        else:
            raise ValueError(f'{price_str} is not a valid string formatted price')
    except ValueError as e:
        raise ValueError(f'{price_str} is not a valid string formatted price')

def run_all_parse_price_string_and_convert_to_int_price_tests():

    def parse_price_string_and_convert_to_int_price_test_1():
        price_string = '12'
        int_price = parse_price_string_and_convert_to_int_price(price_string)
        assert int_price == 1200, f'parse_price_string_and_convert_to_int_price_test_1 failed: {int_price}'

    def parse_price_string_and_convert_to_int_price_test_2():
        price_string = '12.3'
        int_price = parse_price_string_and_convert_to_int_price(price_string)
        assert int_price == 1230, f'parse_price_string_and_convert_to_int_price_test_2 failed: {int_price}'

    def parse_price_string_and_convert_to_int_price_test_3():
        price_string = '12.34'
        int_price = parse_price_string_and_convert_to_int_price(price_string)
        assert int_price == 1234, f'parse_price_string_and_convert_to_int_price_test_3 failed: {int_price}'

    def parse_price_string_and_convert_to_int_price_test_4():
        price_string = '12.345'
        try:
            parse_price_string_and_convert_to_int_price(price_string)
        except ValueError as e:
            assert str(e) == f'{price_string} is not a valid string formatted price'

    def parse_price_string_and_convert_to_int_price_test_5():
        price_string = 'hello world'
        try:
            parse_price_string_and_convert_to_int_price(price_string)
        except ValueError as e:
            assert str(e) == f'{price_string} is not a valid string formatted price'

    parse_price_string_and_convert_to_int_price_test_1()
    parse_price_string_and_convert_to_int_price_test_2()
    parse_price_string_and_convert_to_int_price_test_3()
    parse_price_string_and_convert_to_int_price_test_4()
    parse_price_string_and_convert_to_int_price_test_5()


class Order:

    def __init__(self, order_id: int, ticker: str, order_side: str, int_price: int, volume: int):
        assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
        assert validate_order_side(order_side), VALIDATE_ORDER_SIDE_ERROR_STR
        assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
        assert validate_volume(volume), VALIDATE_VOLUME_ERROR_STR

        self.order_id = order_id
        self.ticker = ticker
        self.order_side = order_side
        self.int_price = int_price
        self.volume = volume

    def match(self, order) -> list[tuple]:
        '''
            Return a pair of trades: maker order converted to trade, taker order converted to trade
            and a remaining order, or None.
        '''
        pass


class PartialOrder:

    def __init__(self):
        self.order_id = None
        self.ticker = None
        self.order_side = None
        self.int_price = None
        self.volume = None

    def __str__(self) -> str:
        return f'PartialOrder({self.order_id}, {self.ticker}, {self.order_side}, price={self.int_price}, volume={self.volume})'

    def copy(self):
        return (
            PartialOrder()
            .set_order_id(self.order_id)
            .set_ticker(self.ticker)
            .set_order_side(self.order_side)
            .set_int_price(self.int_price)
            .set_volume(self.volume)
        )

    def set_order_id(self, order_id: int):
        if order_id is None: return self
        self.order_id = order_id
        return self

    def set_ticker(self, ticker: str):
        if ticker is None: return self
        assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
        self.ticker = ticker
        return self

    def set_order_side(self, order_side: str):
        if order_side is None: return self
        assert validate_order_side(order_side), VALIDATE_ORDER_SIDE_ERROR_STR
        self.order_side = order_side
        return self

    def set_int_price(self, int_price: int):
        if int_price is None: return self
        assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
        self.int_price = int_price
        return self

    def set_volume(self, volume: int):
        if volume is None: return self
        assert validate_volume(volume), VALIDATE_VOLUME_ERROR_STR
        self.volume = volume
        return self

    def with_order_id(self, order_id: int):
        return self.copy().set_order_id(order_id)

    def with_ticker(self, ticker: str):
        assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
        return self.copy().set_ticker(ticker)

    def with_order_side(self, order_side: str):
        assert validate_order_side(order_side), VALIDATE_ORDER_SIDE_ERROR_STR
        return self.copy().set_order_side(order_side)

    def with_int_price(self, int_price: int):
        assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
        return self.copy().set_int_price(int_price)

    def with_volume(self, volume: int):
        assert validate_volume(volume), VALIDATE_VOLUME_ERROR_STR
        return self.copy().set_volume(volume)

    def to_order_id(self) -> int:
        assert validate_order_id(self.order_id), VALIDATE_ORDER_ID_ERROR_STR
        return self.order_id

    def to_ticker(self) -> str:
        assert validate_ticker(self.ticker), VALIDATE_TICKER_ERROR_STR
        return self.ticker

    def to_order_side(self) -> str:
        assert validate_order_side(self.order_side), VALIDATE_ORDER_SIDE_ERROR_STR
        return self.order_side

    def to_int_price(self) -> int:
        assert validate_int_price(self.int_price), VALIDATE_INT_PRICE_ERROR_STR
        return self.int_price

    def to_volume(self) -> int:
        assert validate_volume(self.volume), VALIDATE_VOLUME_ERROR_STR
        return self.volume

    def to_order(self):
        if None in [self.order_id, self.ticker, self.order_side, self.int_price, self.volume]:
            raise RuntimeError(f'PartialOrder has missing fields')

        return Order(
            order_id=self.order_id,
            ticker=self.ticker,
            order_side=self.order_side,
            int_price=self.int_price,
            volume=self.volume,
        )

def run_all_partial_order_tests():

    def partial_order_test():
        partial_order = PartialOrder()

        try:
            partial_order.to_order()
        except RuntimeError as e:
            assert str(e) == f'PartialOrder has missing fields'

        partial_order.set_order_id(1).set_ticker('PYTH').set_order_side('BUY').set_int_price(1234)

        try:
            partial_order.to_order()
        except RuntimeError as e:
            assert str(e) == f'PartialOrder has missing fields'

        partial_order.set_volume(10)
        order = partial_order.to_order()

        assert order.order_id == 1, 'unexpected value for order_id'
        assert order.order_side == 'BUY', 'unexpected value for order_side'
        assert order.int_price == 1234, 'unexpected value for int_price'
        assert order.volume == 10, 'unexpected value for volume'

    partial_order_test()



class Trade:

    def __init__(self, ticker: str, int_price: int, volume: int, order_id_taker: int, order_id_maker: int):
        assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
        assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
        assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR

        self.ticker = ticker
        self.int_price = int_price
        self.volume = volume
        self.order_id_taker = order_id_taker
        self.order_id_maker = order_id_maker


class PriceLevel:

    def __init__(self):
        # PRICE_LEVEL: list of Order by priority
        self.price_level: list[Order] = []

    def _lambda_order_id_match(order: Order, order_id: int) -> bool:
        return order.order_id == order_id

    def _remove_order_by_order_id(self, order_id: int):
        self.price_level = (
            list(
                filter(
                    lambda order: not PriceLevel._lambda_order_id_match(order, order_id),
                    self.price_level,
                )
            )
        )

    def _insert_order(self, order: Order):
        self.price_level.append(order)

    def _filter_orders_by_order_id(self, order_id: int) -> list[Order]:
        return (
            list(
                filter(
                    lambda order: PriceLevel._lambda_order_id_match(order, order_id),
                    self.price_level,
                )
            )
        )

    def _count_orders_by_order_id(self, order_id: int):
        return (
            count(
                filter(
                    lambda order: PriceLevel._lambda_order_id_match(order, order_id),
                    self.price_level,
                )
            )
        )

    def order_id_exists(self, order_id: int) -> bool:
        return self._count_orders_by_order_id(order_id) > 0

    def order_id_count(self, order_id: int) -> int:
        return self._count_orders_by_order_id(order_id)

    # filter, get_or_none and get could perhaps be merged
    # filter just filters, doesn't care if there are 0, 1 or more orders
    # get requires that there is exactly 1 order
    # get_or_none requires 1 or none

    # TODO: might not have a use for this?
    def _get_order_or_none_by_order_id(self, order_id: int) -> Order|None:

        matching_orders = self._filter_orders_by_order_id(order_id)
        assert len(matching_orders) <= 1, 'get_order_or_none_by_order_id failed'

        existing_order: Order|None = None
        if len(matching_orders) == 1:
            existing_order = matching_orders[0]

        return existing_order

    # TODO: implement in terms of _get_order_or_none_by_order_id
    def _get_order_by_order_id(self, order_id: int) -> Order:

        matching_orders = self._filter_orders_by_order_id(order_id)
        assert len(matching_orders) == 1, '_get_order_by_order_id failed'

        existing_order: Order = matching_orders[0]
        return existing_order

    def depth(self) -> int:
        return len(self.price_level)

    # OLD API, move to another class
    # def order_insert(self, order_id: int, ticker: str, order_side: str, int_price: int, volume: int):
    #     assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
    #     assert validate_order_side(order_side), VALIDATE_INT_PRICE_ERROR_STR
    #     assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
    #     assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR

    # TODO: change this to a partial order and call partial_order.to_order to create the order before calling _append_order
    def order_insert(self, partial_order: PartialOrder):
        order_id = partial_order.order_id

        # check the order id doesn't exist
        if self.order_id_exists(order_id):
            raise RuntimeError(f'cannot insert order with existing order_id {order_id}')

        #order = Order(order_id, ticker, order_side, int_price, volume)
        order = partial_order.to_order()
        self._insert_order(order)

    # OLD API, move to another class
    # def order_update(self, order_id: int, volume: int):
    #     assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR

    def order_update(self, order_id: int, volume: int):
        assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR

        # check the order id exists, and only once
        if self.order_id_count(order_id) == 0:
            raise RuntimeError(f'cannot update order with missing order_id {order_id}')
        elif self.order_id_count(order_id) > 1:
            raise RuntimeError(f'cannot update order with duplicate order_id {order_id}')

        existing_order = self._get_order_by_order_id(order_id)

        existing_order_volume = existing_order.volume
        existing_order.volume = volume

        if volume <= existing_order_volume:
            pass
        else:
            # reduce order priority if order volume is increased
            self._remove_order_by_order_id(order_id)
            self._insert_order(existing_order)

    # OLD API, move to another class
    # def order_cancel(self, order_id: int):

    def order_cancel(self, order_id: int):

        # check the order id exists, and only once
        if self.order_id_count(order_id) == 0:
            raise RuntimeError(f'cannot cancel order with missing order_id {order_id}')
        elif self.order_id_count(order_id) > 1:
            raise RuntimeError(f'cannot cancel order with duplicate order_id {order_id}')

        # remove matching order
        self._remove_order_by_order_id(order_id)


def run_all_price_level_tests():

    def price_level_test_1():
        ticker = 'PYTH'
        order_side = 'BUY'
        int_price = 1000
        partial_order = PartialOrder().set_ticker(ticker).set_order_side(order_side).set_int_price(int_price)

        partial_order_1 = partial_order.with_order_id(1).with_volume(10)
        partial_order_2 = partial_order.with_order_id(2).with_volume(20)
        partial_order_3 = partial_order.with_order_id(3).with_volume(30)

        price_level = PriceLevel()

        # price_level.order_insert(order_id=1, ticker=ticker, order_side=order_side, int_price=int_price, volume=10)
        # price_level.order_insert(order_id=2, ticker=ticker, order_side=order_side, int_price=int_price, volume=20)
        # price_level.order_insert(order_id=3, ticker=ticker, order_side=order_side, int_price=int_price, volume=30)
        price_level.order_insert(partial_order_1)
        price_level.order_insert(partial_order_2)
        price_level.order_insert(partial_order_3)

        try:
            price_level.order_insert(partial_order_2)
        except RuntimeError as e:
            assert str(e) == f'cannot insert order with existing order_id {partial_order_2.order_id}'

        price_level.order_cancel(order_id=2)

        order_id = 2
        try:
            price_level.order_cancel(order_id)
        except RuntimeError as e:
            assert str(e) == f'cannot cancel order with missing order_id {order_id}'

        price_level.order_cancel(order_id=1)

        price_level.order_update(order_id=3, volume=50)
        assert price_level._get_order_by_order_id(order_id=3).volume == 50, f'unexpected order volume'

        price_level.order_cancel(order_id=3)
        depth = price_level.depth()
        assert depth == 0, f'depth is not 0, depth = {depth}'

    price_level_test_1()
    #price_level_test_2()


class LimitOrderBookPriceLevel:

    def __init__(self):
        # PRICE_LEVEL -> list of orders and volumes
        self.price_levels: dict[int, PriceLevel] = {}

    def _initialize_price_level(self, int_price: int):
        if not int_price in self.price_levels:
            self.price_levels[int_price] = PriceLevel()

    def _insert_order(self, partial_order: PartialOrder):
        int_price = partial_order.to_int_price()
        self.price_levels[int_price].order_insert(partial_order)

    def _filter_orders_by_order_id(self, order_id: int):
        def filter_empty_list(list: list) -> bool:
            return len(list) > 0

        def extract_single_element_from_list(list: list):
            assert len(list) == 1, f'extract_single_element_from_list failed, length is {len(list)}'
            return list[0]

        return (
            list(
                map(
                    extract_single_element_from_list,
                    filter(
                        filter_empty_list,
                        map(
                            lambda price_level: price_level._filter_orders_by_order_id(order_id),
                            self.price_levels.values(),
                        ),
                    ),
                )
            )
        )

    # Note: will actually remove all orders with order_id
    def _remove_order_by_order_id(self, order_id: int):
        consume(
            map(
                lambda price_level: price_level._remove_order_by_order_id(order_id),
                self.price_levels.values(),
            )
        )

    def _find_order_price_level_by_order_id(self, order_id: int) -> int:

        def select_int_price_level(key_value: tuple[int, PriceLevel]) -> int:
            return key_value[0]

        def filter_by_order_id(key_value: tuple[int, PriceLevel]) -> bool:
            price_level = key_value[1]
            return price_level.order_id_exists(order_id)

        int_price_levels = (
            set(
                map(
                    select_int_price_level,
                    filter(
                        filter_by_order_id,
                        self.price_levels.items(),
                    )
                )
            )
        )

        if len(int_price_levels) == 0:
            raise RuntimeError(f'order_id not found in price_levels')
        elif len(int_price_levels) > 1:
            raise RuntimeError(f'order_id duplicated in multiple price_levels')

        [int_price_level] = int_price_levels
        return int_price_level

    def _get_order_by_order_id(self, order_id: int) -> Order:
        def filter_empty_list(list: list) -> bool:
            return len(list) > 0

        def extract_single_element_from_list(list: list):
            assert len(list) == 1, f'extract_single_element_from_list failed'
            return list[0]

        matching_orders = (
            list(
                map(
                    extract_single_element_from_list,
                    filter(
                        filter_empty_list,
                        map(
                            lambda price_level: price_level._filter_orders_by_order_id(order_id),
                            self.price_levels.values(),
                        ),
                    ),
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
                    lambda price_level: price_level.order_id_exists(order_id),
                    self.price_levels.values(),
                )
            )
        )

    def order_id_count(self, order_id: int) -> int:
        return (
            sum(
                map(
                    lambda price_level: price_level.order_id_count(order_id),
                    self.price_levels.values(),
                )
            )
        )

    def depth(self, int_price: int) -> int:
        self._initialize_price_level(int_price)
        return self.price_levels[int_price].depth()

    def depth_aggregated(self) -> int:
        return (
            sum(
                map(
                    lambda price_level: price_level.depth(),
                    self.price_levels.values(),
                )
            )
        )

    # def order_insert(self, order_id: int, ticker: str, order_side: str, int_price: int, volume: int):
    #     assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
    #     assert validate_order_side(order_side), VALIDATE_INT_PRICE_ERROR_STR
    #     assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
    #     assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR

    def order_insert(self, partial_order: PartialOrder):
        int_price = partial_order.to_int_price()
        self._initialize_price_level(int_price)

        order_id = partial_order.order_id

        # check the order id doesn't exist
        if self.order_id_exists(order_id):
            raise RuntimeError(f'cannot insert order with existing order_id {order_id}')

        partial_order = partial_order.with_int_price(int_price)
        self._insert_order(partial_order)

    def order_update(self, order_id: int, int_price: int, volume: int):
        assert validate_int_price(int_price) > 0, VALIDATE_INT_PRICE_ERROR_STR
        assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR

        # check the order id exists, and only once
        if self.order_id_count(order_id) == 0:
            raise RuntimeError(f'cannot update order with missing order_id {order_id}')
        elif self.order_id_count(order_id) > 1:
            raise RuntimeError(f'cannot update order with duplicate order_id {order_id}')

        existing_order_int_price = self._find_order_price_level_by_order_id(order_id)
        if existing_order_int_price == int_price:
            self.price_levels[existing_order_int_price].order_update(order_id, volume)
        else:
            self.price_levels[existing_order_int_price].order_cancel(order_id)
            self.price_levels[int_price].order_insert(order_id)
            # TODO write a test for both of these cases

    def order_cancel(self, order_id: int):
        # check the order id exists, and only once
        if self.order_id_count(order_id) == 0:
            raise RuntimeError(f'cannot cancel order with missing order_id {order_id}')
        elif self.order_id_count(order_id) > 1:
            raise RuntimeError(f'cannot cancel order with duplicate order_id {order_id}')

        # remove matching order
        self._remove_order_by_order_id(order_id)


def run_all_limit_order_book_price_level_tests():

    def price_level_test_1():
        ticker = 'PYTH'
        order_side = 'BUY'
        int_price_1 = 1000
        int_price_2 = 1010
        partial_order = PartialOrder().set_ticker(ticker).set_order_side(order_side)

        partial_order_1 = partial_order.with_order_id(1).with_volume(10).with_int_price(int_price_1)
        partial_order_2 = partial_order.with_order_id(2).with_volume(20).with_int_price(int_price_1)
        partial_order_3 = partial_order.with_order_id(3).with_volume(30).with_int_price(int_price_1)
        partial_order_4 = partial_order.with_order_id(4).with_volume(40).with_int_price(int_price_2)
        partial_order_5 = partial_order.with_order_id(5).with_volume(50).with_int_price(int_price_2)

        limit_order_book_price_level = LimitOrderBookPriceLevel()

        limit_order_book_price_level.order_insert(partial_order_1)
        limit_order_book_price_level.order_insert(partial_order_2)
        limit_order_book_price_level.order_insert(partial_order_3)
        limit_order_book_price_level.order_insert(partial_order_4)
        limit_order_book_price_level.order_insert(partial_order_5)

        depth = limit_order_book_price_level.depth_aggregated()
        assert depth == 5, f'depth is not 5, depth = {depth}'

        # inserting a duplicate fails
        try:
            limit_order_book_price_level.order_insert(partial_order_2)
        except RuntimeError as e:
            assert str(e) == f'cannot insert order with existing order_id {partial_order_2.order_id}'

        limit_order_book_price_level.order_cancel(order_id=2)

        # cancelling a non-existing/already cancelled order fails
        order_id = 2
        try:
            limit_order_book_price_level.order_cancel(order_id)
        except RuntimeError as e:
            assert str(e) == f'cannot cancel order with missing order_id {order_id}'

        limit_order_book_price_level.order_cancel(order_id=1)

        # TODO: can you update an order to change the price?
        limit_order_book_price_level.order_update(order_id=3, int_price=int_price_1, volume=50) # TODO: write a change price test
        assert limit_order_book_price_level._get_order_by_order_id(order_id=3).int_price == int_price_1, f'unexpected order int_price'
        assert limit_order_book_price_level._get_order_by_order_id(order_id=3).volume == 50, f'unexpected order volume'

        limit_order_book_price_level.order_cancel(order_id=3)

        limit_order_book_price_level.order_cancel(order_id=4)
        limit_order_book_price_level.order_cancel(order_id=5)

        depth = limit_order_book_price_level.depth_aggregated()
        assert depth == 0, f'depth is not 0, depth = {depth}'

    price_level_test_1()
    #price_level_test_2()


class LimitOrderBook:

    def __init__(self):
        # TICKER -> PRICE_LEVEL -> list of orders and volumes
        self.limit_order_book: dict[str, LimitOrderBookPriceLevel] = {}

    def _initialize_ticker(self, ticker: str):
        if not ticker in self.limit_order_book:
            self.limit_order_book[ticker] = LimitOrderBookPriceLevel()

    def _insert_order(self, partial_order: PartialOrder):
        ticker = partial_order.to_ticker()
        self.limit_order_book[ticker].order_insert(partial_order)

    # Note: will actually remove all orders with order_id
    def _remove_order_by_order_id(self, order_id: int):
        consume(
            map(
                lambda limit_order_book_price_level: limit_order_book_price_level._remove_order_by_order_id(order_id),
                self.limit_order_book.values(),
            )
        )

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
                map(
                    extract_single_element_from_list,
                    filter(
                        filter_empty_list,
                        map(
                            lambda limit_order_book_price_level: limit_order_book_price_level._filter_orders_by_order_id(order_id),
                            self.limit_order_book.values(),
                        ),
                    ),
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
        self._remove_order_by_order_id(order_id)


def run_all_limit_order_book_tests():

    def price_level_test_1():
        ticker_pyth = 'PYTH'
        ticker_cpp = 'CPP'
        order_side = 'BUY'
        int_price_1 = 1000

        limit_order_book_price_level = LimitOrderBook()

        limit_order_book_price_level.order_insert(1, ticker=ticker_pyth, order_side=order_side, int_price=int_price_1, volume=10)
        limit_order_book_price_level.order_insert(2, ticker=ticker_pyth, order_side=order_side, int_price=int_price_1, volume=20)
        limit_order_book_price_level.order_insert(3, ticker=ticker_pyth, order_side=order_side, int_price=int_price_1, volume=30)

        limit_order_book_price_level.order_insert(4, ticker=ticker_cpp, order_side=order_side, int_price=int_price_1, volume=40)
        limit_order_book_price_level.order_insert(5, ticker=ticker_cpp, order_side=order_side, int_price=int_price_1, volume=50)
        limit_order_book_price_level.order_insert(6, ticker=ticker_cpp, order_side=order_side, int_price=int_price_1, volume=60)

        depth = limit_order_book_price_level.depth_aggregated()
        assert depth == 6, f'depth is not 6, depth = {depth}'

        # inserting a duplicate fails
        try:
            limit_order_book_price_level.order_insert(3, ticker=ticker_pyth, order_side=order_side, int_price=int_price_1, volume=30)
        except RuntimeError as e:
            assert str(e) == f'cannot insert order with existing order_id {3}'

        limit_order_book_price_level.order_cancel(order_id=2)

        # cancelling a non-existing/already cancelled order fails
        order_id = 2
        try:
            limit_order_book_price_level.order_cancel(order_id)
        except RuntimeError as e:
            assert str(e) == f'cannot cancel order with missing order_id {order_id}'

        limit_order_book_price_level.order_cancel(order_id=1)

        # TODO: can you update an order to change the price?
        limit_order_book_price_level.order_update(order_id=3, int_price=int_price_1, volume=50)
        assert limit_order_book_price_level._get_order_by_order_id(order_id=3).int_price == int_price_1, f'unexpected order int_price'
        assert limit_order_book_price_level._get_order_by_order_id(order_id=3).volume == 50, f'unexpected order volume'

        limit_order_book_price_level.order_cancel(order_id=3)

        limit_order_book_price_level.order_cancel(order_id=4)
        limit_order_book_price_level.order_cancel(order_id=5)
        limit_order_book_price_level.order_cancel(order_id=6)

        depth = limit_order_book_price_level.depth_aggregated()
        assert depth == 0, f'depth is not 0, depth = {depth}'

    price_level_test_1()


class DoubleLimitOrderBook:

    def __init__(self):
        # SIDE -> TICKER -> PRICE_LEVEL -> list of volumes
        self.double_limit_order_book = {
            'BUY': LimitOrderBook(),
            'SELL': LimitOrderBook(),
        }

    def order_insert(self, order_id: int, ticker: str, order_side: str, int_price: int, volume: int):
        pass

    def order_update(self, order_id: int, int_price: int, volume: int):
        pass

    def order_cancel(self, order_id: int):
        pass




#  INSERT,<order_id>,<symbol>,<side>,<price>,<volume>
#  e.g. INSERT,4,FFLY,BUY,23.45,12

#  UPDATE,<order_id>,<price>,<volume>
#  e.g. UPDATE,4,23.12,11

#  CANCEL,<order_id>
#  e.g. CANCEL,4


def runMatchingEngine(operations: list[str]) -> list[str]:
    # TODO ast parser

    lob = DoubleLimitOrderBook()

    for operation in operations:
        split_operation = operation.split(',')
        assert len(split_operation) > 1, 'invalid operation'

        operation_opcode = split_operation[0]
        order_id = split_operation[1]

        if operation_opcode == 'INSERT':
            assert len(split_operation) == 6, 'invalid INSERT syntax'
            ticker = split_operation[2]
            order_side = split_operation[3]
            price_str = split_operation[4]
            volume = split_operation[5]

            int_price = parse_price_string_and_convert_to_int_price(price_str)
            volume = int(volume)

            # TODO: keep this API the same, PartialOrder should be an internal implementation detail
            lob.order_insert(order_id, ticker, order_side, int_price, volume)
        elif operation_opcode == 'UPDATE':
            assert len(split_operation) == 4, 'invalid UPDATE syntax'
            price_str = split_operation[2]
            volume = split_operation[3]
            volume = int(volume)

            int_price = parse_price_string_and_convert_to_int_price(price_str)

            lob.order_update(order_id, int_price, volume)
        elif operation_opcode == 'CANCEL':
            assert len(split_operation) == 2, 'invalid CANCEL syntax'

            lob.order_cancel(order_id)
        else:
            raise ValueError(f'invalid opcode: {operation_opcode}')

    return []



def run_all_tests():
    run_all_parse_price_string_and_convert_to_int_price_tests()
    #run_all_order_tests()
    run_all_partial_order_tests()
    run_all_price_level_tests()
    run_all_limit_order_book_price_level_tests()
    run_all_limit_order_book_tests()
    # run_all_double_limit_order_book_tests()


if __name__ == '__main__':
    run_all_tests()

    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    operations_count = int(input().strip())
    print(f'operations_count={operations_count}')

    operations = []

    for _ in range(operations_count):
        operations_item = input()
        operations.append(operations_item)

    print(operations)

    result = runMatchingEngine(operations)

    fptr.write('\n'.join(result))
    fptr.write('\n')

    fptr.close()
