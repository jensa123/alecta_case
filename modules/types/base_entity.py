"""Definitions of generic base class entity types."""

__all__: list[str] = ["BaseEntity", "BaseEntityNamed"]

from abc import ABC, abstractmethod
from ..helpers.common import is_valid_string


class BaseEntity(ABC):
    """Abstract base class (ABC) representing an entity with an id.

    This is the lowest level common base class for all entity types.
    A class deriving from this ABC should call super().__init__(id_)
    in its own __init__ method.

    The attribute named id_ is mapped to the automatically generated
    primary key in the database. A value of 0 (zero) should be used
    to represent an in-memory object which has not yet been persisted
    to the database.

    Attributes:
        id_: An identifier for the entity, unique among the set of entities of the same type.
    """

    @abstractmethod
    def __init__(self, id_: int) -> None:
        self.id_ = id_

    @property
    def id_(self) -> int:
        """The id of the entity."""
        return self._id

    @id_.setter
    def id_(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        if value < 0:
            raise ValueError(f"id_ must be >= 0, argument is {value}.")
        self._id = value

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

    def __str__(self) -> str:
        return f"Class: {self.__class__.__name__}, id_: {self.id_}"


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

    def __str__(self) -> str:
        return super().__str__() + f", name: {self.name}"
