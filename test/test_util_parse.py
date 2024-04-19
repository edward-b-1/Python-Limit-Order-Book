
from limit_order_book.util_parse import parse_price_string_and_convert_to_int_price


def test_run_all_parse_price_string_and_convert_to_int_price_tests():

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
