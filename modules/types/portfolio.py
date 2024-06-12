from .base_entity import BaseEntityNamed

__all__: list[str] = ["Portfolio"]


class Portfolio(BaseEntityNamed):
    """Class representing a portfolio."""

    def __init__(self, id_, name) -> None:
        super().__init__(id_, name)

    def __eq__(self, other: object) -> bool:
        return super().__eq__(other)
