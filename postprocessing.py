def city_and_day_with_max_temp(df):
    maximum_temp = float("-inf")
    for key, value in df.iteritems():
        if value[0]["maximum"] > maximum_temp:
            maximum_temp = value[0]["maximum"]

    return maximum_temp


def city_and_day_with_min_temp(df):
    minimum_temp = float("inf")
    for key, value in df.iteritems():
        if value[0]["minimum"] < minimum_temp:
            minimum_temp = value[0]["minimum"]

    return minimum_temp


# print(city_and_day_with_max_temp(days_with_temp))
# print(city_and_day_with_min_temp(days_with_temp))
