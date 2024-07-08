
import databento

from databento_limit_order_book import Market


if __name__ == "__main__":

    data_path = "dbeq-basic-20240403.mbo.dbn.zst"
    data = databento.DBNStore.from_file(data_path)

    instrument_map = databento.common.symbology.InstrumentMap()
    instrument_map.insert_metadata(data.metadata)

    market = Market()
    for mbo in data:
        market.apply(mbo)
        if mbo.flags & databento.RecordFlags.F_LAST:
            symbol = (
                instrument_map.resolve(mbo.instrument_id, mbo.pretty_ts_recv.date())
                or ""
            )
            print(f"{symbol} Aggregated BBO | {mbo.pretty_ts_recv}")
            best_bid, best_offer = market.aggregated_bbo(mbo.instrument_id)
            print(f"    {best_offer}")
            print(f"    {best_bid}")
