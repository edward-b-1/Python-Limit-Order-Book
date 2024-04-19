
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
