"""Contains various unit tests."""

import unittest
from modules.helpers.dateutilities import last_business_day
from datetime import date
from modules.types.position import Position
from modules.types.instruments import Equity
from modules.types.portfolio import Portfolio


class DateUtilitiesTestCase(unittest.TestCase):
    """Contains unit tests for the dateutilities module."""

    def test_last_business_day(self):
        self.assertEqual(date(2024, 6, 12), last_business_day(date(2024, 6, 13)))
        self.assertEqual(date(2024, 6, 13), last_business_day(date(2024, 6, 14)))
        self.assertEqual(date(2024, 6, 14), last_business_day(date(2024, 6, 15)))
        self.assertEqual(date(2024, 6, 14), last_business_day(date(2024, 6, 16)))
        self.assertEqual(date(2024, 6, 14), last_business_day(date(2024, 6, 17)))
        self.assertEqual(date(2024, 6, 17), last_business_day(date(2024, 6, 18)))


class PositionTestCase(unittest.TestCase):
    """Contains unit tests for the Position class."""

    def test_create_position(self):
        instrument = Equity(1, "Nvidia")
        portfolio = Portfolio(2, "EQ_US")
        position_date = date(2024, 5, 31)
        pos_1 = Position.create(1, portfolio, instrument, position_date, 55)

    def test_position_market_value(self):
        # Create by adding to properties.
        pos_1 = Position(1)
        pos_1.instrument = Equity(1, "Nvidia")
        pos_1.portfolio = Portfolio(2, "EQ_US")
        pos_1.position_date = date(2024, 5, 31)
        pos_1.quantity = 55
        pos_1_mv = pos_1.market_value(312.0)
        self.assertEqual(pos_1_mv, 17160.0)

        # Create by using class factory method.
        instrument = Equity(2, "Volvo")
        portfolio = Portfolio(1, "EQ_SWE")
        position_date = date(2024, 6, 12)
        pos_2 = Position.create(1, portfolio, instrument, position_date, 12)
        pos_2_mv = pos_2.market_value(78.0)
        self.assertEqual(pos_2_mv, 936)


if __name__ == "__main__":
    unittest.main()
