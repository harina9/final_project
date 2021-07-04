import pandas as pd
import pytest
from preprocessing import data_cleaning
from weather import *

test_latitude = "59.89444"
test_longitude = "30.26417"
future_results = {
    "2021-07-04": {"minimum": 12.88, "maximum": 26.74},
    "2021-07-05": {"minimum": 14.44, "maximum": 28.37},
    "2021-07-06": {"minimum": 14.37, "maximum": 27.69},
    "2021-07-07": {"minimum": 16.52, "maximum": 29.71},
    "2021-07-08": {"minimum": 20.35, "maximum": 29.56},
    "2021-07-09": {"minimum": 19.08, "maximum": 29.56},
}
past_results = {
    "2021-07-03": {"minimum": 11.25, "maximum": 24.34},
    "2021-07-02": {"minimum": 12.9, "maximum": 22.27},
    "2021-07-01": {"minimum": 14.93, "maximum": 23.86},
    "2021-06-30": {"minimum": 15.17, "maximum": 27.04},
    "2021-06-29": {"minimum": 18.54, "maximum": 24.85},
}


def test_max_and_min_temp_for_future_days():
    assert (
        get_max_and_min_temp_for_today_and_next_5_days(test_latitude, test_longitude)
        == future_results
    )


def test_max_and_min_temp_for_past_days():
    assert (
        get_max_and_min_temp_for_previous_5_days(test_latitude, test_longitude)
        == past_results
    )
