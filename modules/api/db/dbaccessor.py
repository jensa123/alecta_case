"""Contains definitions of types used for accessing the database."""

__all__: list[str] = [
    "DbEngine",
    "db_accessor_factory",
    "DbAccessor",
    "SQLiteDbAccesssor",
]

import sqlite3
from typing import Any
from contextlib import closing
from abc import ABC, abstractmethod
from enum import Enum


class DbEngine(Enum):
    """Enumerates the various database engines used."""

    SQLITE = 1


class DbAccessor(ABC):
    """Abstract base class (ABC) defining the interface to be implemented for database accessor types."""

    @abstractmethod
    def __init__(self):
        self._is_open = False

    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_open(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def execute_select_query(
        self, query: str, parameters: tuple[Any, ...] = ()
    ) -> list[Any]:
        """Executes a query and returns the rows.

        Args:
            query: The SQL query to execute, using ? as placeholders for parameters.
            parameters: A tuple of parameters.

        Returns:
            A list of tuples, where each element in the list represents a row
            and the elements of each tuple represents columns.
        """

        raise NotImplementedError

    @abstractmethod
    def execute_query(self, query: str, parameters: tuple[Any, ...] = ()) -> None:
        """Executes a query against the database and does not return anything.

        This method should only be used if the goal is to simply execute a query
        against the database and not care about any side effects.

        Args:
            query: The SQL query to execute, using ? as placeholders for parameters.
            parameters: A tuple of parameters.
        """

        raise NotImplementedError

    @abstractmethod
    def execute_insert_statement(
        self, query: str, parameters: tuple[Any, ...] = ()
    ) -> int | None:
        """Executes a query against the database and returns the last affected row id.

        Args:
            query: The SQL query to execute, using ? as placeholders for parameters.
            parameters: A tuple of parameters.
        """

        raise NotImplementedError


class SQLiteDbAccesssor(DbAccessor):
    """Type used for reading from and writing to an SQLite database.

    Example usage:
        with DbAccesssor("./db/alecta_case_db.db") as db_accessor:
            rows = db_accessor.execute_select_query(
                "select * from Instrument where id = ?;", (1,)
            )
            print(rows)

    Attributes:
        db_path: The path (relative to where the invoked Python script resides) to the SQLite database.
    """

    def __init__(self, db_path: str) -> None:
        super().__init__()
        self.db_path = db_path

    def connect(self) -> None:
        """Opens a database connection if not already open."""
        if self._is_open:
            return
        self.connection = sqlite3.connect(self.db_path)
        self._is_open = True

    def close(self) -> None:
        """Closes the database connection if it is open."""
        if not self._is_open:
            return
        self.connection.close()
        self._is_open = False

    def __enter__(self) -> object:
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def is_open(self) -> bool:
        """Returns True if the database connection is open, otherwise False."""
        return self._is_open

    def execute_select_query(
        self, query: str, parameters: tuple[Any, ...] = ()
    ) -> list[Any]:
        with closing(self.connection.cursor()) as cur:
            rows = cur.execute(query, parameters).fetchall()
            return rows

    def execute_query(self, query: str, parameters: tuple[Any, ...] = ()) -> None:
        with closing(self.connection.cursor()) as cur:
            cur.execute(query, parameters)
            self.connection.commit()

    def execute_insert_statement(self, query, parameters=()):
        with closing(self.connection.cursor()) as cur:
            cur.execute(query, parameters)
            cnt = cur.rowcount
            if cnt == 0:
                return None
            if cnt > 1:
                raise ValueError(
                    f"Insert statements inserting more than one row is not supported. Number of affected rows: {cnt}"
                )
            # self.connection.commit()
            return cur.lastrowid


def db_accessor_factory(
    db_engine: DbEngine, /, db_path: str = "", connection_string: str = ""
) -> DbAccessor:
    """Method used for creating a database accessor corresponding to a specific engine."""

    match db_engine:
        case DbEngine.SQLITE:
            return SQLiteDbAccesssor(db_path)
    raise ValueError(
        f"Types corresponding to engine {db_engine} has not been implemented."
    )
