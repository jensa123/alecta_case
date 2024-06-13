"""Definitions of types used to represent positions."""

__all__: list[str] = ["Position"]

from modules.types.base_entity import BaseEntity
from .portfolio import Portfolio
from .instruments import *
from datetime import date


class Position(BaseEntity):
    """Represents a position / holding in an instrument.

    A position is comprised of a quantity in an instrument, on a given date.
    """

    def __init__(self, id_: int) -> None:
        super().__init__(id_)

    @classmethod
    def create(
        cls,
        id_: int,
        portfolio: Portfolio,
        instrument: Instrument,
        position_date: date,
        quantity: float | int,
    ):
        pos = cls(id_)
        pos.portfolio = portfolio
        pos.instrument = instrument
        pos.position_date = position_date
        pos.quantity = quantity
        return pos

    @property
    def portfolio(self) -> Portfolio:
        """The portfolio of the position."""
        return self._portfolio

    @portfolio.setter
    def portfolio(self, value: Portfolio) -> None:
        if not isinstance(value, Portfolio):
            raise TypeError
        self._portfolio = value

    @property
    def instrument(self) -> Instrument:
        """The instrument of the position."""
        return self._instrument

    @instrument.setter
    def instrument(self, value: Instrument) -> None:
        if not isinstance(value, Instrument):
            raise TypeError
        self._instrument = value

    @property
    def quantity(self) -> float:
        """The quantity of the position."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: float) -> None:
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError
        self._quantity = value

    @property
    def position_date(self) -> date:
        """The date of the position."""
        return self._position_date

    @position_date.setter
    def position_date(self, value: date) -> None:
        if not isinstance(value, date):
            raise TypeError
        self._position_date = value

    def market_value(self, price) -> float:
        """Computes and returns the market value of the position."""
        return self.instrument.market_value(price, self.quantity)
