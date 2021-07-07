from multiprocessing import Pool

import numpy as np
import pandas as pd

from monroe import encode


def get_geohash_for_df(df: pd.DataFrame) -> pd.DataFrame:
    df["geohash"] = df.apply(lambda x: encode(x["Latitude"], x["Longitude"]), axis=1)
    return df


def parallelize_dataframe(df: pd.DataFrame, func) -> pd.DataFrame:
    """
    Adds column with address for each hotel with the help of geopy.
    :return: dataframe with new column "Address".
    """
    num_partitions = 10
    num_workers = 4
    df_split = np.array_split(df, num_partitions)
    with Pool(num_workers) as pool:
        df = pd.concat(pool.map(func, df_split))
    return df


def split_and_save_updated_dataframe(df: pd.DataFrame, output_dir: str) -> None:
    """Saves splitted files intro directory."""
    number = 0
    split_number = df.index[-1] / 100
    df_split = np.array_split(df, int(split_number))
    for i in df_split:
        i.to_csv(f"{output_dir}/file{number}.csv")
        number += 1


def coordinates_of_city_center(df: pd.DataFrame) -> pd.DataFrame:
    """
    Finds central coordinates of each city.
    :param df: dataframe with most popular cities.
    :return: dataframe with cities and their central latitude and longitude.
    """
    lat_max = df.groupby(["City"])["Latitude"].max().sort_index()
    lat_min = df.groupby(["City"])["Latitude"].min().sort_index()
    lon_max = df.groupby(["City"])["Longitude"].max().sort_index()
    lon_min = df.groupby(["City"])["Longitude"].min().sort_index()
    central_lat = (lat_max + lat_min) / 2
    central_lon = (lon_max + lon_min) / 2
    return pd.concat([central_lat, central_lon], axis=1).reset_index()
