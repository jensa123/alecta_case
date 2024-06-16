"""Contains types related to the risk report."""

__all__: list[str] = ["RiskReportSettings", "RiskReport"]

from .risk_figure_generator import RiskFigureGenerator
from ..types import KeyFigureValue
from datetime import date
from typing import Any


class RiskReportSettings:
    """Type representing settings used to generate the risk report."""

    def __init__(
        self,
        portfolio_name: str,
        date_from: date,
        date_to: date,
        key_figures: list[str],
        /,
    ) -> None:
        self.portfolio_name = portfolio_name
        self.date_from = date_from
        self.date_to = date_to
        self.key_figures = key_figures


class RiskReport:
    """Type used to generate figures used by the risk report."""

    def __init__(self, settings: RiskReportSettings) -> None:
        self.settings = settings
        self.rfg = RiskFigureGenerator()

    def generate(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "portfolio": self.settings.portfolio_name,
            "date_from": self.settings.date_from.isoformat(),
            "date_to": self.settings.date_to.isoformat(),
            "key_figures": {},
        }

        for key_figure in self.settings.key_figures:
            if key_figure == "Market value":
                mv: KeyFigureValue = self.rfg.market_value_for_portfolio_and_date(
                    self.settings.portfolio_name, self.settings.date_to
                )
                result["key_figures"][key_figure] = mv.value
            elif key_figure == "Return (1D)":
                ret_1D: KeyFigureValue = self.rfg.return_1D_for_portfolio_and_date(
                    self.settings.portfolio_name, self.settings.date_to
                )
                result["key_figures"][key_figure] = ret_1D.value
            elif key_figure == "Volatility (3M, ann.)":
                vol: KeyFigureValue = self.rfg.volatility_3M_ann_for_portfolio_and_date(
                    self.settings.portfolio_name, self.settings.date_to
                )
                result["key_figures"][key_figure] = vol.value
            else:
                raise ValueError(f"Key figure {key_figure} is not supported.")

        # Always add a series with cumulative returns for [date_from, date_to].
        result["cumulative_returns"] = [
            (t[0].isoformat(), t[1])
            for t in self.rfg.return_1D_cumulative_series(
                self.settings.portfolio_name,
                self.settings.date_from,
                self.settings.date_to,
            )
        ]

        return result
