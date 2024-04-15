#!/bin/python3

import math
import os
import random
import re
import sys



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

def consume(iterable):
    for _ in iterable:
        pass

# a count functional like `filter`, `map`, `reduce`
def count(iterable) -> int:
    return sum(1 for _ in iterable)

VALIDATE_TICKER_ERROR_STR = 'ticker cannot be empty string'
VALIDATE_ORDER_SIDE_ERROR_STR = 'invalid order side'
VALIDATE_INT_PRICE_ERROR_STR = 'int_price must be non-negative'
VALIDATE_VOLUME_ERROR_STR = 'volume must be positive'

def validate_ticker(ticker: str) -> bool:
    return len(ticker) > 0

def validate_order_side(order_side: str) -> bool:
    return order_side == 'BUY' or order_side == 'SELL'

def validate_int_price(int_price: int) -> bool:
    return int_price >= 0

def validate_volume(volume: int) -> bool:
    return volume > 0

def parse_price_string_and_return_int_price(price_str: str) -> int:

    split_price_str = price_str.split('.')

    if len(split_price_str) == 1:
        int_price = 100 * int(price_str)
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


class Order:

    def __init__(self, order_id: int, ticker: str, order_side: str, int_price: int, volume: int):
        assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
        assert validate_order_side(order_side), VALIDATE_ORDER_SIDE_ERROR_STR
        assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
        assert validate_volume(volume), VALIDATE_VOLUME_ERROR_STR

        self.order_id = order_id
        self.int_price = int_price
        self.volume = volume

    def match(self, order: Order) -> list[tuple[Trade, Order, Order]]:
        pass


class Trade:

    def __init__(self, ticker: str, int_price: int, volume: int, order_id_taker: int, order_id_maker: int):
        assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
        assert validate_order_side(order_side), VALIDATE_INT_PRICE_ERROR_STR
        assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR

        self.ticker = ticker
        self.int_price = int_price
        self.volume = volume
        self.order_id_taker = order_id_taker
        self.order_id_maker = order_id_maker


class PriceLevel:

    def __init__(self):
        self.price_level = []

    def _lambda_order_id_match(order: Order) -> bool:
        order_id_ = order.order_id
        return order_id_ == order_id

    def order_insert(self, order_id: int, int, ticker: str, order_side: str, int_price: int, volume: int):
        assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
        assert validate_order_side(order_side), VALIDATE_INT_PRICE_ERROR_STR
        assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
        assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR

        # check the order id doesn't exist
        count_ = (
            count(
                filter(
                    _lambda_order_id_match,
                    self.price_level,
                )
            )
        )

        if count_ > 0:
            raise RuntimeError(f'cannot insert order with existing order_id {order_id}')

        order = Order(order_id, ticker, order_side, int_price, volume)
        self.price_level.append(order)

    def order_update(self, order_id: int, volume: int):
        assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR

        # check the order id exists, and only once
        matching_orders = (
            list(
                filter(
                    _lambda_order_id_match,
                    self.price_level,
                )
            )
        )

        match_order_count = (
            len(
                matching_orders
            )
        )

        if match_order_count == 0:
            raise RuntimeError(f'cannot update order with missing order_id {order_id}')
        elif match_order_count > 1:
            raise RuntimeError(f'cannot update order with duplicate order_id {order_id}')

        existing_order = matching_orders[0]

        existing_order_volume = existing_order.volume
        existing_order.volume = volume

        if volume <= existing_order_volume:
            pass
        else:
            self.price_level = (
                list(
                    filter(
                        lambda order: not _lambda_order_id_match,
                        self.price_level,
                    )
                )
            )

            self.price_level.append(existing_order)


    def order_cancel(self, order_id: int):

        # check the order id exists, and only once
        # TODO

        # remove
        self.price_level = list(
            filter(
                lambda order: not _lambda_order_id_match(order),
                self.price_level,
            )
        )


def run_all_price_level_tests():

    def price_level_test_1():
        price_level = PriceLevel()

        price_level.order_insert(order_id=1, volume=10)
        price_level.order_insert(order_id=2, volume=20)
        price_level.order_insert(order_id=3, volume=30)

        try:
            price_level_order_insert(order_id=2, volume=20)
        except RuntimeError as e:
            assert str(e) == f'cannot insert order with duplicate order_id {2}'


    price_level_test_1()
    price_level_test_2()

class SingleTickerLimitOrderBook:

    def __init__(self):
        # PRICE_LEVEL -> list of orders and volumes
        self.limit_order_book = {}

class LimitOrderBook:

    def __init__(self):
        self.limit_order_book = {} # TICKER -> PRICE_LEVEL -> list of orders and volumes

    def order_insert(self, order_id: int, ticker: str, order_side: str, int_price: int, volume: int):
        assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
        assert validate_order_side(order_side), VALIDATE_INT_PRICE_ERROR_STR
        assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
        assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR

        if not ticker in self.limit_order_book:
            self.limit_order_book[ticker] = {}

        # check the order id doesn't exist
        ticker_order_book = self.limit_order_book[ticker]

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
        if not int_price in ticker_order_book:
            ticker_order_book[int_price] = []

        order_id_volume_tuple = (order_id, volume)
        ticker_order_book[int_price].append(order_id_volume_tuple)

    def order_update(self, order_id: int, int_price: int, volume: int):
        assert validate_order_side(order_side), VALIDATE_INT_PRICE_ERROR_STR
        assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
        assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR

        if not ticker in self.limit_order_book:
            raise RuntimeError(f'ticker {ticker} not in order book when update called')

        # ! don't do this - order by price level
        if not order_id in self.limit_order_book[ticker]:
            raise RuntimeError(f'')

        pass

    def order_cancel(self, order_id: int):
        pass


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




 INSERT,<order_id>,<symbol>,<side>,<price>,<volume>
 e.g. INSERT,4,FFLY,BUY,23.45,12

 UPDATE,<order_id>,<price>,<volume>
 e.g. UPDATE,4,23.12,11

 CANCEL,<order_id>
 e.g. CANCEL,4


def runMatchingEngine(operations: list[str]) -> list[str]:
    # TODO ast parser

    lob = LimitOrderBook()

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

            lob.order_insert(order_id, ticker, order_side, int_price, volume)
        elif operation_opcode == 'UPDATE':
            assert len(split_operation) == 4, 'invalid UPDATE syntax'
            price_str = split_operation[2]
            volume = split_operation[3]

            int_price = parse_price_string_and_convert_to_int_price(price_str)

            lob.order_update(order_id, int_price, volume)
        elif operation_opcode == 'CANCEL':
            assert len(split_operation) == 2, 'invalid CANCEL syntax'

            lob.order_cancel(order_id)
        else:
            raise ValueError(f'invalid opcode: {operation_opcode}')



def run_all_tests():
    run_all_price_level_tests()
    run_all_single_ticker_order_book_tests()
    run_all_limit_order_book_tests()
    run_all_double_limit_order_book_tests()


if __name__ == '__main__':
    run_all_tests()

    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    operations_count = int(input().strip())

    operations = []

    for _ in range(operations_count):
        operations_item = input()
        operations.append(operations_item)

    result = runMatchingEngine(operations)

    fptr.write('\n'.join(result))
    fptr.write('\n')

    fptr.close()
