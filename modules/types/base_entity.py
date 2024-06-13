"""Definitions of generic base class entity types."""

__all__: list[str] = ["BaseEntity", "BaseEntityNamed"]

from abc import ABC, abstractmethod
from ..helpers.common import is_valid_string


class BaseEntity(ABC):
    """Abstract base class (ABC) representing an entity with an id.

    This is the lowest level common base class for all entity types.
    A class deriving from this ABC should call super().__init__(id_)
    in its own __init__ method.
    """

    @abstractmethod
    def __init__(self, id_: int) -> None:
        self._id = id_

    @property
    def id_(self) -> int:
        """The id of the entity."""
        return self._id

    def __eq__(self, other: object) -> bool:
        """Value comparison of BaseEntity objects.

        Args:
            other: The BaseEntity object to check for equality against.

        Returns:
            True if other is an instance of BaseEntity and if it's id_
            property has the same value.
        """
        if not type(other) is type(self):
            return False
        return self._id == other._id


class BaseEntityNamed(BaseEntity):
    """Abstract base class (ABC) representing an entity with an id and a name."""

    @abstractmethod
    def __init__(self, id_: int, name: str) -> None:
        super().__init__(id_)
        self.name = name

    @property
    def name(self) -> str:
        """The name of the instrument."""
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        if not is_valid_string(value):
            raise ValueError
        self.__name = value
