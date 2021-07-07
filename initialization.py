from data_processing import (
    coordinates_of_city_center,
    get_geohash_for_df,
    parallelize_dataframe,
    split_and_save_updated_dataframe,
)
from postprocessing import save_all_results_to_csv
from preprocessing import (
    data_cleaning,
    get_dataframe_with_top_cities,
    unpacking_zip_file,
)
from weather import generate_plots, transform_dict_into_dataframe


def initialize_program(data: str, output_dir: str):
    """
    Initializes program.
    """
    dataframe = unpacking_zip_file(data)
    clean_dataframe = data_cleaning(dataframe)
    df_with_top_cities = get_dataframe_with_top_cities(clean_dataframe)
    df_with_geohash = parallelize_dataframe(df_with_top_cities, get_geohash_for_df)
    split_and_save_updated_dataframe(df_with_geohash, output_dir)
    geolocations = coordinates_of_city_center(df_with_top_cities)
    days_with_temp = transform_dict_into_dataframe(geolocations)
    save_all_results_to_csv(days_with_temp, output_dir)
    generate_plots(days_with_temp, output_dir)
