import pandas as pd


def calc_sum(df, column):
    result = 0
    for i in range(0, len(df.values)):
        result += int(df.values[i][column])
    return result


DATA_FOLDER = "./main/static/data/"
df_deaths = pd.read_csv(DATA_FOLDER + "deaths.csv")
df_cases = pd.read_csv(DATA_FOLDER + "cases.csv")
df_recoveries = pd.read_csv(DATA_FOLDER + "recoveries.csv")


def get_deaths():
    return calc_sum(df_deaths, -1)


def get_cases():
    return calc_sum(df_cases, -1)

    
def get_recoveries():
    return calc_sum(df_recoveries, -1)


def get_active_cases():
    return get_cases() - get_deaths() - get_recoveries()

