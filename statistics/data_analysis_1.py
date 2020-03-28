import pandas as pd

df_deaths = pd.read_csv("data/deaths.csv")
df_cases = pd.read_csv("data/cases.csv")
df_recoveries = pd.read_csv("data/recoveries.csv")


def calc_sum(df, column):
    result = 0
    for i in range(0, len(df.values)):
        result += int(df.values[i][column])
    return result


def get_deaths():
    calc_sum(df_deaths, -1)
    
    
def get_cases():
    calc_sum(df_cases, -1)

    
def get_recoveries():
    calc_sum(df_recoveries, -1)

