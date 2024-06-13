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
