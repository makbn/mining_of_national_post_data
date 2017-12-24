import csv
import datetime
import logging
import pickle
from os.path import join, isfile

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import Conv

logger = logging.getLogger(__name__)


def days2date(x, pos):
    """
    Formatter for date box plot
    :param x: value
    :param pos: tick position
    :return: returns Persian date in 'YYYY/MM/DD' format
    """
    # The two args are the value and tick position
    return Conv.Gregorian((datetime.datetime(1970, 1, 1) + datetime.timedelta(days=x)).strftime('%Y-%m-%d')) \
        .persian_string('{:04d}/{:02d}/{:02d}')

if __name__ == '__main__':
    logging.basicConfig(filename='logs/example1.log',
                        filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    data_path = 'data'
    parcel_info_path = join(data_path, 'parcel_info.csv')
    delivery_path = join(data_path, 'delivery.csv')

    dates_string = []
    dates_day = []
    dates_path = join(data_path, 'dates.pkl')
    if isfile(dates_path):
        logger.info('Loading from file...')
        with open(dates_path, 'rb') as dates_file:
            dates_string, dates_day = pickle.load(dates_file)
    else:
        logger.info('Computing data')
        with open(delivery_path) as csv_file:
            csv_reader = csv.reader(csv_file)
            index = 0
            for row in csv_reader:
                if index % 50 == 0:
                    dates_string.append(row[7])
                    dates_day.append((Conv.Persian(row[7]).gregorian_datetime() - datetime.datetime(1970, 1, 1)).days)
                index += 1
            for i in range(len(dates_day)):
                days = dates_day[i]
                date1 = Conv.Gregorian((datetime.datetime(1970, 1, 1) + datetime.timedelta(days=days))
                                       .strftime('%Y-%m-%d')).persian_string('{:04d}/{:02d}/{:02d}')
                date2 = dates_string[i]
                assert date1 == date2
            with open(dates_path, 'wb') as dates_file:
                pickle.dump((dates_string, dates_day), dates_file)
            logger.info('Saving to file...')
    logger.info('Data is ready.')

    dates_string.sort()
    size = len(dates_string)

    DATE_MEDIAN = 0
    DATE_Q1 = 0
    DATE_Q3 = 0


    DATE_MEDIAN = dates_string[int((size / 2) + 1)]
    DATE_Q1 = dates_string[int((size / 4) + 1)]
    DATE_Q3 = dates_string[int(((size / 4) * 3) + 1)]
    DATE_START = dates_string[0]
    DATE_END = dates_string[int(len(dates_string) - 1)]

    Date_IQR = dates_string[(int((size / 4) + 1)):(int(((size / 4) * 3) + 1))]

    print(DATE_START)
    print(DATE_Q1)
    print(DATE_MEDIAN)
    print(DATE_Q3)
    print(DATE_END)

    logger.info('Plotting...')
    plt.subplots_adjust(left=0.2)
    ax = plt.gca()
    formatter = FuncFormatter(days2date)
    ax.yaxis.set_major_formatter(formatter)
    plt.boxplot(dates_day)
    plt.ylim(17300, 17450)
    plt.show()
