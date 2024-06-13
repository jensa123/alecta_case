"""Definition of portfolio class."""

__all__: list[str] = ["Portfolio"]

from .base_entity import BaseEntityNamed


class Portfolio(BaseEntityNamed):
    """Class representing a portfolio."""

    def __init__(self, id_, name) -> None:
        super().__init__(id_, name)
