import pickle
import csv
import pandas as pd

from os.path import join, isfile


def create_dataframe(dictionary, postnode_info):
    temp_list = []
    for key, value in dictionary.items():
        if len(value) != 0:
            for record in value:
                start = (record[0].time().hour * 60) + record[0].time().minute
                item = (start, start > 840, record[1], record[2], record[3] - (record[2] * 24),
                        record[3], int(key), int(postnode_info[key][0]), int(postnode_info[key][1]))
                temp_list.append(item)
    print(len(temp_list))

    dataframe = pd.DataFrame(temp_list,
                             columns=['start', 'on_work_time', 'end', 'holiday',
                                      'delay_without_holiday', 'delay', 'postnode_id', 'city_id', 'state_id'])
    return dataframe


if __name__ == '__main__':

    data_path = '../data'
    postnode_delay_data = join(data_path, "postnode_delay.pkl")

    if isfile(postnode_delay_data):
        with open(postnode_delay_data, 'rb') as postnode_delay_file:
            postnode_timedelta = pickle.load(postnode_delay_file)

        postnode_info_path = join(data_path, 'postnodes_info.csv')
        postnode_info = {}
        with open(postnode_info_path) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                postnode_info[row[2]] = (row[0], row[1], row[3], row[5])

    df = create_dataframe(postnode_timedelta, postnode_info)
    print("DELAY WITHOUT HOLIDAY:")
    print("Corr With Start: " + str(df['start'].corr(df['delay_without_holiday'])))
    print("Corr With Holiday: " + str(df['holiday'].corr(df['delay_without_holiday'])))
    print("Corr With PostNode ID: " + str(df['postnode_id'].corr(df['delay_without_holiday'])))
    print("Corr With Office hours: " + str(df['on_work_time'].corr(df['delay_without_holiday'])))
    print("Corr With City ID: " + str(df['city_id'].corr(df['delay_without_holiday'])))
    print("Corr With State ID: " + str(df['state_id'].corr(df['delay_without_holiday'])))

    print("DELAY:")
    print("Corr With Start: " + str(df['start'].corr(df['delay'])))
    print("Corr With Holiday: " + str(df['holiday'].corr(df['delay'])))
    print("Corr With PostNode ID: " + str(df['postnode_id'].corr(df['delay'])))
    print("Corr With Office hours: " + str(df['on_work_time'].corr(df['delay'])))
    print("Corr With City ID: " + str(df['city_id'].corr(df['delay'])))
    print("Corr With State ID: " + str(df['state_id'].corr(df['delay'])))
