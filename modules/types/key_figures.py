"""Definitions of types used to represent key figures."""

__all__: list["str"] = ["KeyFigureRefType", "KeyFigure", "KeyFigureValue"]

from .base_entity import BaseEntity, BaseEntityNamed
from enum import Enum
from datetime import date


class KeyFigureRefType(BaseEntityNamed):
    """Represents the type of entity a key figure value is for."""

    def __init__(self, id_: int, name: str) -> None:
        super().__init__(id_, name)


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
        reference_entity: BaseEntity,
        key_figure: KeyFigure,
    ) -> None:
        super().__init__(id_)
        self.key_figure_date = key_figure_date
        self.value = value
        self.key_figure_ref_type = key_figure_ref_type
        self.reference_entity = reference_entity
        self.key_figure = key_figure

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
    def reference_entity(self) -> BaseEntity:
        """The base entity the key figure value is for."""
        return self._reference_entity

    @reference_entity.setter
    def reference_entity(self, value: BaseEntity) -> None:
        if not isinstance(value, BaseEntity):
            raise TypeError
        self._reference_entity = value

    @property
    def key_figure(self) -> KeyFigure:
        """The the key figure the key figure value represents."""
        return self._key_figure

    @key_figure.setter
    def key_figure(self, value: KeyFigure) -> None:
        if not isinstance(value, KeyFigure):
            raise TypeError
        self._key_figure = value
