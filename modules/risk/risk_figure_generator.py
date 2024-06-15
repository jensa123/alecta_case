"""Contains types used for generating figures used by the risk report."""

from ..api.db import RiskDbAccessor
from ..types import *
from datetime import date, timedelta


class RiskFigureGenerator:

    def __init__(self) -> None:
        self._risk_db_accessor = RiskDbAccessor()

    def market_value_for_portfolio_and_date(
        self, portfolio_name: str, date_: date
    ) -> None:
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

            db.insert_key_figure_value(
                KeyFigureValue(0, date_, total_mv, ref_type, portfolio_, key_figure)
            )

    def market_value_for_portfolio_and_date_range(
        self, portfolio_name: str, date_from: date, date_to: date
    ):
        date_: date = date_from
        while date_ <= date_to:
            self.market_value_for_portfolio_and_date(portfolio_name, date_)
            date_ = date_ + timedelta(days=1)
