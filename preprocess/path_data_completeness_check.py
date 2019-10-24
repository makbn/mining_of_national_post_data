import csv
import pickle
from os.path import join, isfile
import logging


def path_data_completeness_check(exchange_list):
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


def dummy_postnode_check(exchange_list):
    dummies = {}
    state = 1
    last_postnode = -1
    for item in exchange_list:
        if item[2] != state:
            if item[0] not in dummies.keys():
                dummies[item[0]] = 1
            else:
                dummies[item[0]] += 1
        if state == 1:
            last_postnode = item[0]
        else:
            if last_postnode != item[0]:
                if item[0] not in dummies.keys():
                    dummies[item[0]] = 1
                else:
                    dummies[item[0]] += 1
                if last_postnode not in dummies.keys():
                    dummies[last_postnode] = 1
                else:
                    dummies[last_postnode] += 1

        state = (state + 1) % 2
    return dummies


if __name__ == '__main__':
    logging.basicConfig(filename='../logs/path_data_completeness_check.log',
                        filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    data_path = '../data'
    sample_data = join(data_path, 'parcel_exchanges_small.pkl')
    full_data = join(data_path, 'parcel_exchanges.pkl')

    # choose data set
    working_data = full_data
    clean_data={}
    #loading exchange data
    if isfile(working_data):
        with open(working_data, 'rb') as data_file:
            parcel_exchange = pickle.load(data_file)

        postnode_info_path = join(data_path, 'postnodes_info.csv')
        exchanges_cities_path = join(data_path, 'exchanges_cities.csv')
        postnode_info = {}
        exchanges_cities = {}

        # creating postnodes info
        with open(postnode_info_path) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                postnode_info[row[2]] = (row[0], row[1], row[3], row[5])
        # get count of exchange in each city
        with open(exchanges_cities_path) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                exchanges_cities[row[0]] = row[1]
        # fault ratio for each postnode
        fault_postnode = {}

        for parcel_code, values in parcel_exchange.items():
            temp = dummy_postnode_check(values)
            if len(temp) >= 1:
                for postnode, count in temp.items():
                    if postnode not in fault_postnode.keys():
                        fault_postnode[postnode] = count
                    else:
                        fault_postnode[postnode] += count

        fault_postnode = [(k, fault_postnode[k]) for k in sorted(fault_postnode, key=fault_postnode.get, reverse=True)]

        dates_path = join(data_path, 'fault_postnode.pkl')
        if isfile(dates_path):
            with open(dates_path, 'wb') as dummy_file:
                pickle.dump(fault_postnode, dummy_file)

        cities_fault_ratio = {}
        cities_id_fault_ratio = {}
        state_id_fault_ratio = {}
        cities_fault_postnode_count = {}

        for k in fault_postnode:
            if k[0] not  in postnode_info.keys():
                continue
            # get name of city as key
            key = postnode_info[k[0]][3]
            cities_id_fault_ratio[key] = postnode_info[k[0]][0]
            state_id_fault_ratio[key] = postnode_info[k[0]][1]

            if key not in cities_fault_ratio.keys():
                cities_fault_ratio[key] = k[1]
                cities_fault_postnode_count[key] = 1

            else:
                cities_fault_ratio[key] += k[1]
                cities_fault_postnode_count[key] += 1

        for key in cities_fault_ratio.keys():
            if key in exchanges_cities.keys():
                cities_fault_ratio[key] = cities_fault_ratio[key] / int(exchanges_cities[key]);

        cities_fault_ratio = [(k, cities_fault_ratio[k]) for k in sorted(cities_fault_ratio, key=cities_fault_ratio.get, reverse=True)]

        cities_fault_ratio_path=join(data_path, 'cities_fault_ratio_full.csv')
        with open(cities_fault_ratio_path, 'wt', newline='') as csv_file:
            csvw=csv.writer(csv_file)
            for k in cities_fault_ratio:
                print(k[0] + " == "+str(k[1]))
                if k[1]< 1:
                    csvw.writerow([k[0],cities_id_fault_ratio[k[0]],state_id_fault_ratio[k[0]],k[1]])
