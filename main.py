"""Main script for executing the risk report.

How to run this script:
python main.py 2024-05-31

"""

from modules.types import *
from sys import argv
from datetime import date
from modules.helpers.common import is_valid_string


if __name__ == "__main__":
    print("Running risk report for date...")
    # eq = Equity(1, "Nvidia")
    # bo = Bond(100, "SGB 1058")
    p1 = Portfolio(1, "ALFA_JR")
    p2 = Portfolio(1, "ALFA_JR")
    print(p1 == p2)
    print(p1 is p2)
