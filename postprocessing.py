def city_and_day_with_max_temp(df):
    maximum_temp = float("-inf")
    for i in df.values:
        for j in i:
            if j["maximum"] > maximum_temp:
                maximum_temp = j["maximum"]

    return maximum_temp


def city_and_day_with_min_temp(df):
    minimum_temp = float("inf")
    for i in df.values:
        for j in i:
            if j["minimum"] < minimum_temp:
                minimum_temp = j["minimum"]

    return minimum_temp

def city_with_max_range_of_max_tep(df):
    maximum_range = float("-inf")
    for i in df.values:
        i = [j['maximum'] for j in i]
        range_temp = max(i) - min(i)
        if range_temp > maximum_range:
            maximum_range = range_temp

    return maximum_range

def city_and_day_with_max_range_of_min_and_max_temp(df):
    maximum_range_min_max = float("-inf")
    for i in df.values:
        for j in i:
            range_temp = j['maximum'] - j['minimum']
            if range_temp > maximum_range_min_max:
                maximum_range_min_max = round(range_temp, 2)

    return maximum_range_min_max


