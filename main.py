import csv
import re
import datetime

from os.path import join

import gc

from utils.jalali import *
import pickle as pkl

data_path = 'data'
if __name__ == '__main__':
    # parcels_receive = {}
    # with open(join(data_path, 'parcel_info.csv'), newline='') as file:
    #     csv_reader = csv.reader(file)
    #     for row in csv_reader:
    #         date = Persian(row[3]).gregorian_string('{:04d}-{:02d}-{:02d}')
    #         time = row[4]
    #         start_datetime = datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')
    #         parcels_receive[row[0]] = (row[1], row[2], start_datetime)
    # with open(join(data_path, 'parcel_receive.pkl'), 'wb') as file:
    #     pkl.dump(parcels_receive, file)

    # exchanges = []
    # with open(join(data_path, 'exchange_in.csv'), newline='') as file:
    #     csv_reader = csv.reader(file)
    #     for row in csv_reader:
    #         date = Persian(row[2]).gregorian_string('{:04d}-{:02d}-{:02d}')
    #         time = row[3]
    #         date_time = datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')
    #         exchanges.append((row[0], row[1], date_time, 1))
    # with open(join(data_path, 'exchange_out.csv'), newline='') as file:
    #     csv_reader = csv.reader(file)
    #     for row in csv_reader:
    #         date = Persian(row[2]).gregorian_string('{:04d}-{:02d}-{:02d}')
    #         time = row[3]
    #         date_time = datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')
    #         exchanges.append((row[0], row[1], date_time, 0))
    # print(len(exchanges))
    # with open(join(data_path, 'exchanges.pkl'), 'wb') as file:
    #     pkl.dump(exchanges, file)

    # with open(join(data_path, 'exchanges.pkl'), 'rb') as file:
    #     exchanges = pkl.load(file)
    # parcel_exchanges = {code: list() for code in set([row[0] for row in exchanges])}
    # for row in exchanges:
    #     parcel_exchanges[row[0]].append((row[1], row[2], row[3]))
    # for key in parcel_exchanges.keys():
    #     parcel_exchanges[key].sort(key=lambda tup: tup[1])
    # with open(join(data_path, 'parcel_exchanges.pkl'), 'wb') as file:
    #     pkl.dump(parcel_exchanges, file)

    # with open(join(data_path, 'parcel_receive.pkl'), 'rb') as file:
    #     parcels_receive = pkl.load(file)
    # with open(join(data_path, 'parcel_exchanges.pkl'), 'rb') as file:
    #     parcel_exchanges = pkl.load(file)
    # assert len(parcel_exchanges) == len(parcels_receive)
    # for key in parcel_exchanges.keys():
    #     receive = parcels_receive[key]
    #     parcel_exchanges[key].append((receive[0], receive[2], 1))
    #     parcel_exchanges[key].sort(key=lambda tup: tup[1])
    # with open(join(data_path, 'parcel_exchanges_with_source.pkl'), 'wb') as file:
    #     pkl.dump(parcel_exchanges, file)

    # # Sampling
    # with open(join(data_path, 'parcel_exchanges.pkl'), 'rb') as file:
    #     parcel_exchanges = pkl.load(file)
    # keys = list(parcel_exchanges.keys())[0:100]
    # tmp = {}
    # for key in keys:
    #     tmp[key] = parcel_exchanges[key]
    # with open(join(data_path, 'parcel_exchanges_small.pkl'), 'wb') as file:
    #     pkl.dump(tmp, file)








    # postnode_info = {}
    # with open(join(data_path, 'PostNodes.csv'), newline='', encoding='utf-8') as file:
    #     csv_reader = csv.reader(file)
    #     for row in csv_reader:
    #         postnode_info[row[2]] = (str.strip(row[1], '\ufeff'), str.strip(row[0], '\ufeff'))
    #
    # ignored = set()
    # source = {}
    # dest = {}
    # with open(join(data_path, 'parcel_receive.pkl'), 'rb') as file:
    #     parcel_receive = pkl.load(file)
    # for parcel in parcel_receive.keys():
    #     city = parcel_receive[parcel][1]
    #     dest[parcel] = city
    #
    #     node = parcel_receive[parcel][0]
    #     if node in postnode_info.keys():
    #         city = postnode_info[node][1]
    #         source[parcel] = city
    #     else:
    #         ignored.add(parcel)
    # parcel_receive = None
    # gc.collect()
    #
    # both = 0
    # normal = 0
    # returned = 0
    # other = 0
    # with open(join(data_path, 'parcel_exchanges.pkl'), 'rb') as file:
    #     parcel_exchanges = pkl.load(file)
    # for parcel in parcel_exchanges.keys():
    #     if parcel not in ignored:
    #         destId = parcel_exchanges[parcel][-1][0]
    #         destCity = postnode_info[destId][1]
    #         if dest[parcel] == source[parcel]:
    #             both += 1
    #         elif destCity == dest[parcel]:
    #             normal += 1
    #         elif destCity == source[parcel]:
    #             returned += 1
    #         else:
    #             other += 1
    #
    #
    # print(both)
    # print(normal)
    # print(returned)
    # print(other)
    # print(len(ignored))

    with open(join(data_path, 'parcel_exchanges.pkl'), 'rb') as file:
        parcel_exchanges = pkl.load(file)

    duplicates = 0
    faults = 0
    exchanges = 0
    beginFault = 0
    endFault = 0
    superFault = 0
    for parcel in parcel_exchanges.keys():
        lastPostnode = -1
        lastState = -1
        for exchange in parcel_exchanges[parcel]:
            if lastState == -1:
                lastPostnode = exchange[0]
                lastState = exchange[2]
                # assert lastState == 1
                if lastState == 0:
                    beginFault += 1
                    print('Check this:', parcel)
                continue

            if lastPostnode == exchange[0]:
                if lastState == 1 and exchange[2] == 0:
                    assert True
                elif lastState == exchange[2]:
                    duplicates += 1
                else:
                    superFault += 1
                    print('Super Fault:', parcel)
                    # assert False
            else:
                if lastState == 0 and exchange[2] == 1:
                    exchanges += 1
                elif lastState == 0 and exchange[2] == 0:
                    exchanges += 1
                    faults += 1
                elif lastState == 1 and exchange[2] == 0:
                    exchanges += 1
                    faults += 2
                else:
                    exchanges += 1
                    faults += 1
            lastPostnode = exchange[0]
            lastState = exchange[2]
        exchange = parcel_exchanges[parcel][-1]
        if exchange[2] == 0:
            exchanges += 1
            faults += 1
            endFault += 1
    print('Duplicates:', duplicates)
    print('Faults:', faults)
    print('begin:', beginFault)
    print('end:', endFault)
    print('super:', superFault)
    print('total:', exchanges)

    print('Done.')

    # # Check and remove duplicates
    # parcel_info = {}
    # with open(join(data_path, 'parcel_info.csv'), newline='') as file:
    #     csv_reader = csv.reader(file)
    #     for row in csv_reader:
    #         if row[0] not in parcel_info.keys():
    #             parcel_info[row[0]] = row
    #         else:
    #             old_row = parcel_info[row[0]]
    #             assert old_row[1] == row[1] and old_row[2] == row[2] and old_row[3] == row[3] and old_row[4] == row[4]
    # with open(join(data_path, 'parcel_info_without_duplicate.csv'), 'wt', newline='') as file:
    #     csv_writer = csv.writer(file)
    #     for code in parcel_info.keys():
    #         csv_writer.writerow(parcel_info[code])

    # in_list = []
    # with open(join(data_path, 'exchange_out.csv'), newline='') as file:
    #     line = file.readline()
    #     while line:
    #         in_list.append(line)
    #         line = file.readline()
    # in_set = set(in_list)
    # if len(in_list) != len(in_set):
    #     in_new_list = list(in_set)
    #     with open(join(data_path, 'exchange_out_without_duplicate.csv'), 'wt', newline='') as file:
    #         for line in in_new_list:
    #             file.write(line)
    # print('Done.')
