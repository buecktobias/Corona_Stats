import pandas as pd
from matplotlib import pyplot as plt
from .data_loader import CASES_FILE, DEATHS_FILE, RECOVERIES_FILE, DATA_FOLDER


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


class DataAnalysis:
    instance = None

    @staticmethod
    def get_instance():
        return DataAnalysis.instance

    def __init__(self):
        if DataAnalysis.instance is None:
            self.DATA_FOLDER = DATA_FOLDER
            self.PLOT_FOLDER = "./main/static/plots/"

            # DATA FILE NAMES
            self.CASES_TIME_SERIES_DATA_FILE = CASES_FILE
            self.RECOVERIES_TIME_SERIES_DATA_FILE = RECOVERIES_FILE
            self.DEATHS_TIME_SERIES_DATA_FILE = DEATHS_FILE

            # DFs
            self.df_deaths = None
            self.df_cases = None
            self.df_recoveries = None

            # time series s
            self.cases_time_series = None
            self.deaths_time_series = None
            self.recoveries_time_series = None
            self.active_cases_time_series = None

            # plot files
            self.CASES_PLOT_FILE = self.PLOT_FOLDER + "cases.svg"
            self.DEATHS_PLOT_FILE = self.PLOT_FOLDER + "deaths.svg"
            self.RECOVERIES_PLOT_FILE = self.PLOT_FOLDER + "recoveries.svg"
            self.ACTIVE_CASES_PLOT_FILE = self.PLOT_FOLDER + "active_cases.svg"

            self.update()

            DataAnalysis.instance = self
        else:
            pass

    def update(self):
        self.__load_dfs()
        self.__load_time_series()
        self.__create_plots()

    def get_deaths(self):
        return calc_sum(self.df_deaths, -1)

    def get_cases(self):
        return calc_sum(self.df_cases, -1)

    def get_recoveries(self):
        return calc_sum(self.df_recoveries, -1)

    def get_active_cases(self):
        return self.get_cases() - self.get_deaths() - self.get_recoveries()

    def __create_plots(self):
        self.__create_active_cases_plot()
        self.__create_cases_plot()
        self.__create_recoveries_plot()
        self.__create_deaths_plot()

    def __load_dfs(self):
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

    def __create_time_series_plot(self, data, title, to_file):
        plt.title(f"COVID-19 {title}")
        plt.xticks(list(range(0, len(self.__get_dates()), 10)))
        plt.plot(self.__get_dates(), data)
        plt.savefig(to_file)

    def __create_cases_plot(self):
        self.__create_time_series_plot(self.cases_time_series, "Cases", self.CASES_PLOT_FILE)

    def __create_deaths_plot(self):
        self.__create_time_series_plot(self.deaths_time_series, "Deaths", self.DEATHS_PLOT_FILE)

    def __create_recoveries_plot(self):
        self.__create_time_series_plot(self.recoveries_time_series, "Recoveries", self.RECOVERIES_PLOT_FILE)
    
    def __create_active_cases_plot(self):
        self.__create_time_series_plot(self.active_cases_time_series, "Active Cases", self.ACTIVE_CASES_PLOT_FILE)
