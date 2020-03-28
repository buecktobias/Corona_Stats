import requests
from threading import Timer

URL_Data = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
URL_recoveries = URL_Data + "time_series_covid19_confirmed_global.csv"
URL_deaths = URL_Data + "time_series_covid19_deaths_global.csv"
URL_cases = URL_Data + "time_series_covid19_confirmed_global.csv"

urls_file = [(URL_cases, "../static/data/cases.csv"), (URL_recoveries, "../static/data/recoveries.csv"), (URL_deaths, "../static/data/deaths.csv")]


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