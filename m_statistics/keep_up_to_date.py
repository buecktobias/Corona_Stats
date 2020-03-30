from threading import Timer
from . import data_loader
from . import data_analysis_1


def keep_up_with_corona():
    data_loader.download_all_files()
    data_analysis: data_analysis_1.DataAnalysis = data_analysis_1.DataAnalysis.get_instance()
    data_analysis.update()
    t = Timer(1 * 60 * 60, keep_up_with_corona)  # calls itself every hour
    t.start()


if __name__ == '__main__':
    keep_up_with_corona()