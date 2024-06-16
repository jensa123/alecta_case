"""Contains types used for generating figures used by the risk report."""

__all__: list[str] = ["RiskFigureGenerator"]

from ..api.db import RiskDbAccessor
from ..types import *
from datetime import date, timedelta
import statistics
import math


class RiskFigureGenerator:
    """Class used for calculating and persisting risk figures consumed by the risk report."""

    def __init__(self) -> None:
        self._risk_db_accessor = RiskDbAccessor()

    def market_value_for_portfolio_and_date(
        self, portfolio_name: str, date_: date
    ) -> KeyFigureValue:
        """Calculates and stores the market value for a given portfolio and date.

        Args:
            portfolio_name: The name of the portfolio.
            date_: The date to calculate and store market value for.

        Returns:
            A KeyFigureValue object representing the key figure value
            which was either inserted or updated in the database.
        """

        db: RiskDbAccessor
        with self._risk_db_accessor as db:
            portfolio_ = db.get_portfolio_from_name(portfolio_name)
            ref_type = db.get_key_figure_ref_type_from_name("Portfolio")
            key_figure = db.get_key_figure_from_name("Market value")
            positions: list[Position] = db.get_positions(
                position_date=date_, portfolio=portfolio_
            )
            total_mv: float = 0.0
            for pos in positions:
                instrument_price: Price = db.get_prices(
                    instrument=pos.instrument, date_from=date_, date_to=date_
                )[0]
                total_mv += pos.market_value(instrument_price.price)

            key_figure_value: KeyFigureValue = KeyFigureValue(
                0, date_, total_mv, ref_type, portfolio_, key_figure
            )
            db.insert_or_update_key_figure(key_figure_value)
            return key_figure_value

    def market_value_for_portfolio_and_date_range(
        self, portfolio_name: str, date_from: date, date_to: date
    ) -> list[KeyFigureValue]:
        """Calculates and stores the market value for a given portfolio and date range.

        Args:
            portfolio_name: The name of the portfolio.
            date_from: The first date to calculate and store market value for.
            date_to: The last date to calculate and store market value for.

        Returns:
            A list of KeyFigureValue objects representing the key figure values
            which were either inserted or updated in the database.
        """

        result: list[KeyFigureValue] = []
        date_: date = date_from
        while date_ <= date_to:
            result.append(
                self.market_value_for_portfolio_and_date(portfolio_name, date_)
            )
            date_ = date_ + timedelta(days=1)
        return result

    def return_1D_for_portfolio_and_date(
        self, portfolio_name: str, date_: date
    ) -> KeyFigureValue:
        prev_date: date = date_ - timedelta(days=1)
        market_values: list[KeyFigureValue] = (
            self.market_value_for_portfolio_and_date_range(
                portfolio_name, prev_date, date_
            )
        )

        return_1D: float = market_values[1].value / market_values[0].value - 1.0

        db: RiskDbAccessor
        with self._risk_db_accessor as db:
            key_figure = db.get_key_figure_from_name("Return (1D)")
            key_figure_value: KeyFigureValue = KeyFigureValue(
                0,
                date_,
                return_1D,
                market_values[0].key_figure_ref_type,
                market_values[0].reference_entity,
                key_figure,
            )
            db.insert_or_update_key_figure(key_figure_value)
            return key_figure_value

    def return_1D_for_portfolio_and_date_range(
        self, portfolio_name: str, date_from: date, date_to: date
    ) -> list[KeyFigureValue]:
        result: list[KeyFigureValue] = []
        date_: date = date_from
        while date_ <= date_to:
            result.append(self.return_1D_for_portfolio_and_date(portfolio_name, date_))
            date_ = date_ + timedelta(days=1)
        return result

    def volatility_3M_ann_for_portfolio_and_date(
        self, portfolio_name: str, date_: date
    ) -> KeyFigureValue:
        date_start: date = date_ - timedelta(days=89)
        returns: list[KeyFigureValue] = self.return_1D_for_portfolio_and_date_range(
            portfolio_name, date_start, date_
        )
        vol = statistics.stdev([math.log(1 + k.value) for k in returns])
        vol = vol * math.sqrt(365)  # Annualize

        db: RiskDbAccessor
        with self._risk_db_accessor as db:
            portfolio_ = db.get_portfolio_from_name(portfolio_name)
            ref_type = db.get_key_figure_ref_type_from_name("Portfolio")
            key_figure = db.get_key_figure_from_name("Volatility (3M, ann.)")
            key_figure_value: KeyFigureValue = KeyFigureValue(
                0, date_, vol, ref_type, portfolio_, key_figure
            )
            db.insert_or_update_key_figure(key_figure_value)
            return key_figure_value

    def return_1D_cumulative_series(
        self, portfolio_name: str, date_from: date, date_to: date
    ) -> list[tuple[date, float]]:

        returns: list[KeyFigureValue] = self.return_1D_for_portfolio_and_date_range(
            portfolio_name, date_from, date_to
        )

        result: list[tuple[date, float]] = []
        date_: date = date_from
        cumulative_return: float = 0
        while date_ <= date_to:
            key_figure_value: KeyFigureValue = next(
                filter(lambda k: k.key_figure_date == date_, returns)
            )
            cumulative_return = (1 + cumulative_return) * (
                1 + key_figure_value.value
            ) - 1.0
            result.append((date_, cumulative_return))
            date_ = date_ + timedelta(days=1)
        return result
