"""Main script for executing the risk report.

How to run this script:

- Configure the RiskReportSettings object by choosing
portfolio, date range and key figures.

- Run script from command line: python main.py
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


if __name__ == "__main__":

    risk_report: RiskReport = RiskReport(
        RiskReportSettings(
            "EQ_US",  # Allowed values: EQ_US, EQ_SWE, FI_US, FI_SWE
            date(2024, 1, 1),  # Must be >= 2024-01-01
            date(2024, 5, 31),  # Must be <= 2024-05-31
            ["Market value", "Return (1D)", "Volatility (3M, ann.)"],
        )
    )
    output: dict[str, Any] = risk_report.generate()
    print(json.dumps(output, indent=4))
