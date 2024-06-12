"""Contains various unit tests."""

import unittest
from modules.helpers.dateutilities import last_business_day
from datetime import date


class DateUtilitiesTestCase(unittest.TestCase):
    """Contains unit tests for the dateutilities module."""

    def test_last_business_day(self):
        self.assertEqual(date(2024, 6, 12), last_business_day(date(2024, 6, 13)))
        self.assertEqual(date(2024, 6, 13), last_business_day(date(2024, 6, 14)))
        self.assertEqual(date(2024, 6, 14), last_business_day(date(2024, 6, 15)))
        self.assertEqual(date(2024, 6, 14), last_business_day(date(2024, 6, 16)))
        self.assertEqual(date(2024, 6, 14), last_business_day(date(2024, 6, 17)))
        self.assertEqual(date(2024, 6, 17), last_business_day(date(2024, 6, 18)))


if __name__ == "__main__":
    unittest.main()
