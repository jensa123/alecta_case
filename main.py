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

    print(f"Running risk report for date {get_input_date(argv)}")
    # -----------------------------------------------------------

    risk_db_accessor: RiskDbAccessor
    with RiskDbAccessor() as risk_db_accessor:
        print(risk_db_accessor)
        instruments_ = risk_db_accessor.get_instruments()
        for i in instruments_:
            print(i)

        print("Get one instrument")
        i = risk_db_accessor.get_instrument(2)
        print(i)

        print("Get instrument types")
        instrument_types = risk_db_accessor.get_instrument_types()
        for inst_type in instrument_types:
            print(inst_type)

        print("Get portfolios")
        portfolios = risk_db_accessor.get_portfolios()
        for p in portfolios:
            print(p)
        p = risk_db_accessor.get_portfolio(3)
        print(p)

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

    # ------------------------------------
    print("Risk report program finished.")
