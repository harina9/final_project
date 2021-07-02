from data_processing import *
from preprocessing import (
    data_cleaning,
    get_dataframe_with_top_cities,
    unpacking_zip_file,
)
from weather import *


def initialize_program(data: str, output_dir: str):
    """
    Gets todays temperature and temp for 5 future days for each city.
    """
    dataframe = unpacking_zip_file(data)
    clean_dataframe = data_cleaning(dataframe)
    df_with_top_cities = get_dataframe_with_top_cities(clean_dataframe)
    geolocations = coordinates_of_city_center(df_with_top_cities)
    days_with_temp = transform_dict_into_dataframe(geolocations)

    generate_plots(geolocations, output_dir)