"""Contains types for interacting with the risk report database."""

__all__: list[str] = ["RiskDbAccessor"]

from .dbaccessor import db_accessor_factory, DbAccessor, DbEngine
from ...types import *
from typing import Any


class RiskDbAccessor:
    """Type used for communicating with the risk report database."""

    def __init__(self):
        self._db_accessor = db_accessor_factory(
            DbEngine.SQLITE, db_path="./db/alecta_case_db.db"
        )

    def __enter__(self) -> object:
        self._db_accessor.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._db_accessor.close()

    def _generic_select(self, columns: list[str], table: str, /) -> list[Any]:
        return self._db_accessor.execute_select_query(
            f"select {','.join(columns)} from {table};"
        )

    def get_instruments(self) -> list[Instrument]:
        """Get all instruments in the database.

        Returns:
            A list of all instruments in the database.
        """

        instruments_ = self._generic_select(
            ["id", "name", "instrument_type_id"], "Instrument"
        )
        result: list[Instrument] = []
        for inst in instruments_:
            match inst[2]:
                case 1:
                    result.append(Equity(inst[0], inst[1]))
                case 2:
                    result.append(Bond(inst[0], inst[1]))
                case _:
                    raise ValueError(
                        f"instrument_type_id {inst[2]} has not been implemented."
                    )
        return result

    def get_instrument(self, id_: int) -> Instrument | None:
        """Get the instrument with the provided id.

        Attributes:
            id_: The id of the instrument.

        Returns:
            The instrument if found, otherwise None.
        """
        instruments_: list[Instrument] = [
            i for i in self.get_instruments() if i.id_ == id_
        ]
        count = len(instruments_)
        if count == 0:
            return None
        else:
            return instruments_[0]

    def get_instrument_types(self) -> list[InstrumentType]:
        instrument_types: list[Any] = self._generic_select(
            ["id", "name"], "InstrumentType"
        )
        return [InstrumentType(row[0], row[1]) for row in instrument_types]

    def get_portfolios(self) -> list[Portfolio]:
        """Gets all portfolios in the database.

        Returns:
            A list of all portfolios in the database.
        """

        portfolios: list[Any] = self._generic_select(["id", "name"], "Portfolio")
        return [Portfolio(row[0], row[1]) for row in portfolios]

    def get_portfolio(self, id_: int) -> Portfolio | None:
        """Gets the portfoliow ith the provided id.

        Attributes:
            id_: The id of the portfolio.

        Returns:
            The portfolio if found, otherwise None.
        """
        portfolios_: list[Portfolio] = [
            i for i in self.get_portfolios() if i.id_ == id_
        ]
        count = len(portfolios_)
        if count == 0:
            return None
        else:
            return portfolios_[0]

    def get_positions(self) -> list[Position]:
        positions_: list[Any] = self._generic_select(
            ["id", "date_from", "date_to", "portfolio_id", "instrument_id", "quantity"],
            "Position",
        )
        result: list[Position] = []
        for p in positions_:
            pass  # TODO Implement
