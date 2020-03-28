import pandas as pd
import os


def calc_sum(df, column):
    result = 0
    for i in range(0, len(df.values)):
        result += int(df.values[i][column])
    return result


def get_deaths():
    df_deaths = pd.read_csv("static/data/deaths.csv")
    return calc_sum(df_deaths, -1)
    
    
def get_cases():
    df_cases = pd.read_csv("static/data/cases.csv")
    return calc_sum(df_cases, -1)

    
def get_recoveries():
    df_recoveries = pd.read_csv("static/data/recoveries.csv")
    return calc_sum(df_recoveries, -1)

