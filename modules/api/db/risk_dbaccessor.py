"""Contains types for interacting with the risk report database."""

__all__: list[str] = ["RiskDbAccessor"]

from .dbaccessor import db_accessor_factory, DbAccessor, DbEngine
from ...types import *
from typing import Any
from datetime import date


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

    def _generic_select(
        self, columns: list[str], table: str, /, *, id_: int | None = None
    ) -> list[Any]:
        query = f"select {','.join(columns)} from {table}"
        parameters: tuple[Any, ...] = ()
        if id_ is not None:
            query = query + f" where id = ?;"
            parameters = (id_,)
        else:
            query = query + ";"
        return self._db_accessor.execute_select_query(query, parameters)

    def _generic_delete(self, id_: int, table: str, /) -> int:
        return self._db_accessor.execute_query(
            f"delete from {table} where id = ?", (id_,)
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

    def get_instrument_from_name(self, name: str) -> Instrument | None:
        """Gets the instrument with the provided name.

        Args:
            name: The name of the instrument.

        Returns:
            The instrument if found, otherwise None.
        """
        instruments_: list[Instrument] = [
            i for i in self.get_instruments() if i.name == name
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
        """Gets the portfolio with the provided id.

        Args:
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

    def get_portfolio_from_name(self, name: str) -> Portfolio | None:
        """Gets the portfolio with the provided name.

        Args:
            name: The name of the portfolio.

        Returns:
            The portfolio if found, otherwise None.
        """
        portfolios_: list[Portfolio] = [
            i for i in self.get_portfolios() if i.name == name
        ]
        count = len(portfolios_)
        if count == 0:
            return None
        else:
            return portfolios_[0]

    def get_positions(
        self, *, position_date: date | None = None, portfolio: Portfolio | None = None
    ) -> list[Position]:
        """Gets all positions in the database.

        This method can also be called with arguments position_date and portfolio.
        If an argument is provided it is used to filter the results.

        Args:
            position_date: A date a position's [date_from, date_to] interval must cover.
            portfolio: A portfolio a position must belong to.

        Returns:
            A list of all positions in the database.
        """
        positions_: list[Any] = self._generic_select(
            ["id", "date_from", "date_to", "portfolio_id", "instrument_id", "quantity"],
            "Position",
        )
        result: list[Position] = []
        for pos in positions_:
            include: bool = True
            id_: int = pos[0]
            date_from = date.fromisoformat(pos[1])
            date_to = date.fromisoformat(pos[2])
            portfolio_: Portfolio = self.get_portfolio(pos[3])
            instrument_: Instrument = self.get_instrument(pos[4])
            quantity: float = pos[5]

            if position_date is not None:
                if not (position_date >= date_from and position_date <= date_to):
                    include = False

            if portfolio is not None:
                if not portfolio.id_ == portfolio_.id_:
                    include = False

            if include:
                result.append(
                    Position.create(
                        id_, portfolio_, instrument_, date_from, date_to, quantity
                    )
                )
        return result

    def get_position(self, id_: int) -> Position | None:
        positions: Position = [pos for pos in self.get_positions() if pos.id_ == id_]
        count: int = len(positions)
        if count == 0:
            return None
        else:
            return positions[0]

    def get_key_figures(self) -> list[KeyFigure]:
        key_figures_: list[Any] = self._generic_select(["id", "name"], "KeyFigure")
        return [KeyFigure(row[0], row[1]) for row in key_figures_]

    def get_key_figure(self, id_: int) -> KeyFigure | None:
        suspects = [kf for kf in self.get_key_figures() if kf.id_ == id_]
        count = len(suspects)
        if count == 0:
            return None
        else:
            return suspects[0]

    def get_key_figure_from_name(self, name: str) -> KeyFigure | None:
        key_figures_: list[KeyFigure] = [
            i for i in self.get_key_figures() if i.name == name
        ]
        count: int = len(key_figures_)
        if count == 0:
            return None
        else:
            return key_figures_[0]

    def get_key_figure_ref_types(self) -> list[KeyFigureRefType]:
        """Gets all key figure ref types in the database.

        Returns:
            A list of all key figure ref types in the database.
        """
        key_figure_ref_types: list[Any] = self._generic_select(
            ["id", "name"], "KeyFigureRefType"
        )
        return [KeyFigureRefType(row[0], row[1]) for row in key_figure_ref_types]

    def get_key_figure_ref_type_from_name(self, name: str) -> KeyFigureRefType | None:
        """Gets a key figure ref type matching the provided name from the database.

        Args:
            name: The name of the key figure ref type.

        Returns:
            A KeyFigureRefType instance if found, otherwise None.
        """
        key_figure_ref_types: list[KeyFigureRefType] = [
            i for i in self.get_key_figure_ref_types() if i.name == name
        ]
        count = len(key_figure_ref_types)
        if count == 0:
            return None
        else:
            return key_figure_ref_types[0]

    def get_key_figure_ref_type_from_id(self, id_: int) -> KeyFigureRefType | None:
        key_figure_ref_types: list[KeyFigureRefType] = self._generic_select(
            ["id", "name"], "KeyFigureRefType", id_=id_
        )
        count = len(key_figure_ref_types)
        if count == 0:
            return None
        else:
            return KeyFigureRefType(
                key_figure_ref_types[0][0], key_figure_ref_types[0][1]
            )

    def get_key_figure_values(self) -> list[KeyFigureValue]:
        """Gets all key figure values in the database.

        Returns:
            A list of KeyFigureValue instances.
        """
        key_figure_values: list[Any] = self._generic_select(
            ["id", "date", "value", "ref_type", "ref_entity_id", "key_figure_id"],
            "KeyFigureValue",
        )
        result: list[KeyFigureValue] = []
        for kfv in key_figure_values:
            id_: int = kfv[0]
            date_: date = date.fromisoformat(kfv[1])
            value: float | int = kfv[2]
            ref_type: KeyFigureRefType = self.get_key_figure_ref_type_from_id(kfv[3])
            ref_entity: BaseEntity
            match ref_type.name:
                case "Instrument":
                    ref_entity = self.get_instrument(kfv[4])
                case "Position":
                    ref_entity = self.get_position(kfv[4])
                case "Portfolio":
                    ref_entity = self.get_portfolio(kfv[4])
                case _:
                    raise RuntimeError
            key_figure = self.get_key_figure(kfv[5])
            result.append(
                KeyFigureValue(id_, date_, value, ref_type, ref_entity, key_figure)
            )
        return result

    def insert_key_figure_value(self, key_figure_value: KeyFigureValue) -> None:
        v: KeyFigureValue = key_figure_value

        row_id: int | None = self._db_accessor.execute_insert_statement(
            "insert into KeyFigureValue (date, value"
            ", ref_type, ref_entity_id, key_figure_id) values (?, ?, ?, ?, ?);",
            (
                v.key_figure_date.isoformat(),
                v.value,
                v.key_figure_ref_type.id_,
                v.reference_entity.id_,
                v.key_figure.id_,
            ),
        )

        if row_id is None:
            raise RuntimeError(f"No row id returned, insert most likely failed.")

        v.id_ = row_id

    def delete_key_figure_values(self) -> int:
        """Deletes all key figure values in the database.

        Returns:
            The number of deleted key figure values.
        """
        return self._db_accessor.execute_query("delete from KeyFigureValue;")

    def delete_key_figure_value(self, key_figure_value: KeyFigureValue) -> bool:
        row_count: int = self._generic_delete(
            key_figure_value.id_, key_figure_value.__class__.__name__
        )
        if row_count > 0:
            return True
        return False

    def get_prices(
        self,
        *,
        instrument: Instrument | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[Price]:
        """Gets prices from the database.

        This method can be called without arguments or optionally
        with arguments. If any argument is provided it is used as
        a filter.

        Args:
            instrument: The instrument to get prices for.
            date_from: The earliest date to get prices for.
            date_to: The latest date to get prices for.

        Returns:
            A list of Price objects.
        """

        all_prices: list[Any] = self._generic_select(
            ["id", "instrument_id", "date", "price"], "Prices"
        )

        result: list[Price] = []
        for price in all_prices:
            include: bool = True
            id_: int = price[0]
            instrument_id = price[1]
            date_: date = date.fromisoformat(price[2])
            value: float = price[3]

            if instrument is not None:
                if instrument.id_ != instrument_id:
                    include = False
            if date_from is not None:
                if date_ < date_from:
                    include = False
            if date_to is not None:
                if date_ > date_to:
                    include = False

            if include:
                result.append(
                    Price(id_, self.get_instrument(instrument_id), date_, value)
                )
        return result
