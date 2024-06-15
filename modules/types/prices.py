"""Contains types representing prices."""

__all__: list[str] = ["Price"]

from .base_entity import BaseEntity
from datetime import date
from .instruments import Instrument


class Price(BaseEntity):
    """Type representing a price in the database."""

    def __init__(
        self, id_: int, instrument: Instrument, price_date: date, price: float | int
    ):
        super().__init__(id_)
        self.price_date = price_date
        self.instrument = instrument
        self.price = price

    @property
    def price_date(self) -> date:
        """The date the price is for."""
        return self._price_date

    @price_date.setter
    def price_date(self, value: date) -> None:
        if not isinstance(value, date):
            raise TypeError
        self._price_date = value

    @property
    def instrument(self) -> Instrument:
        """The instrument the price is for."""
        return self._instrument

    @instrument.setter
    def instrument(self, value: Instrument) -> None:
        if not isinstance(value, Instrument):
            raise TypeError
        self._instrument = value

    @property
    def price(self) -> float | int:
        """The actual price, a numeric value."""
        return self._price

    @price.setter
    def price(self, value: float | int) -> None:
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError
        self._price = value
