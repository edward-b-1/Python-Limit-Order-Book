
from limit_order_book import Order
from limit_order_book import Trade
from limit_order_book import LimitOrderBook
from limit_order_book import DoubleLimitOrderBook

from limit_order_book.limit_order_book import PartialOrder
from limit_order_book.limit_order_book import PriceLevel
from limit_order_book.limit_order_book import LimitOrderBookPriceLevel

from limit_order_book.limit_order_book import parse_price_string_and_convert_to_int_price


def run_all_parse_price_string_and_convert_to_int_price_tests():

    def parse_price_string_and_convert_to_int_price_test_1():
        price_string = '12'
        int_price = parse_price_string_and_convert_to_int_price(price_string)
        assert int_price == 120000, f'parse_price_string_and_convert_to_int_price_test_1 failed: {int_price}'

    def parse_price_string_and_convert_to_int_price_test_2():
        price_string = '12.3'
        int_price = parse_price_string_and_convert_to_int_price(price_string)
        assert int_price == 123000, f'parse_price_string_and_convert_to_int_price_test_2 failed: {int_price}'

    def parse_price_string_and_convert_to_int_price_test_3():
        price_string = '12.34'
        int_price = parse_price_string_and_convert_to_int_price(price_string)
        assert int_price == 123400, f'parse_price_string_and_convert_to_int_price_test_3 failed: {int_price}'

    def parse_price_string_and_convert_to_int_price_test_4():
        price_string = '12.345'
        int_price = parse_price_string_and_convert_to_int_price(price_string)
        assert int_price == 123450, f'parse_price_string_and_convert_to_int_price_test_3 failed: {int_price}'

    def parse_price_string_and_convert_to_int_price_test_5():
        price_string = '12.3456'
        int_price = parse_price_string_and_convert_to_int_price(price_string)
        assert int_price == 123456, f'parse_price_string_and_convert_to_int_price_test_3 failed: {int_price}'

    def parse_price_string_and_convert_to_int_price_test_6():
        price_string = '12.34567'
        try:
            parse_price_string_and_convert_to_int_price(price_string)
        except ValueError as e:
            assert str(e) == f'{price_string} is not a valid string formatted price'

    def parse_price_string_and_convert_to_int_price_test_7():
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
    parse_price_string_and_convert_to_int_price_test_6()
    parse_price_string_and_convert_to_int_price_test_7()


# TODO: write the tests for match and finish the match function
# should test prices which do not match
# prices which match
# prices which cross through
# same volume
# asymetric volume (both ways)
def run_all_order_tests():

    # 1/1
    # Test no matching order for different ticker
    def run_order_test_no_match_different_ticker():
        int_price = 1000
        volume = 10

        order_1 = Order(
            order_id=1,
            ticker='PYTH',
            order_side='BUY',
            int_price=int_price,
            volume=volume,
        )

        order_2 = Order(
            order_id=2,
            ticker='JAVA',
            order_side='SELL',
            int_price=int_price,
            volume=volume,
        )

        trade = order_1.match(order_2)
        assert trade == None, f'unexpected order match'

    # 1/1
    # Test no matching order for same order_side
    def run_order_test_no_match_same_order_side():
        ticker = 'PYTH'
        order_side = 'BUY'
        int_price = 1000
        volume = 10

        order_1 = Order(
            order_id=1,
            ticker=ticker,
            order_side=order_side,
            int_price=int_price,
            volume=volume,
        )

        order_2 = Order(
            order_id=2,
            ticker=ticker,
            order_side=order_side,
            int_price=int_price,
            volume=volume,
        )

        trade = order_1.match(order_2)
        assert trade == None, f'unexpected order match'

    # 1/1
    # Test no matching order for incompatiable int_price
    def run_order_test_no_match_no_match_price():
        ticker = 'PYTH'
        volume = 10

        order_1 = Order(
            order_id=1,
            ticker=ticker,
            order_side='BUY',
            int_price=1000,
            volume=volume,
        )

        order_2 = Order(
            order_id=2,
            ticker=ticker,
            order_side='SELL',
            int_price=1010,
            volume=volume,
        )

        trade = order_1.match(order_2)
        assert trade == None, f'unexpected order match'

    # 1/3
    # Test fully matched order for compatiable int_price
    def run_order_test_full_match_same_price():
        ticker = 'PYTH'
        int_price = 1000
        volume = 10

        order_1 = Order(
            order_id=1,
            ticker=ticker,
            order_side='BUY',
            int_price=int_price,
            volume=volume,
        )

        order_2 = Order(
            order_id=2,
            ticker=ticker,
            order_side='SELL',
            int_price=int_price,
            volume=volume,
        )

        expected_trade = Trade(
            order_id_maker=1,
            order_id_taker=2,
            ticker=ticker,
            int_price=int_price,
            volume=volume
        )

        trade = order_1.match(order_2)
        assert trade == expected_trade, f'unexpected trade data or no trade'

    # 2/3
    # Test partially matched maker order for compatiable int_price
    def run_order_test_partial_maker_match_same_price():
        ticker = 'PYTH'
        int_price = 1000

        order_1 = Order(
            order_id=1,
            ticker=ticker,
            order_side='BUY',
            int_price=int_price,
            volume=20,
        )

        order_2 = Order(
            order_id=2,
            ticker=ticker,
            order_side='SELL',
            int_price=int_price,
            volume=10,
        )

        expected_trade = Trade(
            order_id_maker=1,
            order_id_taker=2,
            ticker=ticker,
            int_price=int_price,
            volume=10
        )

        trade = order_1.match(order_2)
        assert trade == expected_trade, f'unexpected trade data or no trade'
        assert order_1.volume == 10, f'unexpected maker order volume'
        assert order_2.volume == 0, f'unexpected taker order volume'

    # 3/3
    # Test partially matched taker order for compatiable int_price
    def run_order_test_partial_taker_match_same_price():
        ticker = 'PYTH'
        int_price = 1000

        order_1 = Order(
            order_id=1,
            ticker=ticker,
            order_side='BUY',
            int_price=int_price,
            volume=10,
        )

        order_2 = Order(
            order_id=2,
            ticker=ticker,
            order_side='SELL',
            int_price=int_price,
            volume=20,
        )

        expected_trade = Trade(
            order_id_maker=1,
            order_id_taker=2,
            ticker=ticker,
            int_price=int_price,
            volume=10
        )

        trade = order_1.match(order_2)
        assert trade == expected_trade, f'unexpected trade data or no trade'
        assert order_1.volume == 0, f'unexpected maker order volume'
        assert order_2.volume == 10, f'unexpected taker order volume'

    # 1/3
    # Test fully matched order for crossing taker price
    def run_order_test_full_match_crossing_taker_price():
        ticker = 'PYTH'
        volume = 10

        order_1 = Order(
            order_id=1,
            ticker=ticker,
            order_side='BUY',
            int_price=2000,
            volume=volume,
        )

        order_2 = Order(
            order_id=2,
            ticker=ticker,
            order_side='SELL',
            int_price=1000,
            volume=volume,
        )

        expected_trade = Trade(
            order_id_maker=1,
            order_id_taker=2,
            ticker=ticker,
            int_price=1000,
            volume=volume
        )

        trade = order_1.match(order_2)
        print(trade)
        assert trade == expected_trade, f'unexpected trade data or no trade'

    # 2/3
    # Test partially matched maker order for crossing taker price
    def run_order_test_partial_maker_match_crossing_taker_price():
        ticker = 'PYTH'

        order_1 = Order(
            order_id=1,
            ticker=ticker,
            order_side='BUY',
            int_price=2000,
            volume=20,
        )

        order_2 = Order(
            order_id=2,
            ticker=ticker,
            order_side='SELL',
            int_price=1000,
            volume=10,
        )

        expected_trade = Trade(
            order_id_maker=1,
            order_id_taker=2,
            ticker=ticker,
            int_price=1000,
            volume=10
        )

        trade = order_1.match(order_2)
        assert trade == expected_trade, f'unexpected trade data or no trade'
        assert order_1.volume == 10, f'unexpected maker order volume'
        assert order_2.volume == 0, f'unexpected taker order volume'

    # 3/3
    # Test partially matched taker order for crossing taker price
    def run_order_test_partial_taker_match_crossing_taker_price():
        ticker = 'PYTH'

        order_1 = Order(
            order_id=1,
            ticker=ticker,
            order_side='BUY',
            int_price=2000,
            volume=10,
        )

        order_2 = Order(
            order_id=2,
            ticker=ticker,
            order_side='SELL',
            int_price=1000,
            volume=20,
        )

        expected_trade = Trade(
            order_id_maker=1,
            order_id_taker=2,
            ticker=ticker,
            int_price=1000,
            volume=10
        )

        trade = order_1.match(order_2)
        assert trade == expected_trade, f'unexpected trade data or no trade'
        assert order_1.volume == 0, f'unexpected maker order volume'
        assert order_2.volume == 10, f'unexpected taker order volume'

    # 1/3
    # Test fully matched order for crossing taker price (reversed)
    def run_order_test_full_match_crossing_taker_price_reversed():
        ticker = 'PYTH'
        volume = 10

        order_1 = Order(
            order_id=1,
            ticker=ticker,
            order_side='SELL',
            int_price=1000,
            volume=volume,
        )

        order_2 = Order(
            order_id=2,
            ticker=ticker,
            order_side='BUY',
            int_price=2000,
            volume=volume,
        )

        expected_trade = Trade(
            order_id_maker=1,
            order_id_taker=2,
            ticker=ticker,
            int_price=2000,
            volume=volume
        )

        trade = order_1.match(order_2)
        print(trade)
        assert trade == expected_trade, f'unexpected trade data or no trade'

    # 2/3
    # Test partially matched maker order for crossing taker price (reversed)
    def run_order_test_partial_maker_match_crossing_taker_price_reversed():
        ticker = 'PYTH'

        order_1 = Order(
            order_id=1,
            ticker=ticker,
            order_side='SELL',
            int_price=1000,
            volume=20,
        )

        order_2 = Order(
            order_id=2,
            ticker=ticker,
            order_side='BUY',
            int_price=2000,
            volume=10,
        )

        expected_trade = Trade(
            order_id_maker=1,
            order_id_taker=2,
            ticker=ticker,
            int_price=2000,
            volume=10
        )

        trade = order_1.match(order_2)
        assert trade == expected_trade, f'unexpected trade data or no trade'
        assert order_1.volume == 10, f'unexpected maker order volume'
        assert order_2.volume == 0, f'unexpected taker order volume'

    # 3/3
    # Test partially matched taker order for crossing taker price (reversed)
    def run_order_test_partial_taker_match_crossing_taker_price_reversed():
        ticker = 'PYTH'

        order_1 = Order(
            order_id=1,
            ticker=ticker,
            order_side='SELL',
            int_price=1000,
            volume=10,
        )

        order_2 = Order(
            order_id=2,
            ticker=ticker,
            order_side='BUY',
            int_price=2000,
            volume=20,
        )

        expected_trade = Trade(
            order_id_maker=1,
            order_id_taker=2,
            ticker=ticker,
            int_price=2000,
            volume=10
        )

        trade = order_1.match(order_2)
        assert trade == expected_trade, f'unexpected trade data or no trade'
        assert order_1.volume == 0, f'unexpected maker order volume'
        assert order_2.volume == 10, f'unexpected taker order volume'

    run_order_test_no_match_different_ticker() # 1/1
    run_order_test_no_match_same_order_side() # 1/1
    run_order_test_no_match_no_match_price() # 1/1
    run_order_test_full_match_same_price() # 1/3
    run_order_test_partial_maker_match_same_price() # 2/3
    run_order_test_partial_taker_match_same_price() # 3/3
    run_order_test_full_match_crossing_taker_price() # 1/3
    run_order_test_partial_maker_match_crossing_taker_price() # 2/3
    run_order_test_partial_taker_match_crossing_taker_price() # 3/3
    run_order_test_full_match_crossing_taker_price_reversed() # 1/3
    run_order_test_partial_maker_match_crossing_taker_price_reversed() # 2/3
    run_order_test_partial_taker_match_crossing_taker_price_reversed() # 3/3

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

        remaining_partial_order_2 = price_level.order_cancel(order_id=2)
        assert remaining_partial_order_2 == partial_order_2, (
            f'remaining PartialOrder {remaining_partial_order_2} does not match original PartialOrder {partial_order_2}'
        )

        order_id = 2
        try:
            price_level.order_cancel(order_id)
        except RuntimeError as e:
            assert str(e) == f'cannot cancel order with missing order_id {order_id}'

        remaining_partial_order_1 = price_level.order_cancel(order_id=1)
        assert remaining_partial_order_1 == partial_order_1, (
            f'remaining PartialOrder {remaining_partial_order_1} does not match original PartialOrder {partial_order_1}'
        )

        price_level.order_update(order_id=3, volume=50)
        assert price_level._get_order_by_order_id(order_id=3).volume == 50, f'unexpected order volume'

        remaining_partial_order_3 = price_level.order_cancel(order_id=3)
        assert remaining_partial_order_3 == partial_order_3.with_volume(50), (
            f'remaining PartialOrder {remaining_partial_order_3} does not match original PartialOrder {partial_order_3}'
        )

        depth = price_level.depth()
        assert depth == 0, f'depth is not 0, depth = {depth}'

    price_level_test_1()
    #price_level_test_2()


def run_all_limit_order_book_price_level_tests():

    def limit_order_book_price_level_test_1():
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

    def limit_order_book_price_level_update_test():
        partial_order_1 = (
            PartialOrder()
            .with_order_id(100)
            .with_ticker('PYTH')
            .with_order_side('BUY')
            .with_int_price(1234)
            .with_volume(10)
        )

        # lower priority
        partial_order_2 = (
            PartialOrder()
            .with_order_id(101)
            .with_ticker('PYTH')
            .with_order_side('BUY')
            .with_int_price(1234)
            .with_volume(20)
        )

        limit_order_book_price_level = LimitOrderBookPriceLevel()

        limit_order_book_price_level.order_insert(partial_order_1)

        # todo add function to check priority
        priority = limit_order_book_price_level._query_priority(partial_order_1.order_id)
        assert priority == 0, f'unexpected order priority {priority}, expected priority {0}'


    limit_order_book_price_level_test_1()
    limit_order_book_price_level_update_test()
    #price_level_test_2()

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


def run_all_double_limit_order_book_tests():

    def check_depth_aggregated(lob: DoubleLimitOrderBook, depth: int):
        assert lob.depth_aggregated() == depth, f'unexpected depth {lob.depth_aggregated()}, expected {depth}'

    def double_limit_order_book_test_1():
        lob = DoubleLimitOrderBook()

        lob.order_insert(order_id=1, ticker='PYTH', order_side='BUY', int_price=1000, volume=10)
        # TODO: implement this
        #priority = lob.priority(order_id=1)
        #assert priority == 0, f'unexpected priority {priority} for order {1}, expected {0}'
        check_depth_aggregated(lob, 1)

        lob.order_insert(order_id=2, ticker='PYTH', order_side='BUY', int_price=1000, volume=20)
        check_depth_aggregated(lob, 2)

        lob.order_insert(order_id=3, ticker='PYTH', order_side='BUY', int_price=1020, volume=10)
        check_depth_aggregated(lob, 3)

        lob.order_insert(order_id=4, ticker='PYTH', order_side='BUY', int_price=1020, volume=20)
        check_depth_aggregated(lob, 4)

        lob.order_insert(order_id=5, ticker='PYTH', order_side='SELL', int_price=1100, volume=10)
        check_depth_aggregated(lob, 5)

        lob.order_update(order_id=1, int_price=1000, volume=5)
        check_depth_aggregated(lob, 5)

        lob.order_update(order_id=1, int_price=1010, volume=5)
        check_depth_aggregated(lob, 5)

        lob.order_update(order_id=2, int_price=1010, volume=20)
        check_depth_aggregated(lob, 5)

        lob.order_cancel(5)
        lob.order_cancel(4)
        lob.order_cancel(3)
        lob.order_cancel(2)
        lob.order_cancel(1)
        check_depth_aggregated(lob, 0)


    double_limit_order_book_test_1()


def test_limit_order_book():
    run_all_tests()


def run_all_tests():
    run_all_parse_price_string_and_convert_to_int_price_tests()
    run_all_order_tests()
    run_all_partial_order_tests()
    run_all_price_level_tests()
    run_all_limit_order_book_price_level_tests()
    run_all_limit_order_book_tests()
    run_all_double_limit_order_book_tests()


run_all_tests()
