import csv
import datetime
import logging
import pickle
from os.path import join, isfile

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import Conv

logger = logging.getLogger(__name__)

def secs2timestring(x, pos):
    """
    Formatter for date box plot
    :param x: value
    :param pos: tick position
    :return: returns Persian date in 'YYYY/MM/DD' format
    """
    # The two args are the value and tick position
    hour=int(x/3600)
    if hour<10:
        h_str="0"+str(hour)
    else:
        h_str=str(hour)

    minute= int((x-(hour*3600))/60)

    if minute<10:
        m_str="0"+str(minute)
    else:
        m_str=str(minute)

    second= int(((x-(hour*3600))-minute*60))

    if second<10:
        s_str="0"+str(second)
    else:
        s_str=str(second)
    return str(h_str + ":" + m_str + ":" + s_str)


def string2time(str):
    """
    create datetime with today date and time from str
    :param str: time
    :return: datetime
    """
    time = str.split(":")
    # The two args are the value and tick position
    return datetime.datetime.now().replace(hour=int(time[0]), minute=int(time[1]), second=int(time[2]), microsecond=0)


if __name__ == '__main__':
    logging.basicConfig(filename='logs/delivery_time_dispersion.log',
                        filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    data_path = 'data'
    parcel_info_path = join(data_path, 'parcel_info.csv')
    delivery_path = join(data_path, 'delivery.csv')

    times_string = []
    time_sec = []
    times = []
    dates_path = join(data_path, 'times.pkl')
    if isfile(dates_path):
        logger.info('Loading from file...')
        with open(dates_path, 'rb') as dates_file:
            times_string, time_sec = pickle.load(dates_file)
    else:
        logger.info('Computing data')
        with open(delivery_path) as csv_file:
            csv_reader = csv.reader(csv_file)
            start_time = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            index = 0
            for row in csv_reader:
                if index % 50 == 0:
                    times_string.append(row[8])
                    time = (string2time(row[8]))
                    times.append(time)
                    time_sec.append((time - start_time).total_seconds())
                index += 1
            with open(dates_path, 'wb') as dates_file:
                pickle.dump((times_string, time_sec), dates_file)
            logger.info('Saving to file...')
    logger.info('Data is ready.')

    times_string.sort()
    size = len(times_string)
    #
    # DATE_MEDIAN = 0
    # DATE_Q1 = 0
    # DATE_Q3 = 0
    #
    # DATE_MEDIAN = times_string[int((size / 2) + 1)]
    # DATE_Q1 = times_string[int((size / 4) + 1)]
    # DATE_Q3 = times_string[int(((size / 4) * 3) + 1)]
    # DATE_START = times_string[0]
    # DATE_END = times_string[int(len(times_string) - 1)]
    #
    # Date_IQR = times_string[(int((size / 4) + 1)):(int(((size / 4) * 3) + 1))]
    #
    # print(DATE_START)
    # print(DATE_Q1)
    # print(DATE_MEDIAN)
    # print(DATE_Q3)
    # print(DATE_END)

    logger.info('Plotting...')
    formatter = FuncFormatter(secs2timestring)
    fig, plts = plt.subplots(1, 2)



    '''
    wspace # the amount of width reserved for blank space between subplots
    '''
    plt.subplots_adjust(left=0.2, wspace=2,top=0.8)
    plt.suptitle('Parcel\'s Delivery Time Dispersion Box Plot', fontsize=16)

    ax = plt.gca()


    plts[0].boxplot(time_sec, notch=1)
    plts[0].set_title('Clean')
    plts[0].set_ylim(9*3600, 15*3600)
    plts[0].yaxis.set_major_formatter(formatter)
    plts[0].set_ylabel('Time')

    plts[1].boxplot(time_sec)
    plts[1].set_title('!Clean')
    plts[1].yaxis.set_major_formatter(formatter)


    plt.show()
    plt.savefig('time.eps', format='eps', dpi=600)
