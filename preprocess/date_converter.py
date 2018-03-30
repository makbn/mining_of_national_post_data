import csv

from utils import jalali
from os.path import join

data_path = '../data'
if __name__ == '__main__':
    exchanges = []
    with open(join(data_path, 'exchange_out.csv'), newline='') as exchanges_file:
        csv_reader = csv.reader(exchanges_file)
        for row in csv_reader:
            exchanges.append(row)

    dates = []
    times = []
    for row in exchanges:
        date, time = row[2].split()
        dates.append(jalali.Gregorian(date).persian_string('{:04d}/{:02d}/{:02d}'))
        time = time.split('.')[0]
        times.append(time)

    assert len(dates) == len(exchanges)
    with open(join(data_path, 'exchange_out_new.csv'), mode='w', newline='') as exchanges_file:
        csv_writer = csv.writer(exchanges_file)
        for i in range(len(exchanges)):
            row = exchanges[i]
            csv_writer.writerow([row[0], row[1], dates[i], times[i]])
