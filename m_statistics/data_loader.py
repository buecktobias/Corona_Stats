import requests
from threading import Timer
import Corona_Stats.settings as settings
import os

URL_Data = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
URL_recoveries = URL_Data + "time_series_covid19_recovered_global.csv"
URL_deaths = URL_Data + "time_series_covid19_deaths_global.csv"
URL_cases = URL_Data + "time_series_covid19_confirmed_global.csv"

DATA_FOLDER = settings.DATA_FOLDER_PATH

CASES_FILE_NAME = os.path.join(DATA_FOLDER, "cases.csv")
RECOVERIES_FILE_NAME = os.path.join(DATA_FOLDER, "recoveries.csv")
DEATHS_FILE_NAME = os.path.join(DATA_FOLDER, "deaths.csv")

urls_file = [(URL_cases, CASES_FILE_NAME),
             (URL_recoveries, RECOVERIES_FILE_NAME),
             (URL_deaths, DEATHS_FILE_NAME)]


def download(url, file_name):
    text = requests.get(url).text
    with open(file_name, "w") as file:
        file.write(text)


def download_all_files():
    for url, file_name in urls_file:
        download(url, file_name)


def always_update():
    download_all_files()
    t = Timer(1 * 60 * 60, always_update)  # calls itself every hour
    t.start()


if __name__ == '__main__':
    download_all_files()
