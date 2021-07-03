import zipfile
from collections import Counter

import pandas as pd


def unpacking_zip_file(path: str) -> pd.DataFrame:
    """
    Get DataFrame from csv file.
    :param path: string with the path to csv file.
    :return: DataFrame with the data.
    """
    with zipfile.ZipFile(path) as z:
        data = []
        for file in z.namelist():
            data.append(pd.read_csv(z.open(file), delimiter=","))

    return pd.concat(data, ignore_index=True)


def data_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get cleaned DataFrame from any unnecessary data.
    :param df: dataframe with noisy data.
    :return: DataFrame with the clean data.
    """
    df["Latitude"] = (
        df["Latitude"]
        .astype("str")
        .str.extract(r"^(-?\d+\.\d+)", expand=False)
        .astype(float)
    )
    df["Longitude"] = (
        df["Longitude"]
        .astype("str")
        .str.extract(r"^(-?\d+\.\d+)", expand=False)
        .astype(float)
    )
    res = df.drop(df[(df["Latitude"] > 90)].index)
    res_1 = res.drop(res[res["Latitude"] < -90].index)
    res_2 = res_1.drop(res_1[res_1["Longitude"] < -180].index)
    res_3 = res_2.drop(res_2[res_2["Longitude"] > 180].index)
    res_3 = res_3.dropna(axis=0, how="any")
    return res_3.reset_index(drop=True)


def get_most_common(series: pd.Series) -> pd.Series:
    """
    Find the most common value in series.
    :param series: series.
    :return: series of the most common value.
    """
    x = list(series)
    my_counter = Counter(x)
    return my_counter.most_common(1)[0][0]


def get_dataframe_with_top_cities(df: pd.DataFrame) -> pd.DataFrame:
    """
    Finds most popular cities in grouped dataframe by country.
    :param df: dataframe with all the cities.
    :return: dataframe with only most popular cities.
    """
    cities = df.groupby(["Country"]).agg(get_most_common)["City"]
    return df[df["City"].isin(cities)].sort_values(["City"]).reset_index(drop=True)
