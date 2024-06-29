
import pandas


def compare_rows(index: int, last_row: pandas.DataFrame, row: pandas.DataFrame):

    action = 'action'

    last_row_action = last_row[action]
    row_action = row[action]

    if not (last_row_action == 'F' and row_action == 'C'):
        return False

    relevant_columns = [
        'rtype',
        'publisher_id',
        'instrument_id',
        'side',
        'price',
        'size',
        'channel_id',
        'order_id',
        # flags?
        'sequence',
        'symbol',
    ]

    last_row_relevant_columns = last_row[relevant_columns]
    row_relevant_columns = row[relevant_columns]

    return row_relevant_columns.equals(last_row_relevant_columns)