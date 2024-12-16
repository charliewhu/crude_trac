import typing as t
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Grade:
    name: str


@dataclass
class Trade:
    """Base class for bids, offers, and trades."""

    grade: Grade
    location: str
    terms: t.Literal["FOB", "CIF", "DAP"]
    kb: int  # volume
    expiry: datetime  # When the order expires
    formula: str  # e.g., "Dated Brent ±", outright price
    differential: float  # Price differential
    buy_sell_ind: t.Literal["bid", "offer", "buy", "sell"]
    counterparty: str
    date: datetime  # Timestamp when the bid/offer/trade was made
    deal_date: t.Optional[datetime] = None  # When the trade was confirmed
    id: t.Optional[str] = field(default_factory=lambda: str(uuid.uuid4()))
