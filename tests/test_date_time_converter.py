from datetime import date, datetime
import unittest
import pytest

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from add_articles_to_graph.date_time_converter import get_datetime


class TestDateTime(unittest.TestCase):
    def testMonthParsedCorrectly(self):
        dateTimeObject = get_datetime("2022-05-11T10:45:32.000Z")
        assert dateTimeObject.month == 5

    def testYearParsedCorrectly(self):
        dateTimeObject = get_datetime("2022-05-11T10:45:32.000Z")
        assert dateTimeObject.year == 2022

    def testDayParsedCorrectly(self):
        dateTimeObject = get_datetime("2022-05-11T10:45:32.000Z")
        assert dateTimeObject.day == 11

    def testTimeParsedCorrectly(self):
        dateTimeObject = get_datetime("2022-05-11T10:45:32.000Z")
        assert dateTimeObject.hour == 10

    def testDateTimeCoverterFormatOne(self):
        dateTimeObject = get_datetime("2022-05-11T10:45:32")
        assert dateTimeObject == datetime(2022, 5, 11, 10, 45, 32)

    def testDateTimeCoverterFormatTwo(self):
        dateTimeObject = get_datetime("2022-05-11 10:45:32")
        assert dateTimeObject == datetime(2022, 5, 11, 10, 45, 32)

    def testDateTimeCoverterFormatThree(self):
        dateTimeObject = get_datetime("2022-05-11T10:45:32.000")
        assert dateTimeObject == datetime(2022, 5, 11, 10, 45, 32)

    def testDefault(self):
        dateTimeObject = get_datetime("2022")
        assert dateTimeObject == datetime(2011, 11, 4, 0, 0)
