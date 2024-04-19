



def test_run_all_double_limit_order_book_tests():

    from limit_order_book import DoubleLimitOrderBook

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
