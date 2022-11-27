"""
File:           date_time_converter.py
Author:         Ted Jenks
Creation Date:  14/05/2022
Last Edit Date: 14/05/2022
Last Edit By:   Ted Jenks

Functions:      get_datetime(raw_date)

Summary of File:

    Contains functions to convert string to datetime object.
"""

from datetime import datetime
from datetime import date


def get_datetime(raw_date):
    """
    Get the datetime object of the article date

    Args:
        raw_date (str): raw date from article

    Returns:
        datetime: datetime object for article
    """
    print(raw_date)
    try:
        datetime_object = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        try:
            datetime_object = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S.%f")
        except:
            try:
                datetime_object = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S")
            except:
                try:
                    datetime_object = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
                except:
                    try:
                        datetime_object = datetime.strptime(
                            raw_date, "%Y-%m-%dT%H:%M:%S-%f:%f"
                        )
                    except:
                        datetime_object = datetime(2011, 11, 4, 0, 0)
    return datetime_object
