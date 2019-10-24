import pickle
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from os.path import join, isfile

from sklearn.svm import SVR


def get_predict_delay_model(post_node_list):


    # Load the diabetes dataset


    # Split the data into training/testing sets
    diabetes_X_train = post_node_list[:-(len(post_node_list)//2)]
    diabetes_X_test = post_node_list[-(len(post_node_list)//2):]

    print(str(len(diabetes_X_train)))
    print(str(len(diabetes_X_test)))

    # Split the targets into training/testing sets
    diabetes_y_train = [postnode[4] for postnode in diabetes_X_train]
    diabetes_y_test = [postnode[4] for postnode in diabetes_X_test]

    # diabetes_X_train = [(record[0], record[2], record[5], record[6], record[7]) for record in diabetes_X_train]
    # diabetes_X_test = [(record[0], record[2], record[5], record[6], record[7]) for record in diabetes_X_test]
    diabetes_X_train = np.asarray([record[0] for record in diabetes_X_train])
    diabetes_X_test = np.asarray([record[0] for record in diabetes_X_test])
    diabetes_X_train = diabetes_X_train.reshape((-1, 1))
    diabetes_X_test = diabetes_X_test.reshape((-1, 1))

    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(diabetes_X_train, diabetes_y_train)

    # Bijan
    svr = SVR(kernel='rbf')
    svr.fit(diabetes_X_train, diabetes_y_train)

    # Make predictions using the testing set
    diabetes_y_pred = regr.predict(diabetes_X_test)
    diabetes_y_pred = svr.predict(diabetes_X_test)

    # The coefficients
    print('Coefficients: \n', regr.coef_)
    # The mean squared error
    print("Mean squared error: %.2f"
          % mean_squared_error(diabetes_y_test, diabetes_y_pred))
    # print("Score: "+regr)
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % r2_score(diabetes_y_test, diabetes_y_pred))
    print(svr.score(diabetes_X_test, diabetes_y_test))

    print(diabetes_y_pred)
    print(diabetes_y_test)
    # Plot outputs
    #start_test = [postnode[0] for postnode in diabetes_X_test]
    plt.scatter(diabetes_X_test, diabetes_y_test, color='black')
    plt.plot(diabetes_X_test, diabetes_y_pred, color='blue', linewidth=1)

    plt.xticks(())
    plt.yticks(())

    plt.show()


def create_list(dictionary, postnode_info):
    temp_list = []
    for key, value in dictionary.items():
        if len(value) != 0:
            for record in value:
                start = (record[0].time().hour * 60) + record[0].time().minute
                item = (start,
                        start > 840,
                        record[2],
                        record[3] - (record[2] * 24),
                        record[3],
                        int(key),
                        int(postnode_info[key][0]),
                        int(postnode_info[key][1]))
                temp_list.append(item)
    return temp_list


def create_dataframe(dictionary, postnode_info):
    temp_list = create_list(dictionary,postnode_info)

    dataframe = pd.DataFrame(temp_list,
                             columns=['start', 'on_work_time',  'holiday',
                                      'delay_without_holiday', 'delay', 'postnode_id', 'city_id', 'state_id'])
    return dataframe


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
                postnode_info[row[2]] = (row[0], row[1], row[3], row[5])

    # df = create_dataframe(postnode_timedelta, postnode_info)
    # print("DELAY WITHOUT HOLIDAY:")
    # print("Corr With Start: " + str(df['start'].corr(df['delay_without_holiday'])))
    # print("Corr With Holiday: " + str(df['holiday'].corr(df['delay_without_holiday'])))
    # print("Corr With PostNode ID: " + str(df['postnode_id'].corr(df['delay_without_holiday'])))
    # print("Corr With Office hours: " + str(df['on_work_time'].corr(df['delay_without_holiday'])))
    # print("Corr With City ID: " + str(df['city_id'].corr(df['delay_without_holiday'])))
    # print("Corr With State ID: " + str(df['state_id'].corr(df['delay_without_holiday'])))
    #
    # print("DELAY:")
    # print("Corr With Start: " + str(df['start'].corr(df['delay'])))
    # print("Corr With Holiday: " + str(df['holiday'].corr(df['delay'])))
    # print("Corr With PostNode ID: " + str(df['postnode_id'].corr(df['delay'])))
    # print("Corr With Office hours: " + str(df['on_work_time'].corr(df['delay'])))
    # print("Corr With City ID: " + str(df['city_id'].corr(df['delay'])))
    # print("Corr With State ID: " + str(df['state_id'].corr(df['delay'])))
    c=0
    postnode_timedelta_s={}
    for k,v in postnode_timedelta.items():
        if c%20==0:
            postnode_timedelta_s[k]=v
        c += 1

    pred = get_predict_delay_model(create_list(postnode_timedelta_s, postnode_info))


