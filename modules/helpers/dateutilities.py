"""Useful date functions.

Contains useful date functions, such as retrieving
the last business day etc.
"""

__all__: list[str] = ["last_business_day"]

from datetime import date, timedelta


def last_business_day(input_date: date) -> date:
    """Get the last business day based on a given input date."""
    if not isinstance(input_date, date):
        raise TypeError
    weekday = input_date.weekday()
    subtract_days = 1
    match weekday:
        case 6:
            subtract_days = 2
        case 0:
            subtract_days = 3
    return input_date.__sub__(timedelta(days=subtract_days))
