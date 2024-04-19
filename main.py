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


if __name__ == '__main__':

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
