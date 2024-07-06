'''
Implement the same orderbook as the one in the Databento example. We can perhaps
use this data structure to produce sensible messages to drive the Limit Order
Book.
'''

from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field
import databento as db
from databento_dbn import FIXED_PRICE_SCALE, UNDEF_PRICE, BidAskPair
from sortedcontainers import SortedDict


@dataclass
class Order:
    id: int
    side: str
    price: int
    size: int
    ts_event: int
    is_tob: bool = field(default=False)


@dataclass
class LevelOrders:
    price: int
    orders: list[Order] = field(default_factory=list, compare=False)

    def __bool__(self) -> bool:
        return bool(self.orders)

    @property
    def level(self) -> PriceLevel:
        return PriceLevel(
            price=self.price,
            count=sum(1 for o in self.orders if not o.is_tob),
            size=sum(o.size for o in self.orders),
        )


@dataclass
class PriceLevel:
    price: int
    size: int = 0
    count: int = 0

    def __str__(self) -> str:
        price = self.price / FIXED_PRICE_SCALE
        return f"{self.size:4} @ {price:6.2f} | {self.count:2} order(s)"


@dataclass
class Book:
    orders_by_id: dict[int, Order] = field(default_factory=dict)
    offers: SortedDict[int, LevelOrders] = field(default_factory=SortedDict)
    bids: SortedDict[int, LevelOrders] = field(default_factory=SortedDict)

    def bbo(self) -> tuple[PriceLevel | None, PriceLevel | None]:
        return self.get_bid_level(), self.get_ask_level()

    def get_bid_level(self, idx: int = 0) -> PriceLevel | None:
        if self.bids and len(self.bids) > idx:
            # Reverse for bids to get highest prices first
            return self.bids.peekitem(-(idx + 1))[1].level
        return None

    def get_ask_level(self, idx: int = 0) -> PriceLevel | None:
        if self.offers and len(self.offers) > idx:
            return self.offers.peekitem(idx)[1].level
        return None

    def get_bid_level_by_px(self, px: int) -> PriceLevel | None:
        try:
            return self._get_level(px, "B").level
        except KeyError:
            return None

    def get_ask_level_by_px(self, px: int) -> PriceLevel | None:
        try:
            return self._get_level(px, "A").level
        except KeyError:
            return None

    def get_snapshot(self, level_count: int = 1) -> list[BidAskPair]:
        snapshots = []
        for level in range(level_count):
            ba_pair = BidAskPair()
            bid = self.get_bid_level(level)
            if bid:
                ba_pair.bid_px = bid.price
                ba_pair.bid_sz = bid.size
                ba_pair.bid_ct = bid.count
            ask = self.get_ask_level(level)
            if ask:
                ba_pair.ask_px = ask.price
                ba_pair.ask_sz = ask.size
                ba_pair.ask_ct = ask.count
            snapshots.append(ba_pair)
        return snapshots

    def apply(
        self,
        ts_event: int,
        action: str,
        side: str,
        order_id: int,
        price: int,
        size: int,
        flags: db.RecordFlags,
    ) -> None:
        # Trade or Fill: no change
        if action == "T" or action == "F":
            return
        # Clear book: remove all resting orders
        if action == "R":
            self._clear()
            return
        # side=N is only valid with Trade, Fill, and Clear actions
        assert side == "A" or side == "B"
        # UNDEF_PRICE indicates the book level should be removed
        if price == UNDEF_PRICE and flags & db.RecordFlags.F_TOB:
            self._side_levels(side).clear()
            return
        # Add: insert a new order
        if action == "A":
            self._add(ts_event, side, order_id, price, size, flags)
        # Cancel: partially or fully cancel some size from a resting order
        elif action == "C":
            self._cancel(side, order_id, price, size)
        # Modify: change the price and/or size of a resting order
        elif action == "M":
            self._modify(ts_event, side, order_id, price, size, flags)
        else:
            raise ValueError(f"Unknown {action =}")

    def _clear(self):
        self.orders_by_id.clear()
        self.offers.clear()
        self.bids.clear()

    def _add(
        self,
        ts_event: int,
        side: str,
        order_id: int,
        price: int,
        size: int,
        flags: db.RecordFlags,
    ):
        order = Order(
            order_id,
            side,
            price,
            size,
            ts_event,
            is_tob=bool(flags & db.RecordFlags.F_TOB),
        )
        if order.is_tob:
            levels = self._side_levels(side)
            levels.clear()
            levels[price] = LevelOrders(price=price, orders=[order])
        else:
            level = self._get_or_insert_level(price, side)
            assert order_id not in self.orders_by_id
            self.orders_by_id[order_id] = order
            level.orders.append(order)

    def _cancel(
        self,
        side: str,
        order_id: int,
        price: int,
        size: int,
    ):
        order = self.orders_by_id[order_id]
        level = self._get_level(price, side)
        assert order.size >= size
        order.size -= size
        # If the full size is cancelled, remove the order from the book
        if order.size == 0:
            self.orders_by_id.pop(order_id)
            level.orders.remove(order)
            # If the level is now empty, remove it from the book
            if not level:
                self._remove_level(price, side)

    def _modify(
        self,
        ts_event: int,
        side: str,
        order_id: int,
        price: int,
        size: int,
        flags: db.RecordFlags,
    ):

        order = self.orders_by_id.get(order_id)
        if order is None:
            # If order not found, treat it as an add
            self._add(ts_event, side, order_id, price, size, flags)
            return
        assert order.side == side, f"Order {order} changed side to {side}"
        prev_level = self._get_level(order.price, side)
        if order.price != price:
            prev_level.orders.remove(order)
            if not prev_level:
                self._remove_level(order.price, side)
            level = self._get_or_insert_level(price, side)
            level.orders.append(order)
        else:
            level = prev_level
        # The order loses its priority if the price changes or the size increases
        if order.price != price or order.size < size:
            order.ts_event = ts_event
            level.orders.remove(order)
            level.orders.append(order)
        order.size = size
        order.price = price

    def _side_levels(self, side: str) -> SortedDict:
        if side == "A":
            return self.offers
        if side == "B":
            return self.bids
        raise ValueError(f"Invalid {side =}")

    def _get_level(self, price: int, side: str) -> LevelOrders:
        levels = self._side_levels(side)
        if price not in levels:
            raise KeyError(f"No price level found for {price =} and {side =}")
        return levels[price]

    def _get_or_insert_level(self, price: int, side: str) -> LevelOrders:
        levels = self._side_levels(side)
        if price in levels:
            return levels[price]
        level = LevelOrders(price=price)
        levels[price] = level
        return level

    def _remove_level(self, price: int, side: str):
        levels = self._side_levels(side)
        levels.pop(price)


@dataclass
class Market:
    books: defaultdict[int, defaultdict[int, Book]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(Book)),
    )

    def get_books_by_pub(self, instrument_id: int) -> defaultdict[int, Book]:
        return self.books[instrument_id]

    def get_book(self, instrument_id: int, publisher_id: int) -> Book:
        return self.books[instrument_id][publisher_id]

    def bbo(
        self,
        instrument_id: int,
        publisher_id: int,
    ) -> tuple[PriceLevel | None, PriceLevel | None]:
        return self.books[instrument_id][publisher_id].bbo()

    def aggregated_bbo(
        self,
        instrument_id: int,
    ) -> tuple[PriceLevel | None, PriceLevel | None]:
        agg_bbo: list[PriceLevel | None] = [None, None]
        # max for bids, min for asks
        for idx, reducer in [(0, max), (1, min)]:
            all_best = [b.bbo()[idx] for b in self.books[instrument_id].values()]
            all_best = [b for b in all_best if b]
            if not all_best:
                continue
            best_price = reducer(b.price for b in all_best)
            best = [b for b in all_best if b.price == best_price]
            agg_bbo[idx] = PriceLevel(
                price=best_price,
                size=sum(b.size for b in best),
                count=sum(b.count for b in best),
            )
        return tuple(agg_bbo)

    def apply(self, mbo: db.MBOMsg):
        book = self.books[mbo.instrument_id][mbo.publisher_id]
        book.apply(
            ts_event=mbo.ts_event,
            action=mbo.action,
            side=mbo.side,
            order_id=mbo.order_id,
            price=mbo.price,
            size=mbo.size,
            flags=mbo.flags,
        )
