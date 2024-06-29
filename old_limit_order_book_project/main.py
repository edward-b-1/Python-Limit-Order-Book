#!/bin/python3

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


import os

from old_limit_order_book.trade import Trade
from old_limit_order_book.double_limit_order_book import DoubleLimitOrderBook

from util_io.util_parse import parse_price_string_and_convert_to_int_price
from util_io.util_encode import encode_trades

# Examples:
#
#  INSERT,<order_id>,<symbol>,<side>,<price>,<volume>
#  e.g. INSERT,4,FFLY,BUY,23.45,12
#
#  UPDATE,<order_id>,<price>,<volume>
#  e.g. UPDATE,4,23.12,11
#
#  CANCEL,<order_id>
#  e.g. CANCEL,4


def runMatchingEngine(operations: list[str]) -> list[str]:
    '''
    Parameters:

        - operations: list of string operations

    Returns:

        - list representing trades and order book state
    '''

    # TODO ast parser

    lob = DoubleLimitOrderBook()
    trades = []

    for operation in operations:
        split_operation = operation.split(',')
        assert len(split_operation) > 1, 'invalid operation'

        operation_opcode = split_operation[0]
        order_id_str = split_operation[1]
        order_id = int(order_id_str)

        if operation_opcode == 'INSERT':
            assert len(split_operation) == 6, 'invalid INSERT syntax'
            ticker = split_operation[2]
            order_side = split_operation[3]
            price_str = split_operation[4]
            volume = split_operation[5]

            int_price = parse_price_string_and_convert_to_int_price(price_str)
            volume = int(volume)

            trade_list = lob.order_insert(order_id, ticker, order_side, int_price, volume)
            trades += trade_list
        elif operation_opcode == 'UPDATE':
            assert len(split_operation) == 4, 'invalid UPDATE syntax'
            price_str = split_operation[2]
            volume = split_operation[3]
            volume = int(volume)

            int_price = parse_price_string_and_convert_to_int_price(price_str)

            trade_list = lob.order_update(order_id, int_price, volume)
            trades += trade_list
        elif operation_opcode == 'CANCEL':
            assert len(split_operation) == 2, 'invalid CANCEL syntax'

            lob.order_cancel(order_id)
        else:
            raise ValueError(f'invalid opcode: {operation_opcode}')

    return_data = []
    if len(trades) > 0:
        encoded_trades = encode_trades(trades)
        return_data = encoded_trades

    order_book_str = str(lob)
    for order_book_str in order_book_str.split('\n'):
        return_data.append(order_book_str)

    return return_data


if __name__ == '__main__':

    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    operations_count = int(input().strip())
    operations = []

    for _ in range(operations_count):
        operations_item = input()
        operations.append(operations_item)

    print(operations)

    result = runMatchingEngine(operations)

    fptr.write('\n'.join(result))
    fptr.write('\n')

    fptr.close()
