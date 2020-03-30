from threading import Timer

from . import data_loader
from . import plot_creator


def keep_up_with_corona():
    data_loader.download_all_files()
    plot_creator.create_plots()
    t = Timer(1 * 60 * 60, keep_up_with_corona)  # calls itself every hour
    t.start()


if __name__ == '__main__':
    keep_up_with_corona()