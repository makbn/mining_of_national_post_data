import pickle
import csv
import pandas as pd
import statistics as s

from os.path import join, isfile


def get_delay_mean(dictionary, postnode_info):
    means = {}
    means_city = {}
    means_state = {}

    for key, value in dictionary.items():
        if len(value) != 0:
            delay_sum = 0
            count = 0
            for record in value:
                delay_sum += record[3]
                count += 1
            means[key] = delay_sum/count
            city_key = postnode_info[key][3]
            if city_key not in means_city.keys():
                means_city[city_key] =[delay_sum/count]
            else:
                means_city[city_key].append(delay_sum/count)
            state_key = postnode_info[key][1]
            if state_key not in means_state.keys():
                means_state[state_key] = [delay_sum/count]
            else:
                means_state[state_key].append(delay_sum/count)

    data_path = '../data'
    means_path = join(data_path, "postnode_delay_mean.csv")
    with open(means_path, 'wt') as mean_file:
        csvw = csv.writer(mean_file)
        for k , v in means.items():
            csvw.writerow([k, v])
    city_means_path = join(data_path, "city_delay_mean.csv")
    with open(city_means_path, 'wt') as mean_file:
        csvw = csv.writer(mean_file)
        for k, v in means_city.items():
            csvw.writerow([k, s.mean(v)])
    state_means_path = join(data_path, "state_delay_mean.csv")
    with open(state_means_path, 'wt') as mean_file:
        csvw = csv.writer(mean_file)
        for k, v in means_state.items():
            csvw.writerow([k, s.mean(v)])




if __name__ == '__main__':

    data_path = '../data'
    postnode_delay_data = join(data_path, "postnode_delay_1.pkl")

    if isfile(postnode_delay_data):
        with open(postnode_delay_data, 'rb') as postnode_delay_file:
            postnode_timedelta = pickle.load(postnode_delay_file)

        postnode_info_path = join(data_path, 'postnodes_info.csv')
        postnode_info = {}
        with open(postnode_info_path) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                #city-state-postnode-type-pn-en
                postnode_info[row[2]] = (row[0], row[1], row[3], row[5])

        get_delay_mean(postnode_timedelta,postnode_info)
