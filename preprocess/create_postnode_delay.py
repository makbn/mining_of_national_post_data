import pickle
from os.path import join, isfile
import logging

from utils import time as time_utils


def create_postnode_delay(exchange_list):
    last_postnode = -1
    postnode_time_deltas = {}
    start_datetime = None
    state = -1

    for item in exchange_list:
        if item[2] == 1:
            last_postnode = item[0]
            start_datetime = item[1]
            state = 1
            continue
        if item[2] == 0:
            if last_postnode == item[0]:
                diff = item[1] - start_datetime
                days, seconds = diff.days, diff.seconds
                hours = days * 24 + seconds / 3600
                holidays = time_utils.get_holiday_count_datetime(start_datetime.date(), item[1].date())

                temp = (start_datetime, item[1], holidays, hours)
                if last_postnode not in postnode_time_deltas.keys():
                    postnode_time_deltas[last_postnode] = list()
                postnode_time_deltas[last_postnode].append(temp)
                last_postnode = -1
    return postnode_time_deltas


if __name__ == '__main__':
    logging.basicConfig(filename='../logs/create_postnode_delay.log',
                        filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    data_path = '../data'
    sample_data = join(data_path, 'parcel_exchanges_small.pkl')
    full_data = join(data_path, 'parcel_exchanges.pkl')
    postnode_delay_data = join(data_path,"postnode_delay.pkl")

    # choose data set
    working_data = sample_data
    if isfile(postnode_delay_data):
        with open(postnode_delay_data, 'rb') as postnode_delay_file:
            postnode_timedelta = pickle.load(postnode_delay_file)
            for key, value in postnode_timedelta.items():
                if len(value) != 0:
                    print("Postnode ID:" + str(key))
                    print("Min: " + str(value[0][3]) + " Max: " + str(value[-1][3]) + " Holidays: " + str(value[-1][2]))

    elif isfile(working_data):
        with open(working_data, 'rb') as data_file:
            parcel_exchange = pickle.load(data_file)

        postnodes = set()
        for parcel in parcel_exchange.keys():
            postnodes = postnodes.union(set(row[0] for row in parcel_exchange[parcel]))
        postnode_timedelta = {postnode: list() for postnode in postnodes}
        count = 0
        for parcel_code in parcel_exchange.keys():
            exchange_list = parcel_exchange.get(parcel_code)
            postnode_time_delta_list = create_postnode_delay(exchange_list)
            print(str(count+1))
            count += 1
            for key, value in postnode_time_delta_list.items():
                postnode_timedelta.get(key).extend(value)

        for key, value in postnode_timedelta.items():
            if len(value) != 0:
                print("Postnode ID:" + str(key))
                value.sort(key=lambda x: x[3])
                print("Min: " + str(value[0][3])+" Max: " + str(value[-1][3]) + " Holidays: " + str(value[-1][2]))

        with open(postnode_delay_data, 'wb') as postnode_delay_file:
            pickle.dump(postnode_timedelta, postnode_delay_file)
