
import pandas
import databento

from lib_financial_exchange.limit_order_book.limit_order_book import LimitOrderBook
from lib_financial_exchange.financial_exchange_types import OrderInsertMessage
from lib_financial_exchange.financial_exchange_types import Trade
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume

# mbo_data/xnas-itch-20240105.mbo.dbn.trades.csv
# mbo_data/xnas-itch-20240105.mbo.dbn.orders.csv

from typeguard import typechecked


def other_side(side: str) -> str:
    if side == 'B':
        return 'A'
    if side == 'A':
        return 'B'
    raise RuntimeError(f'other_side: side={side}, not A or B')

def databento_order_side_to_lob_order_side(side: str) -> str|None:
    if side == 'A':
        return 'SELL'
    if side == 'B':
        return 'BUY'
    if side == 'N':
        return None
    raise RuntimeError(f'databento_order_side_to_lob_order_side: side={side} unrecognized')


def check_ts_recv_next_two_rows(row, row_1, row_2):
    ts_recv = row['ts_recv']
    ts_recv_1 = row_1['ts_recv']
    ts_recv_2 = row_2['ts_recv']
    if ts_recv == ts_recv_1 and ts_recv == ts_recv_2:
        pass
    else:
        action_1 = row_1['action']
        action_2 = row_2['action']
        raise RuntimeError(f'Trade followed by {action_1}, {action_2} ts_recv unexpected values {ts_recv}, {ts_recv_1}, {ts_recv_2}')

def check_ts_event_next_two_rows(row, row_1, row_2):
    ts_event = row['ts_event']
    ts_event_1 = row_1['ts_event']
    ts_event_2 = row_2['ts_event']
    if ts_event == ts_event_1 and ts_event == ts_event_2:
        pass
    else:
        action_1 = row_1['action']
        action_2 = row_2['action']
        raise RuntimeError(f'Trade followed by {action_1}, {action_2} ts_event unexpected values {ts_event}, {ts_event_1}, {ts_event_2}')

def check_rtype_next_two_rows(row, row_1, row_2):
    rtype = row['rtype']
    rtype_1 = row_1['rtype']
    rtype_2 = row_2['rtype']
    if rtype == rtype_1 and rtype == rtype_2:
        pass
    else:
        action_1 = row_1['action']
        action_2 = row_2['action']
        raise RuntimeError(f'Trade followed by {action_1}, {action_2} rtype unexpected values {rtype}, {rtype_1}, {rtype_2}')

def check_publisher_id_next_two_rows(row, row_1, row_2):
    publisher_id = row['publisher_id']
    publisher_id_1 = row['publisher_id']
    publisher_id_2 = row['publisher_id']
    if publisher_id == publisher_id_1 and publisher_id == publisher_id_2:
        pass
    else:
        action_1 = row_1['action']
        action_2 = row_2['action']
        raise RuntimeError(f'Trade followed by {action_1}, {action_2} publisher_id unexpected values {publisher_id}, {publisher_id_1}, {publisher_id_2}')

def check_instrument_id_next_two_rows(row, row_1, row_2):
    instrument_id = row['instrument_id']
    instrument_id_1 = row['instrument_id']
    instrument_id_2 = row['instrument_id']
    if instrument_id == instrument_id_1 and instrument_id == instrument_id_2:
        pass
    else:
        action_1 = row_1['action']
        action_2 = row_2['action']
        raise RuntimeError(f'Trade followed by {action_1}, {action_2} instrument_id unexpected values {instrument_id}, {instrument_id_1}, {instrument_id_2}')

def check_side_next_two_rows(row, row_1, row_2):
    side = row['side']
    side_1 = row_1['side']
    side_2 = row_2['side']
    trade_other_side = other_side(side)
    if trade_other_side == side_1 and trade_other_side == side_2:
        pass
    else:
        action_1 = row_1['action']
        action_2 = row_2['action']
        raise RuntimeError(f'Trade followed by {action_1}, {action_2} side unexpected values {side}, {side_1}, {side_2}')

def check_size_next_two_rows(row, row_1, row_2):
    size = row['size']
    size_1 = row['size']
    size_2 = row['size']
    if size == size_1 and size == size_2:
        pass
    else:
        action_1 = row_1['action']
        action_2 = row_2['action']
        raise RuntimeError(f'Trade followed by {action_1}, {action_2} size unexpected values {size}, {size_1}, {size_2}')

def check_channel_id_next_two_rows(row, row_1, row_2):
    channel_id = row['channel_id']
    channel_id_1 = row['channel_id']
    channel_id_2 = row['channel_id']
    if channel_id == channel_id_1 and channel_id == channel_id_2:
        pass
    else:
        action_1 = row_1['action']
        action_2 = row_2['action']
        raise RuntimeError(f'Trade followed by {action_1}, {action_2} channel_id unexpected values {channel_id}, {channel_id_1}, {channel_id_2}')

def check_order_id_next_two_rows(row_1, row_2):
    order_id_1 = row_1['order_id']
    order_id_2 = row_2['order_id']
    if order_id_1 != order_id_2:
        action_1 = row_1['action']
        action_2 = row_2['action']
        raise RuntimeError(f'Trade followed by {action_1}, {action_2} order_id unexpected values {order_id_1}, {order_id_2}')

def check_sequence_next_two_rows(row, row_1, row_2):
    sequence = row['sequence']
    sequence_1 = row_1['sequence']
    sequence_2 = row_2['sequence']
    if sequence == sequence_1 and sequence == sequence_2:
        pass
    else:
        action_1 = row_1['action']
        action_2 = row_2['action']
        raise RuntimeError(f'Trade followed by {action_1}, {action_2} sequence unexpected values {sequence}, {sequence_1}, {sequence_2}')

def check_symbol_next_two_rows(row, row_1, row_2):
    symbol = row['symbol']
    symbol_1 = row_1['symbol']
    symbol_2 = row_2['symbol']
    if symbol == symbol_1 and symbol == symbol_2:
        pass
    else:
        action_1 = row_1['action']
        action_2 = row_2['action']
        raise RuntimeError(f'Trade followed by {action_1}, {action_2} symbol unexpected values {symbol}, {symbol_1}, {symbol_2}')


@typechecked
class OrderIdMap():
    def __init__(self) -> None:
        self.external_order_id_to_internal_order_id = {}
        self.internal_order_id_to_external_order_id = {}

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        slist = []
        for key, value in self.external_order_id_to_internal_order_id.items():
            slist.append(f'{key} -> {value}')
        return '\n'.join(slist)

    def add(self, external_order_id: int, internal_order_id: int):
        if external_order_id in self.external_order_id_to_internal_order_id:
            raise RuntimeError(f'duplicate external_order_id={external_order_id}')
        if internal_order_id in self.internal_order_id_to_external_order_id:
            raise RuntimeError(f'duplicate internal_order_id={internal_order_id}')
        self.external_order_id_to_internal_order_id[external_order_id] = internal_order_id
        self.internal_order_id_to_external_order_id[internal_order_id] = external_order_id

    def convert_internal_order_id_to_external_order_id(self, internal_order_id: int):
        if not internal_order_id in self.internal_order_id_to_external_order_id:
            raise RuntimeError(f'missing internal_order_id={internal_order_id}')
        return self.internal_order_id_to_external_order_id[internal_order_id]

    def convert_external_order_id_to_internal_order_id(self, external_order_id: int):
        if not external_order_id in self.external_order_id_to_internal_order_id:
            raise RuntimeError(f'missing external_order_id={external_order_id}')
        return self.external_order_id_to_internal_order_id[external_order_id]


def get_path(ticker, filename=None):
    ticker = 'nvda'
    #filename = 'xnas-itch-20240105.mbo.dbn.zst'
    return f'/databento/data/mbo/{ticker}/XNAS-20240622-WPPRESG4BH/{filename}'


def convert_price_to_int_price(price: float) -> int:
    return int(round(price * 1000))


def main():

    lob = LimitOrderBook()

    order_id_map = OrderIdMap()

    ticker = 'NVDA'
    filename = 'xnas-itch-20240105.mbo.dbn.zst'
    full_path = get_path(ticker, filename)

    stored_data = databento.DBNStore.from_file(full_path)
    df_trades: pandas.DataFrame = stored_data.to_df().reset_index()

    #df_trades = df_trades.loc[df_trades['price'] == 480.3].reset_index(drop=True)

    df_trades.iloc[0:100].to_csv('df_trades_tmp.csv')

    #print(df_trades.loc[df_trades['order_id'] == 174323])
    for i in range(10):
        print(df_trades.iloc[50*i:50*(i+1)])

    # df_trades = pandas.read_csv(
    #     f'/databento/data/mbo/{ticker}/XNAS-20240622-WPPRESG4BH/{filename}',
    #     #'xnas-itch-20240105.mbo.dbn.orders.csv',
    #     #'order_id_261575.csv',
    # )

    trades_output_list = []

    f_tape_orders = open('tape_orders.txt', 'w')
    f_tape_trades = open('tape_trades.txt', 'w')

    #for index, row in df_trades.iterrows():
    # index_range = list(range(len(df_trades)))
    # for index in index_range:
    index = None
    while index is None or (index + 1) < len(df_trades):
        if index is None:
            index = 0
        else:
            index += 1

        print(f'@ index={index}')
        print(lob.top_of_book(ticker=Ticker('NVDA')))
        row = df_trades.iloc[index]

        instrument_id = row['instrument_id']
        action = row['action']
        side = row['side']
        order_side = databento_order_side_to_lob_order_side(side)
        price = row['price']
        int_price = convert_price_to_int_price(price)
        size = row['size']
        order_id = row['order_id']
        sequence = row['sequence']
        symbol = row['symbol']

        if action == 'T':
            index_1 = index + 1
            index_2 = index + 2
            row_1 = df_trades.iloc[index_1]
            row_2 = df_trades.iloc[index_2]
            action_1 = row_1['action']
            action_2 = row_2['action']

            if action_1 == 'F' and action_2 == 'C':
                check_ts_recv_next_two_rows(row, row_1, row_2)
                check_ts_event_next_two_rows(row, row_1, row_2)
                check_rtype_next_two_rows(row, row_1, row_2)
                check_publisher_id_next_two_rows(row, row_1, row_2)
                check_instrument_id_next_two_rows(row, row_1, row_2)
                check_side_next_two_rows(row, row_1, row_2)
                #check_price_next_two_rows
                check_size_next_two_rows(row, row_1, row_2)
                check_channel_id_next_two_rows(row, row_1, row_2)
                assert order_id == 0, f'Trade order_id is not 0'
                check_order_id_next_two_rows(row_1, row_2)
                order_id_maker = row_1['order_id']
                check_sequence_next_two_rows(row, row_1, row_2)
                check_symbol_next_two_rows(row, row_1, row_2)
                # TODO
                #check_symbol()

                assert order_side is not None, f'order side is None'

                lob_order = OrderInsertMessage(
                    ticker=Ticker(symbol),
                    order_side=OrderSide(order_side),
                    int_price=IntPrice(price),
                    volume=Volume(size),
                )
                print(f'insert order: {lob_order}')
                TICKER = lob_order.to_ticker().to_str()
                ORDER_SIDE = str(lob_order.to_order_side())
                INT_PRICE = lob_order.to_int_price().to_int()
                VOLUME = lob_order.to_volume().to_int()
                f_tape_orders.write(f'ORDER_ADD: {TICKER} {ORDER_SIDE} {INT_PRICE} {VOLUME}')
                (lob_order_id, lob_trades) = lob.order_insert(lob_order)
                # print(f'top of book (2):')
                # print(lob.top_of_book(ticker=Ticker('NVDA')))

                # this should be done elsewhere
                #order_id_map.add(external_order_id=lob_order_id, internal_order_id=lob_order_id)

                if len(lob_trades) < 1:
                    raise RuntimeError(f'no trades')

                # TODO: to reconstruct the original orders, I may have to aggregate several Trades
                # (interpreted as Orders) together
                if len(lob_trades) > 1:
                    print(f'blown up @ index={index}')
                    print(order_id_map)
                    for trade in lob_trades:
                        print(trade)
                    raise RuntimeError(f'multiple trades')

                trade = lob_trades[0]

                expected_trade = Trade(
                    # the order sent to the order book is a taker order, the order book returns a newly generated order id
                    order_id_maker=OrderId(order_id_map.convert_external_order_id_to_internal_order_id(int(order_id_maker))), # this is a bit pointless [still true?]
                    order_id_taker=lob_order_id, # taker orders in the input data have an order id of 0
                    ticker=Ticker(symbol), # we know what the ticker is because the trade tells us
                    int_price=IntPrice(price), # we know what price the order was matched at, because the trade tells us this value
                    volume=Volume(size), # we know what the volume was because the trade tell us this value
                )
                if expected_trade != trade:
                    print(f'blown up @ index={index}')
                assert expected_trade == trade, f'trade does not match expected trade\n{trade}\n{expected_trade}'

                #lob.order_cancel_partial(expected_trade._order_id_maker, volume=Volume(size))

                #print(f'next: {index}')
                #print(next(index_range))
                #print(next(index_range))
                index += 2
            else:
                #print(df_trades.iloc[index:index+10])
                #raise RuntimeError(f'Trade followed by {action_1}, {action_2} not Fill, Cancel')
                # skip this row
                if order_side is not None:
                    raise RuntimeError(f'Trade followed by {action_1}, {action_2}, not Fill, Cancel and order_side={order_side}')
                else:
                    continue

        elif action == 'F':
            raise RuntimeError(f'unhandled Fill index={index}, sequence={sequence}')
        elif action == 'C':
            '''
            A cancel for the full remaining volume has the same semantics as the
            `LimitOrderBook.order_cancel()` function.

            Some cancel messages are expected to cancel only part of the remaining
            order. These have the same semantics as
            `LimitOrderBook.order_cancel_partial()`.
            '''
            order_id = row['order_id']
            size = row['size']
            order_id_maker = OrderId(order_id_map.convert_external_order_id_to_internal_order_id(int(order_id)))
            volume = Volume(size)
            print(f'CANCEL {order_id}, {volume}')
            ORDER_ID = order_id
            f_tape_orders.write(f'ORDER_CANCEL: {ORDER_ID}')
            lob.order_cancel_partial(order_id_maker, volume)

        elif action == 'A':
            lob_order = OrderInsertMessage(
                ticker=Ticker(symbol),
                order_side=OrderSide(order_side),
                int_price=IntPrice(price),
                volume=Volume(size),
            )
            # print(f'the top of book is')
            # print(lob.top_of_book(ticker=Ticker('NVDA')))
            print(f'ADD: {lob_order}')
            ORDER_ID = order_id
            TICKER = lob_order.to_ticker().to_str()
            ORDER_SIDE = str(lob_order.to_order_side())
            INT_PRICE = lob_order.to_int_price().to_int()
            VOLUME = lob_order.to_volume().to_int()
            f_tape_orders.write(f'ORDER_ADD: {ORDER_ID} {TICKER} {ORDER_SIDE} {INT_PRICE} {VOLUME}')
            assert order_id != 0
            (lob_order_id, lob_trades) = lob.order_insert(lob_order)
            if len(lob_trades) != 0:
                print(f'blown up @ index={index}')
            assert len(lob_trades) == 0, f'unexpected Trades generated by Add'

            order_id_map.add(external_order_id=int(order_id), internal_order_id=lob_order_id.to_int())

        elif action == 'M':
            raise RuntimeError(f'unhandled Modify index={index}, sequence={sequence}')
        else:
            raise RuntimeError(f'unhandled {action} index={index}, sequence={sequence}')

    #     ticker = str(instrument_id)
    #     order_side = None
    #     if side == 'B':
    #         order_side = OrderSide.BUY
    #     elif side == 'A':
    #         order_side = OrderSide.SELL
    #     else:
    #         print(row)
    #         raise RuntimeError(f'order_side={order_side} not recognized')

    #     trades = []

    #     if int(order_id) == 261575:
    #         print(row)

    #     if action == 'A':
    #         trades = lob.order_insert(order_id=order_id, ticker=ticker, order_side=order_side, int_price=price, volume=size)
    #     elif action == 'M':
    #         trades = lob.order_update(order_id=order_id, int_price=price, volume=size)
    #     elif action == 'C':
    #         lob.order_cancel(order_id=order_id)
    #     else:
    #         raise RuntimeError(f'action={action} not recognized')

    #     for trade in trades:
    #         trades_output_list.append(
    #             {
    #                 'order_id': trade.order_id_maker,
    #                 'instrument_id': int(trade.ticker),
    #                 'action': 'T',
    #                 'side': 'N',
    #                 'price': trade.int_price,
    #                 'size': trade.volume,
    #             }
    #         )
    #     trades = []

    # df_trades_output = pandas.DataFrame(trades_output_list)

    # print(f'simulated trades:')
    # print(df_trades_output)
    # print(f'')
    # print(f'expected trades:')
    # print(df_trades[['order_id', 'instrument_id', 'action', 'side', 'price', 'size']])
    # print(f'')


if __name__ == '__main__':
    main()
