from m_statistics.data_analysis_1 import DataAnalysis
from Corona_Stats import settings
import os
import pandas as pd

EUROPE = "EU"
AFRICA = "AF"
ASIA = "AS"
NORTH_AMERICA = "NA"
SOUTH_AMERICA = "SA"
AUSTRALIA = "OC"
continent_coordinates = {
    EUROPE: (53.5775, 23.106),
    AFRICA: (5.3, 21.2),
    SOUTH_AMERICA: (-11, -61),
    NORTH_AMERICA: (42, -104),
    ASIA: (37, 85),
    AUSTRALIA: (-21, 131),
    "World": (0, 0)
}

continent_long_names = {
    EUROPE: "EUROPE",
    AFRICA: "AFRICA",
    ASIA: "ASIA",
    NORTH_AMERICA: "NORTH AMERICA",
    SOUTH_AMERICA: "SOUTH AMERICA",
    AUSTRALIA: "AUSTRALIA",
    "World": "World"
}


def get_continent(country):
    with open("countries.csv", "r") as countries_file:
        for line in countries_file:
            elements = line.split(",")
            l_country = elements[4]
            l_continent = elements[-2]
            if l_country == country:
                return l_continent


def create_continent_data_for_corona_map():
    da: DataAnalysis = DataAnalysis()
    da.update()
    dfs = [
        {"file_name": os.path.join(settings.STATIC_FOLDER_PATH, "recoveries_map_data.csv"), "df": da.df_recoveries},
        {"file_name": os.path.join(settings.STATIC_FOLDER_PATH, "cases_map_data.csv"), "df": da.df_cases},
        {"file_name": os.path.join(settings.STATIC_FOLDER_PATH, "deaths_map_data.csv"), "df": da.df_deaths}
    ]

    for df_dict in dfs:
        df = df_dict["df"]
        continents_dict = {
            EUROPE: 0,
            ASIA: 0,
            AFRICA: 0,
            AUSTRALIA: 0,
            NORTH_AMERICA: 0,
            SOUTH_AMERICA: 0,
        }

        for row in df.values:
            region = row[0]
            country = row[1]
            most_recent_value = row[-1]
            continent = get_continent(country)
            if continent in continents_dict:
                continents_dict[continent] += most_recent_value

        continents_dict["World"] = sum(continents_dict.values())

        with open(df_dict["file_name"], "w") as file:
            for continent, amount in continents_dict.items():
                coords = continent_coordinates[continent]
                continent_long_name = continent_long_names[continent]
                file.write(f"{continent_long_name}, {amount}, {str(coords[0])}, {str(coords[1])} \n")


def create_country_stack():
    da = DataAnalysis()
    df_cases: pd.DataFrame = da.df_cases
    # country_name: {value: ..., lat: ..., lng: ...}
    countries = {}
    for row in df_cases.values:
        country = {}
        cases_value = row[-1]
        country_name = row[1]
        country_lat = row[2]
        country_lng = row[3]

        if country_name in countries:
            countries[country_name]["value"] += cases_value
        else:
            country["value"] = cases_value
            country["lat"] = country_lat
            country["lng"] = country_lng

            countries[country_name] = country
    print(countries)

if __name__ == '__main__':
    create_continent_data_for_corona_map()
