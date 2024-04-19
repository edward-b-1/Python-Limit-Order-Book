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

def parse_price_string_and_convert_to_int_price(price_str: str) -> int:
    '''
        prices can have 4 decimal places!
        use a fixed integer conversion factor of 1000
        1000 * digits before `.` + digits after `.`, just split on `.`
        convert to int multiply and add
    '''

    split_price_str = price_str.split('.')

    try:
        if len(split_price_str) == 1:
            int_price = 10000 * int(price_str)
            return int_price
        elif len(split_price_str) == 2:
            integer_part_price_str = split_price_str[0]
            fractional_part_price_str = split_price_str[1]
            scaled_fractional_part_price_str = 0

            if len(fractional_part_price_str) > 4:
                raise ValueError(f'{price_str} is not a valid string formatted price')
            elif len(fractional_part_price_str) == 0:
                raise ValueError(f'{price_str} is not a valid string formatted price')
            else:
                missing_digits = 4 - len(fractional_part_price_str)
                scale_factor = 10**missing_digits
                scaled_fractional_part_price_str = scale_factor * int(fractional_part_price_str)

            return 10000 * int(integer_part_price_str) + scaled_fractional_part_price_str

            # if len(fractional_part_price_str) == 1:
            #     int_price = 100 * int(integer_part_price_str) + 10 * int(fractional_part_price_str)
            #     return int_price
            # elif len(fractional_part_price_str) == 2:
            #     int_price = 100 * int(integer_part_price_str) + int(fractional_part_price_str)
            #     return int_price
            # else:
            #     raise ValueError(f'{price_str} is not a valid string formatted price')
        else:
            raise ValueError(f'{price_str} is not a valid string formatted price')
    except ValueError as e:
        raise ValueError(f'{price_str} is not a valid string formatted price')


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

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Order): return False
        if self.order_id != value.order_id: return False
        if self.ticker != value.ticker: return False
        if self.order_side != value.order_side: return False
        if self.int_price != value.int_price: return False
        if self.volume != value.volume: return False
        return True

    def __str__(self) -> str:
        return (
            f'PartialOrder('
            f'{self.order_id}, '
            f'{self.ticker}, '
            f'{self.order_side}, '
            f'price={self.int_price}, '
            f'volume={self.volume}'
            f')'
        )

    def to_partial_order(self):
        return (
            PartialOrder()
            .with_order_id(self.order_id)
            .with_ticker(self.ticker)
            .with_order_side(self.order_side)
            .with_int_price(self.int_price)
            .with_volume(self.volume)
        )

    def set_int_price(self, int_price: int) -> None:
        assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR

    def match(self, taker_order) -> list[tuple]:
        '''
            The Maker order must be self. The Taker order must be order.

            If price levels cross through, the Maker recieves the bonus/premium, meaning
            that the Taker price is used.

            The Maker order (self) is modified if a Trade occurs.
            The Taker order (`order`) is modified if a Trade occurs.

            Return:
                A Trade, if orders are compatiable, or None.
        '''
        maker_order = self

        if maker_order.ticker != taker_order.ticker:
            return None

        if maker_order.order_side == taker_order.order_side:
            return None

        if maker_order.order_side == 'BUY' and taker_order.order_side == 'SELL':
            if maker_order.int_price < taker_order.int_price:
                return None

        if maker_order.order_side == 'SELL' and taker_order.order_side == 'BUY':
            if maker_order.int_price > taker_order.int_price:
                return None

        match_int_price = taker_order.int_price

        match_volume = min(maker_order.volume, taker_order.volume)
        maker_volume = maker_order.volume - match_volume
        taker_volume = taker_order.volume - match_volume

        # TODO:
        # NOTE: it is the responsibility of the managing data structure to
        # filter orders which have zero remaining volume
        maker_order.volume = maker_volume
        taker_order.volume = taker_volume

        trade = Trade(
            order_id_maker=maker_order.order_id,
            order_id_taker=taker_order.order_id,
            ticker=self.ticker,
            int_price=match_int_price,
            volume=match_volume,
        )

        return trade



class PartialOrder:

    def __init__(self):
        self.order_id = None
        self.ticker = None
        self.order_side = None
        self.int_price = None
        self.volume = None

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, PartialOrder): return False
        if self.order_id != value.order_id: return False
        if self.ticker != value.ticker: return False
        if self.order_side != value.order_side: return False
        if self.int_price != value.int_price: return False
        if self.volume != value.volume: return False
        return True

    def __str__(self) -> str:
        return (
            f'PartialOrder('
            f'{self.order_id}, '
            f'{self.ticker}, '
            f'{self.order_side}, '
            f'price={self.int_price}, '
            f'volume={self.volume}'
            f')'
        )

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



class Trade:

    def __init__(self, order_id_maker: int, order_id_taker: int, ticker: str, int_price: int, volume: int):
        assert validate_order_id(order_id_maker), VALIDATE_ORDER_ID_ERROR_STR
        assert validate_order_id(order_id_taker), VALIDATE_ORDER_ID_ERROR_STR
        assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
        assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
        assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR

        self.order_id_maker = order_id_maker
        self.order_id_taker = order_id_taker
        self.ticker = ticker
        self.int_price = int_price
        self.volume = volume

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Trade): return False
        if self.order_id_maker != value.order_id_maker: return False
        if self.order_id_taker != value.order_id_taker: return False
        if self.ticker != value.ticker: return False
        if self.int_price != value.int_price: return False
        if self.volume != value.volume: return False
        return True

    def __str__(self) -> str:
        return (
            f'Trade('
            f'order_id_maker={self.order_id_maker}, '
            f'order_id_taker={self.order_id_taker}, '
            f'{self.ticker}, '
            f'price={self.int_price}, '
            f'volume={self.volume}'
            f')'
        )


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

    def _query_priority(self, order_id: int) -> int:
        #matching_order = next(order for order in self.price_level if _lambda_order_id_match(order, order_id))
        #priority = self.price_level.index(matching_order)
        _lambda_order_id_match = PriceLevel._lambda_order_id_match
        index = (
            next(
                index for (index, order) in enumerate(self.price_level)
                    if _lambda_order_id_match(order, order_id))
        )
        return index

    def depth(self) -> int:
        return len(self.price_level)

    def order_insert(self, partial_order: PartialOrder):
        order_id = partial_order.order_id

        # check the order id doesn't exist
        if self.order_id_exists(order_id):
            raise RuntimeError(f'cannot insert order with existing order_id {order_id}')

        #order = Order(order_id, ticker, order_side, int_price, volume)
        order = partial_order.to_order()
        self._insert_order(order)

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

    # TODO: update semantics of others (return partialorder)
    def order_cancel(self, order_id: int):

        # check the order id exists, and only once
        if self.order_id_count(order_id) == 0:
            raise RuntimeError(f'cannot cancel order with missing order_id {order_id}')
        elif self.order_id_count(order_id) > 1:
            raise RuntimeError(f'cannot cancel order with duplicate order_id {order_id}')

        # remove matching order
        order = self._get_order_by_order_id(order_id)
        self._remove_order_by_order_id(order_id)
        return order.to_partial_order()


class LimitOrderBookPriceLevel:

    def __init__(self):
        # PRICE_LEVEL -> list of orders and volumes
        self.price_levels: dict[int, PriceLevel] = {}

    def _initialize_price_level(self, int_price: int):
        if not validate_int_price(int_price):
            raise ValueError(f'price \'{int_price}\' is not a valid integer price')

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

    def _query_priority(self, order_id: int) -> int:
        int_price = self._find_order_price_level_by_order_id(order_id)
        price_level = self.price_levels[int_price]
        return price_level._query_priority(order_id)

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

        self._initialize_price_level(int_price)

        # check the order id exists, and only once
        if self.order_id_count(order_id) == 0:
            raise RuntimeError(f'cannot update order with missing order_id {order_id}')
        elif self.order_id_count(order_id) > 1:
            raise RuntimeError(f'cannot update order with duplicate order_id {order_id}')

        existing_order_int_price = self._find_order_price_level_by_order_id(order_id)
        if existing_order_int_price == int_price:
            self.price_levels[existing_order_int_price].order_update(order_id, volume)
        else:
            ##existing_order: Order = self._get_order_by_order_id(order_id)
            ##existing_order.set_int_price(int_price)
            # TODO: add order_cancel_pop to return order or make order_cancel return the order
            # should it return a partial order with the int_price removed? (probably no?)
            partial_order = self.price_levels[existing_order_int_price].order_cancel(order_id)
            partial_order.set_int_price(int_price)
            self.price_levels[int_price].order_insert(partial_order)
            # TODO write a test for both of these cases

    def order_cancel(self, order_id: int):
        # check the order id exists, and only once
        if self.order_id_count(order_id) == 0:
            raise RuntimeError(f'cannot cancel order with missing order_id {order_id}')
        elif self.order_id_count(order_id) > 1:
            raise RuntimeError(f'cannot cancel order with duplicate order_id {order_id}')

        # remove matching order
        self._remove_order_by_order_id(order_id)


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


class DoubleLimitOrderBook:

    def __init__(self):
        # SIDE -> TICKER -> PRICE_LEVEL -> list of volumes
        self.double_limit_order_book = {
            'BUY': LimitOrderBook(),
            'SELL': LimitOrderBook(),
        }

    def _find_order_side_by_order_id(self, order_id: int) -> str:
        limit_order_book_buy = self.double_limit_order_book['BUY']
        limit_order_book_sell = self.double_limit_order_book['SELL']

        # TODO: consider using count here instead
        order_exists_in_buy_side = limit_order_book_buy.order_id_exists(order_id)
        order_exists_in_sell_side = limit_order_book_sell.order_id_exists(order_id)

        if order_exists_in_buy_side and not order_exists_in_sell_side:
            return 'BUY'
        elif not order_exists_in_buy_side and order_exists_in_sell_side:
            return 'SELL'

    def _find_limit_order_book_buy_order_side(self, order_side: str) -> LimitOrderBook:
        # if order_side == 'BUY':
        #     return True
        # elif order_side == 'SELL':
        #     return True
        # else:
        #     return False

        limit_order_book = None

        if order_side == 'BUY':
            limit_order_book = self.double_limit_order_book['BUY']
        elif order_side == 'SELL':
            limit_order_book = self.double_limit_order_book['SELL']

        if limit_order_book is None:
            raise RuntimeError(f'invalid order_side {order_side}')

        return limit_order_book

    def depth(self, order_side: str) -> int:
        return self.double_limit_order_book[order_side].depth()

    def depth_aggregated(self) -> int:
        return (
            sum(
                map(
                    lambda limit_order_book: limit_order_book.depth_aggregated(),
                    self.double_limit_order_book.values(),
                )
            )
        )

    def order_insert(self, order_id: int, ticker: str, order_side: str, int_price: int, volume: int):
        # limit_order_book = None

        # if order_side == 'BUY':
        #     limit_order_book = self.double_limit_order_book['BUY']
        # elif order_side == 'SELL':
        #     limit_order_book = self.double_limit_order_book['SELL']

        # if limit_order_book is None:
        #     raise RuntimeError(f'invalid order_side {order_side}')

        # TODO: _find_limit_order_book_by_order_id
        limit_order_book = self._find_limit_order_book_buy_order_side(order_side)   # TODO: use this kind of semantics in other structures

        # TODO: create PartialOrder here and set order side?
        limit_order_book.order_insert(
            order_id=order_id,
            ticker=ticker,
            order_side=order_side,
            int_price=int_price,
            volume=volume,
        )

    def order_update(self, order_id: int, int_price: int, volume: int):
        order_side = self._find_order_side_by_order_id(order_id)

        # TODO: _find_limit_order_book_by_order_id
        limit_order_book = self._find_limit_order_book_buy_order_side(order_side)
        limit_order_book.order_update(order_id, int_price, volume)

        # if order_side == 'BUY':
        #     limit_order_book_buy = self.double_limit_order_book['BUY']
        #     limit_order_book_buy.order_update(order_id, int_price, volume)
        # elif order_side == 'SELL':
        #     limit_order_book_sell = self.double_limit_order_book['SELL']
        #     limit_order_book_sell.order_update(order_id, int_price, volume)
        # else:
        #     raise RuntimeError(f'cannot update order which exists in both buy and sell side book with order_id {order_id}')

    def order_cancel(self, order_id: int):
        order_side = self._find_order_side_by_order_id(order_id)

        # TODO: _find_limit_order_book_by_order_id
        limit_order_book = self._find_limit_order_book_buy_order_side(order_side)
        limit_order_book.order_cancel(order_id)

        # if order_side == 'BUY':
        #     limit_order_book_buy = self.double_limit_order_book['BUY']
        #     limit_order_book_buy.order_cancel(order_id)
        # elif order_side == 'SELL':
        #     limit_order_book_sell = self.double_limit_order_book['SELL']
        #     limit_order_book_sell.order_cancel(order_id)
        # else:
        #     raise RuntimeError(f'cannot cancel order which exists in both buy and sell side book with order_id {order_id}')

# TODO
#if __name__ == '__main__':
#    run_all_tests()