import typing as t
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Trade:
    """Base class for bids, offers, and trades."""

    grade: str
    location: str
    kb: int  # volume
    expiry: datetime  # When the order expires
    formula: str  # e.g., "Dated Brent ±", outright price
    differential: float  # Price differential
    date: datetime  # Timestamp when the bid/offer/trade was made
    deal_date: datetime  # When the trade was confirmed
    buy_sell_ind: t.Literal["bid", "offer", "buy", "sell"]
    counterparty: str
    id: t.Optional[str] = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class CrudeGrade:
    """Represents a specific crude grade and its associated data."""

    name: str
    trades: list[Trade] = field(default_factory=list)

    def add_trade(self, trade: Trade):
        """Add a trade to the list."""
        self.trades.append(trade)

    def get_latest_order(self) -> t.Optional[Trade]:
        """Retrieve the most recent bid/offer."""
        return max(self.trades, key=lambda t: t.date, default=None)

    def get_latest_trade(self) -> t.Optional[Trade]:
        """Retrieve the most recent confirmed trade."""
        return max(self.trades, key=lambda t: t.deal_date, default=None)

    def get_best_bid(self) -> t.Optional[Trade]:
        """Retrieve the highest bid."""
        return max(
            [trade for trade in self.trades if trade.buy_sell_ind == "bid"],
            key=lambda b: b.differential,
            default=None,
        )

    def get_best_offer(self) -> t.Optional[Trade]:
        """Retrieve the lowest offer."""
        return min(
            [trade for trade in self.trades if trade.buy_sell_ind == "offer"],
            key=lambda o: o.differential,
            default=None,
        )

    def get_present_value(self) -> t.Optional[float]:
        """
        Determine the present value based on:
        - Most recent trade (preferred).
        - Best bid if no trades exist.
        - Best offer if no bids or trades exist.
        """
        latest_trade = self.get_latest_trade()
        if latest_trade:
            return latest_trade.differential

        best_bid = self.get_best_bid()
        if best_bid:
            return best_bid.differential

        best_offer = self.get_best_offer()
        if best_offer:
            return best_offer.differential

        return None  # No data available to determine present value


@dataclass
class CrudeMarket:
    """Manages all crude grades and their market data."""

    grades: list[CrudeGrade] = field(default_factory=list)

    def add_grade(self, crude_grade: CrudeGrade):
        """Add a new crude grade to the market."""
        self.grades.append(crude_grade)

    def find_grade(self, name: str) -> t.Optional[CrudeGrade]:
        """Retrieve a crude grade by name."""
        return next((grade for grade in self.grades if grade.name == name), None)

    def get_all_present_values(self) -> dict:
        """
        Retrieve the present values of all crude grades.
        Returns:
            dict: {crude_grade_name: present_value}
        """
        return {grade.name: grade.get_present_value() for grade in self.grades}
