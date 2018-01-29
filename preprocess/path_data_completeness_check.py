import pickle
from os.path import join, isfile
import logging


def path_data_completeness_check(exchange_list):
    # exchange_list = exchange_list[1:]

    # if len(exchange_list)==2:
    #     return True
    # return False

    state = 1
    last_postnode = -1
    for item in exchange_list:
        if item[2] != state:
            return False
        if state == 1:
            last_postnode = item[0]
        else:
            if last_postnode != item[0]:
                return False
        state = (state + 1) % 2
    print(len(exchange_list))
    return True


if __name__ == '__main__':
    logging.basicConfig(filename='../logs/path_data_completeness_check.log',
                        filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    data_path = '../data'
    sample_data = join(data_path, 'parcel_exchanges_small.pkl')
    full_data = join(data_path, 'parcel_exchanges.pkl')

    # choose data set
    working_data = sample_data
    clean_data={}
    if isfile(working_data):
        with open(working_data, 'rb') as data_file:
            parcel_exchange = pickle.load(data_file)
        count = 0
        for parcel_code in parcel_exchange.keys():
            exchange_list=parcel_exchange.get(parcel_code)
            if path_data_completeness_check(exchange_list):
                clean_data[parcel_code] = exchange_list
                count += 1
        print("Count : " + str(count))
