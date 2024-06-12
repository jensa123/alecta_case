"""Definitions of instrument types.

This module contains definitions of instrument types used for generating
the risk report.
"""

__all__: list[str] = ["Instrument", "Equity", "Bond"]

from abc import abstractmethod
from .base_entity import BaseEntityNamed
from ..helpers.common import is_valid_string


class Instrument(BaseEntityNamed):
    """Abstract base class for instruments containing common properties.

    This class cannot be instantiated, it acts as a general blueprint
    for more specific instrument classes. All instrument have an instrument_id
    property. This property can only be set when creating the instrument.
    """

    @abstractmethod
    def __init__(self, instrument_id: int, name: str) -> None:
        super().__init__(instrument_id, name)

    @abstractmethod
    def market_value(self) -> float:
        """Calculates the market value of a position held in the instrument."""
        pass


class Equity(Instrument):
    """Class representing an equity investment."""

    def __init__(self, instrument_id, name) -> None:
        super().__init__(instrument_id, name)

    def market_value(self, price: float = 0, quantity: float = 0) -> float:
        """Calculates the market value of a position held in the equity instrument.

        The market value is defined as price * quantity.

        Args:
            price: The price of the equity.
            quantity: The quantity of the position held in the equity.
        """
        return price * quantity


class Bond(Instrument):
    """Class representing a bond investment."""

    def __init__(self, instrument_id, name) -> None:
        super().__init__(instrument_id, name)

    def market_value(self, price: float = 0, notional: float = 0) -> float:
        """Calculates the market value of a position held in the bond.

        Args:
            price: The dirty price of the bond.
            notional: The notional amount of the position held in the bond.
        """
        return price / 100.0 * notional
