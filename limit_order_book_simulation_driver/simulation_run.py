
import pandas

from old_limit_order_book.order_side import OrderSide
from old_limit_order_book.double_limit_order_book import DoubleLimitOrderBook

# mbo_data/xnas-itch-20240105.mbo.dbn.trades.csv
# mbo_data/xnas-itch-20240105.mbo.dbn.orders.csv


def main():

    lob = DoubleLimitOrderBook()

    df_trades = pandas.read_csv(
        #'xnas-itch-20240105.mbo.dbn.orders.csv',
        'order_id_261575.csv',
    )

    trades_output_list = []

    for index, row in df_trades.iterrows():
        instrument_id = row['instrument_id']
        order_id = row['order_id']
        action = row['action']
        side = row['side']
        price = row['price']
        size = row['size']

        if action == 'T':
            continue
        elif action == 'F':
            continue

        ticker = str(instrument_id)
        order_side = None
        if side == 'B':
            order_side = OrderSide.BUY
        elif side == 'A':
            order_side = OrderSide.SELL
        else:
            print(row)
            raise RuntimeError(f'order_side={order_side} not recognized')

        trades = []

        if int(order_id) == 261575:
            print(row)

        if action == 'A':
            trades = lob.order_insert(order_id=order_id, ticker=ticker, order_side=order_side, int_price=price, volume=size)
        elif action == 'M':
            trades = lob.order_update(order_id=order_id, int_price=price, volume=size)
        elif action == 'C':
            lob.order_cancel(order_id=order_id)
        else:
            raise RuntimeError(f'action={action} not recognized')

        for trade in trades:
            trades_output_list.append(
                {
                    'order_id': trade.order_id_maker,
                    'instrument_id': int(trade.ticker),
                    'action': 'T',
                    'side': 'N',
                    'price': trade.int_price,
                    'size': trade.volume,
                }
            )
        trades = []

    df_trades_output = pandas.DataFrame(trades_output_list)

    print(f'simulated trades:')
    print(df_trades_output)
    print(f'')
    print(f'expected trades:')
    print(df_trades[['order_id', 'instrument_id', 'action', 'side', 'price', 'size']])
    print(f'')


if __name__ == '__main__':
    main()
