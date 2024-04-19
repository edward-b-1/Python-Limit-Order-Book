
from limit_order_book import Order
from limit_order_book import Trade
from limit_order_book import LimitOrderBook
from limit_order_book import DoubleLimitOrderBook

from limit_order_book.limit_order_book import PartialOrder
from limit_order_book.limit_order_book import PriceLevel
from limit_order_book.limit_order_book import LimitOrderBookPriceLevel

from limit_order_book.util_parse import parse_price_string_and_convert_to_int_price



def test_run_all_limit_order_book_price_level_tests():

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

def test_run_all_limit_order_book_tests():

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

    def test_order_cancel():
        limit_order_book_price_level = LimitOrderBook()
        limit_order_book_price_level.order_insert(1, 'PYTH', 'BUY', 1000, 20)
        removed_order = limit_order_book_price_level.order_cancel(1)
        expected_order = PartialOrder(
            order_id=1,
            ticker='PYTH',
            order_side='BUY',
            int_price=1000,
            volume=20,
        )
        assert removed_order == expected_order, f'removed order data does not match expected order data'


    price_level_test_1()
    test_order_cancel()


