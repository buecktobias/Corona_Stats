import pandas as pd
from matplotlib import pyplot as plt
from m_statistics.data_loader import CASES_FILE_NAME, RECOVERIES_FILE_NAME, DEATHS_FILE_NAME
import Corona_Stats.settings as settings
import os
from m_statistics.colors import Color
from datetime import datetime, timedelta
import numpy as np


def calc_sum(df, column):
    result = 0
    for i in range(0, len(df.values)):
        result += int(df.values[i][column])
    return result


def get_all_sums(df):
    ls = []
    for i in range(4, len(df.columns)):
        ls.append(calc_sum(df, i))
    return ls


def get_poly_fit(series, deg):
    x = np.arange(len(series))
    y = np.array(series)
    return np.polyfit(x, y, deg)


def calc_poly(polies, number):
    result = 0
    for power, factor in enumerate(reversed(polies)):
        result += factor * (number ** power)
    return result


class DataAnalysis:
    instance = None

    @staticmethod
    def get_instance():
        return DataAnalysis.instance

    def __init__(self):
        # DATA FILE NAMES
        self.CASES_TIME_SERIES_DATA_FILE = CASES_FILE_NAME
        self.RECOVERIES_TIME_SERIES_DATA_FILE = RECOVERIES_FILE_NAME
        self.DEATHS_TIME_SERIES_DATA_FILE = DEATHS_FILE_NAME

        # DFs
        self.df_deaths = None
        self.df_cases = None

        # DFs
        self.df_deaths = None
        self.df_cases = None
        self.df_recoveries = None

        # time series
        self.cases_time_series = None
        self.deaths_time_series = None
        self.recoveries_time_series = None
        self.active_cases_time_series = None

        # plot files

        self.CASES_PLOT_FILE = os.path.join(settings.PLOT_FOLDER_PATH, "cases.svg")
        self.DEATHS_PLOT_FILE = os.path.join(settings.PLOT_FOLDER_PATH, "deaths.svg")
        self.RECOVERIES_PLOT_FILE = os.path.join(settings.PLOT_FOLDER_PATH, "recoveries.svg")
        self.ACTIVE_CASES_PLOT_FILE = os.path.join(settings.PLOT_FOLDER_PATH, "active_cases.svg")

        # best fit plot files
        self.CASES_POLY_FIT_PLOT_FILE = os.path.join(settings.PLOT_FOLDER_PATH, "cases_poly_fit.svg")
        self.DEATHS_POLY_FIT_PLOT_FILE = os.path.join(settings.PLOT_FOLDER_PATH, "deaths_poly_fit.svg")
        self.RECOVERIES_POLY_FIT_PLOT_FILE = os.path.join(settings.PLOT_FOLDER_PATH, "recoveries_poly_fit.svg")
        self.ACTIVE_CASES_POLY_FIT_PLOT_FILE = os.path.join(settings.PLOT_FOLDER_PATH, "active_cases_poly_fit.svg")

        DataAnalysis.instance = self

    def update(self):
        self.load_dfs()
        self.__load_time_series()
        self.__create_plots()

    def get_deaths(self):
        if self.df_deaths is None:
            self.load_dfs()
        return calc_sum(self.df_deaths, -1)

    def get_cases(self):
        if self.df_cases is None:
            self.load_dfs()
        return calc_sum(self.df_cases, -1)

    def get_recoveries(self):
        if self.df_recoveries is None:
            self.load_dfs()
        return calc_sum(self.df_recoveries, -1)

    def get_active_cases(self):
        return self.get_cases() - self.get_deaths() - self.get_recoveries()

    def __create_plots(self):
        # normal time series
        self.__create_active_cases_plot()
        self.__create_cases_plot()
        self.__create_recoveries_plot()
        self.__create_deaths_plot()

        # best fit line (polynomial fit deg 3)
        self.__create_active_cases_poly_fit_plot()
        self.__create_deaths_poly_fit_plot()
        self.__create_recoveries_poly_fit_plot()
        self.__create_cases_poly_fit_plot()

    def load_dfs(self):
        self.df_deaths = pd.read_csv(self.DEATHS_TIME_SERIES_DATA_FILE)
        self.df_cases = pd.read_csv(self.CASES_TIME_SERIES_DATA_FILE)
        self.df_recoveries = pd.read_csv(self.RECOVERIES_TIME_SERIES_DATA_FILE)

    def __load_time_series(self):
        self.cases_time_series = self.__get_time_series_cases()
        self.deaths_time_series = self.__get_time_series_deaths()
        self.recoveries_time_series = self.__get_time_series_recoveries()
        self.active_cases_time_series = self.__get_time_series_active_cases()

    def __get_time_series_cases(self):
        return get_all_sums(self.df_cases)

    def __get_time_series_deaths(self):
        return get_all_sums(self.df_deaths)

    def __get_time_series_recoveries(self):
        return get_all_sums(self.df_recoveries)

    def __get_time_series_active_cases(self):
        cases = self.__get_time_series_cases()
        deaths = self.__get_time_series_deaths()
        recoveries = self.__get_time_series_recoveries()

        active_cases = []

        for i in range(len(cases)):
            active_cases.append(cases[i] - deaths[i] - recoveries[i])

        return active_cases

    def __get_dates(self):
        return list(self.df_cases.columns[4:])

    def __create_time_series_plot(self, data, title, to_file, color):
        fig, ax = plt.subplots()
        ax.set_title(f"COVID-19 {title}")
        ax.set_xticks(list(range(0, len(self.__get_dates()), 10)))
        ax.plot(self.__get_dates(), data, c=color)
        bg_color = Color.light_background_color
        ax.set_facecolor(bg_color)
        fig.savefig(to_file)

    def __create_cases_plot(self):
        color = Color.cases_color
        self.__create_time_series_plot(self.cases_time_series, "Cases", self.CASES_PLOT_FILE, color)

    def __create_deaths_plot(self):
        color = Color.brand_color
        self.__create_time_series_plot(self.deaths_time_series, "Deaths", self.DEATHS_PLOT_FILE, color)

    def __create_recoveries_plot(self):
        color = Color.recovered_color
        self.__create_time_series_plot(self.recoveries_time_series, "Recoveries", self.RECOVERIES_PLOT_FILE, color)

    def __create_active_cases_plot(self):
        color = Color.active_cases_color
        self.__create_time_series_plot(self.active_cases_time_series, "Active Cases", self.ACTIVE_CASES_PLOT_FILE,
                                       color)

    def longer_dates(self, longer):
        dates = self.__get_dates()
        last_date = dates[-1]
        year = int("20" + last_date.split("/")[2])
        month = int(last_date.split("/")[0])
        day = int(last_date.split("/")[1])
        date = datetime(year, month, day)
        new_dates = []
        for i in range(longer):
            date += timedelta(days=1)
            new_dates.append(date.strftime("%m/%d/%y"))
        return dates + new_dates

    def plot_poly(self, polies, series, to_file, title, legend):
        fig, ax = plt.subplots()
        x = np.arange(len(series))

        forecast_days = 20

        longer_dates_ls = self.longer_dates(forecast_days)

        longer_dates_ls_short = []

        for i in range(0, len(longer_dates_ls), 20):
            longer_dates_ls_short.append(longer_dates_ls[i])

        ax.set_title(title)
        ax.set_xticks(list(range(0, len(series) + forecast_days, 20)))
        ax.set_xticklabels(longer_dates_ls_short)
        ax.scatter(x, series, s=2, c="red", label=legend)

        poly_line_x = np.arange(len(series) + forecast_days)
        poly_line_y = list(map(lambda num: calc_poly(polies, num), poly_line_x))
        ax.plot(poly_line_x, poly_line_y, "--", label="best fit line")
        ax.legend()
        fig.show()
        fig.savefig(to_file)

    def create_active_cases_data(self):
        rows = len(self.df_cases.values)
        columns = len(self.df_cases.values[0])
        # todo create df for active case ???? maybe

    def __create_cases_poly_fit_plot(self):
        self.plot_poly(get_poly_fit(self.cases_time_series, 3), self.cases_time_series, self.CASES_POLY_FIT_PLOT_FILE, "COVID-19 Cases Polynomial Best Fit Line", "Cases")

    def __create_active_cases_poly_fit_plot(self):
        self.plot_poly(get_poly_fit(self.active_cases_time_series, 3), self.active_cases_time_series, self.ACTIVE_CASES_POLY_FIT_PLOT_FILE, "COVID-19 Active Cases Polynomial Best Fit Line", "Active Cases")

    def __create_recoveries_poly_fit_plot(self):
        self.plot_poly(get_poly_fit(self.recoveries_time_series, 3), self.recoveries_time_series, self.RECOVERIES_POLY_FIT_PLOT_FILE, "COVID-19 Recoveries Polynomial Best Fit Line", "Recoveries")

    def __create_deaths_poly_fit_plot(self):
        self.plot_poly(get_poly_fit(self.cases_time_series, 3), self.cases_time_series, self.DEATHS_POLY_FIT_PLOT_FILE, "COVID-19 Deaths Polynomial Best Fit Line", "Deaths")



if __name__ == '__main__':
    DataAnalysis().update()
