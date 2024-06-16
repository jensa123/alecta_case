"""Main script for executing the risk report.

How to run this script:
python main.py 2024-05-31

"""

from modules.types import *
from sys import argv
from datetime import date
from modules.helpers.common import is_valid_string
from modules.helpers.dateutilities import last_business_day
from modules.types.position import Position
from modules.types.key_figures import KeyFigureRefType
from modules.api.db import db_accessor_factory, DbEngine, DbAccessor, RiskDbAccessor
from modules.risk import RiskFigureGenerator
from modules.risk import RiskReportSettings, RiskReport
from typing import Any
import json


def get_input_date(argv: list[str]) -> date:
    """Get the date to run the risk report for from command line arguments.

    Args:
        argv: The list[str] containing command line arguments passed to the script.

    Returns:
        The date to use when running the risk report.
    """
    if len(argv) == 1:
        return last_business_day(date.today())
    else:
        return date.fromisoformat(argv[1])


if __name__ == "__main__":

    risk_report: RiskReport = RiskReport(
        RiskReportSettings(
            "EQ_SWE",
            date(2024, 1, 1),
            date(2024, 5, 31),
            ["Market value", "Return (1D)", "Volatility (3M, ann.)"],
        )
    )
    output: dict[str, Any] = risk_report.generate()
    print(json.dumps(output, indent=4))

    # risk_db_accessor: RiskDbAccessor
    # with RiskDbAccessor() as risk_db_accessor:
    #     portfolio_ = risk_db_accessor.get_portfolio_from_name("EQ_US")
    #     ref_type = risk_db_accessor.get_key_figure_ref_type_from_name("Portfolio")
    #     key_figure = risk_db_accessor.get_key_figure_from_name("Market value")
    #     date_: date = date(2024, 1, 1)
    #     risk_db_accessor.insert_or_update_key_figure(
    #         KeyFigureValue(4, date_, 3333, ref_type, portfolio_, key_figure)
    #     )

    # g = RiskFigureGenerator()
    # g.market_value_for_portfolio_and_date_range(
    #     "EQ_US", date(2023, 12, 31), date(2024, 5, 31)
    # )
    # g.return_1D_for_portfolio_and_date_range(
    #     "EQ_US", date(2024, 1, 1), date(2024, 5, 31)
    # )
    # g.volatility_3M_ann_for_portfolio_and_date("EQ_US", date(2024, 5, 31))

    # risk_db_accessor: RiskDbAccessor
    # with RiskDbAccessor() as risk_db_accessor:

    #     # Calculate market values for a portfolio for a date range
    #     portfolio_ = risk_db_accessor.get_portfolio_from_name("EQ_US")
    #     date_from: date = date(2023, 12, 31)
    #     date_to: date = date(2024, 5, 31)
    #     ref_type = risk_db_accessor.get_key_figure_ref_type_from_name("Portfolio")
    #     key_figure = risk_db_accessor.get_key_figure_from_name("Market value")

    #     vdate: date = date_from
    #     while vdate <= date_to:

    #         positions: list[Position] = risk_db_accessor.get_positions(vdate, portfolio)

    #         vdate = vdate + 1

    # print(risk_db_accessor)
    # instruments_ = risk_db_accessor.get_instruments()
    # for i in instruments_:
    #     print(i)

    # print("Get one instrument")
    # i = risk_db_accessor.get_instrument(2)
    # print(i)

    # print("Get instrument types")
    # instrument_types = risk_db_accessor.get_instrument_types()
    # for inst_type in instrument_types:
    #     print(inst_type)

    # print("Get portfolios")
    # portfolios = risk_db_accessor.get_portfolios()
    # for p in portfolios:
    #     print(p)
    # p = risk_db_accessor.get_portfolio(3)
    # print(p)

    # print("Get positions")
    # positions = risk_db_accessor.get_positions(
    #     position_date=date(2023, 12, 31),
    #     portfolio=risk_db_accessor.get_portfolio_from_name("FI_SWE"),
    # )
    # for pos in positions:
    #     print(pos)

    # print("Get key figures")
    # key_figures_ = risk_db_accessor.get_key_figures()
    # for kf in key_figures_:
    #     print(kf)
    # mv_kf = risk_db_accessor.get_key_figure_from_name("Market value")
    # print(mv_kf)

    # print("Get key figure ref types")
    # key_figure_ref_types = risk_db_accessor.get_key_figure_ref_types()
    # for kfrt in key_figure_ref_types:
    #     print(kfrt)

    # print("Get all prices")
    # all_prices = risk_db_accessor.get_prices()

    # print("Get prices for a particular instrument and date range")
    # tesla_april_prices = risk_db_accessor.get_prices(
    #     instrument=risk_db_accessor.get_instrument_from_name("Tesla"),
    #     date_from=date(2024, 4, 1),
    #     date_to=date(2024, 4, 30),
    # )

    # print("Get all key figure values")
    # all_key_figure_values = risk_db_accessor.get_key_figure_values()
    # for kfv in all_key_figure_values:
    #     print(kfv)

    # print("Delete all key figure values")
    # risk_db_accessor.delete_key_figure_values()

    # print("Insert a key figure value")
    # kfv = KeyFigureValue(
    #     0,
    #     date(2023, 12, 31),
    #     55.0 * 100 + 3.0 * 100,
    #     risk_db_accessor.get_key_figure_ref_type_from_name("Portfolio"),
    #     risk_db_accessor.get_portfolio_from_name("EQ_US"),
    #     risk_db_accessor.get_key_figure_from_name("Market value"),
    # )
    # risk_db_accessor.insert_key_figure_value(kfv)

    # db_accessor: DbAccessor = db_accessor_factory(
    #     DbEngine.SQLITE, "./db/alecta_case_db.db"
    # )
    # db_accessor.connect()
    # electrolux = Equity(0, "Electrolux")
    # last_row_id = db_accessor.execute_insert_statement(
    #     "insert into Instrument (name, instrument_type_id) values (?, ?), (?, ?)",
    #     (electrolux.name, 1, "HM", 1),
    # )
    # electrolux.id_ = last_row_id
    # db_accessor.close()

    # with db_acc as db_accessor:
    # db_accessor.
    # instruments = db_accessor.execute_select_query(
    #     "select * from Instrument where id = ?;", (1,)
    # )
    # for row in instruments:
    #     inst_type: int = row[2]
    #     if inst_type == 1:
    #         equity = Equity(row[0], row[1])
    #     elif inst_type == 2:
    #         bond = Bond(row[0], row[1])
    #     print(row)
