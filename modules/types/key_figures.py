"""Definitions of types used to represent key figures."""

__all__: list["str"] = ["KeyFigureRefType", "KeyFigure", "KeyFigureValue"]

from .base_entity import BaseEntity, BaseEntityNamed
from enum import Enum
from datetime import date


class KeyFigureRefType(Enum):
    """Enumerates the different types of entities a key figure can represent."""

    INSTRUMENT = 1
    POSITION = 2
    PORTFOLIO = 3


class KeyFigure(BaseEntityNamed):
    """Represents a key figure."""

    def __init__(self, id_: int, name: str) -> None:
        super().__init__(id_, name)


class KeyFigureValue(BaseEntity):
    """Represents an actual value for a key figure.

    A key figure is a numeric value for a given date and type of entity.
    For example, a key figure could represent the standard deviation of
    the log returns for the price of a particular instrument.
    """

    def __init__(
        self,
        id_: int,
        key_figure_date: date,
        value: float | int,
        key_figure_ref_type: KeyFigureRefType,
        reference_entity_id: int,
        key_figure_id: int,
    ) -> None:
        super().__init__(id_)
        self.key_figure_date = key_figure_date
        self.value = value
        self.key_figure_ref_type = key_figure_ref_type
        self.reference_entity_id = reference_entity_id
        self.key_figure_id = key_figure_id

    @property
    def key_figure_date(self) -> date:
        """The date the key figure is for."""
        return self._key_figure_date

    @key_figure_date.setter
    def key_figure_date(self, value: date) -> None:
        if not isinstance(value, date):
            raise TypeError
        self._key_figure_date = value

    @property
    def value(self) -> float | int:
        """The numeric value of the key figure value."""
        return self._value

    @value.setter
    def value(self, value: float | int) -> None:
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError
        self._value = value

    @property
    def key_figure_ref_type(self) -> KeyFigureRefType:
        """The type of the entity the key figure value is for."""
        return self._key_figure_ref_type

    @key_figure_ref_type.setter
    def key_figure_ref_type(self, value: KeyFigureRefType) -> None:
        if not isinstance(value, KeyFigureRefType):
            raise TypeError
        self._key_figure_ref_type = value

    @property
    def reference_entity_id(self) -> int:
        """The id of the entity the key figure value is for."""
        return self._reference_entity_id

    @reference_entity_id.setter
    def reference_entity_id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        self._reference_entity_id = value

    @property
    def key_figure_id(self) -> int:
        """The id of the key figure the key figure value represents."""
        return self._key_figure_id

    @key_figure_id.setter
    def key_figure_id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        self._key_figure_id = value
