"""Contains definition of InstrumentType class."""

__all__: list[str] = ["InstrumentType"]

from .base_entity import BaseEntityNamed


class InstrumentType(BaseEntityNamed):
    """Type representing an instrument type."""

    def __init__(self, id_: int, name: str) -> None:
        super().__init__(id_, name)
