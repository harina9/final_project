import datetime
import json
import math
import urllib.request as req
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def get_current_and_next_seven_days_weather_data(latitude: str, longitude: str) -> dict:
    """
    Gets todays temperature and temp for 5 future days for each city.
    :return: dicts with jsons info with past five days weather data.
    """
    api_key = "b205018c387102aaeb72cce9e7fd7730"
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units={}&exclude={}&appid={}"
    units_of_measure = "metric"
    exclude_params = "current,minutely,hourly,alerts"

    with req.urlopen(
        url.format(latitude, longitude, units_of_measure, exclude_params, api_key)
    ) as session:
        response = session.read().decode()
        data = json.loads(response)

    return data


def get_past_five_days_weather_data(latitude: str, longitude: str) -> list:
    """
    Gets past five days temperature for each city.
    :return: list of jsons with past five days weather data.
    """

    api_key = "b205018c387102aaeb72cce9e7fd7730"
    url = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={}&lon={}&dt={}&units={}&appid={}"

    jsons = []
    for i in range(1, 6):
        previous_date = math.floor(
            (datetime.datetime.today() - datetime.timedelta(days=i)).timestamp()
        )
        units_of_measure = "metric"

        with req.urlopen(
            url.format(latitude, longitude, previous_date, units_of_measure, api_key)
        ) as session:
            response = session.read().decode()
        data = json.loads(response)
        jsons.append(data)

    return jsons


def get_max_and_min_temp_for_today_and_next_5_days(
    latitude: str, longitude: str
) -> dict:
    """
    Gets dict with the info for each day about mix and max temperature.
    :return: dictionary with weather data for each day.
    """

    our_dict = get_current_and_next_seven_days_weather_data(latitude, longitude)
    new_dict = {}

    for i in range(6):
        value_dict = {}
        new_data = int(our_dict["daily"][i]["dt"])
        normal_data = datetime.datetime.utcfromtimestamp(new_data).strftime("%Y-%m-%d")
        new_dict[normal_data] = None
        value_dict["minimum"] = our_dict["daily"][i]["temp"]["min"]
        value_dict["maximum"] = our_dict["daily"][i]["temp"]["max"]
        new_dict[normal_data] = value_dict

    return new_dict


def get_max_and_min_temp_for_previous_5_days(latitude: str, longitude: str) -> dict:
    """
    Gets dict with the info for each day about mix and max temperature.
    :return: dictionary with weather data for each day.
    """
    our_list = get_past_five_days_weather_data(latitude, longitude)

    list_of_temp_per_hour = []
    for i in range(5):
        days_temp_list = []
        list_of_temp_per_hour.append(days_temp_list)
        for j in range(24):
            days_temp = our_list[i]["hourly"][j]["temp"]
            days_temp_list.append(days_temp)

    list_with_dates = []
    for i in range(5):
        new_data = datetime.datetime.utcfromtimestamp(
            our_list[i]["current"]["dt"]
        ).strftime("%Y-%m-%d")
        list_with_dates.append(new_data)

    list_with_max_min_temp = []
    for j in list_of_temp_per_hour:
        full_list = {"minimum": min(j), "maximum": max(j)}
        list_with_max_min_temp.append(full_list)

    return dict(zip(list_with_dates, list_with_max_min_temp))


def transform_dict_into_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes dataframe with the info about cities' central coordinates and
    makes dataframe with info about each day for most popular cities.
    """
    new_df = df.astype({"Latitude": "str", "Longitude": "str"})

    info_temp = {}
    for index, row in new_df.iterrows():
        max_min_next_days = get_max_and_min_temp_for_today_and_next_5_days(
            row["Latitude"], row["Longitude"]
        )
        max_min_previous_days = get_max_and_min_temp_for_previous_5_days(
            row["Latitude"], row["Longitude"]
        )
        info_temp[row["City"]] = {**max_min_next_days, **max_min_previous_days}

    return pd.DataFrame(info_temp).T


def generate_plots(df: pd.DataFrame, output_dir: str) -> None:
    """
    Generates plots of min and max temperature range for each city and saves them into directory.
    """
    days = df.columns.values
    for index, row in df.iterrows():
        city_name = index

        path_to_plot = Path(f"{output_dir}/{city_name}/")
        path_to_plot.mkdir(parents=True, exist_ok=True)

        minimum_temp = []
        for i in row:
            minimum_temp.append(i["minimum"])
        plt.figure()
        plt.plot(days, minimum_temp)
        plt.xticks(rotation=20)
        plt.xlabel("Days")
        plt.ylabel("Degrees")
        plt.savefig(path_to_plot / f"{city_name}_min_temperature.png")

        maximum_temp = []
        for i in row:
            maximum_temp.append(i["maximum"])
        plt.figure()
        plt.plot(days, maximum_temp)
        plt.xticks(rotation=20)
        plt.xlabel("Days")
        plt.ylabel("Degrees")
        plt.savefig(path_to_plot / f"{city_name}_max_temperature.png")
