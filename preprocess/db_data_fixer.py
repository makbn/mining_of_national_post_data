import csv
import re

if __name__ == '__exchange_fixer__':
    exchange_in = []
    with open('data/exchange_in.csv', mode='rt', newline='\r\n', encoding='utf-8') as exchange_in_file:
        for line in exchange_in_file:
            line = line.rstrip('\'\r\n')
            parts = line.split('؛')
            for i in range(len(parts)):
                parts[i] = parts[i].strip('\ufeff')
                parts[i] = parts[i].strip()
            exchange_in.append([parts[0], parts[1], parts[2]])

    with open('data/exchange_in_new.csv', newline='', mode='w') as csv_file:
        writer = csv.writer(csv_file)
        for row in exchange_in:
            writer.writerow(row)

if __name__ == '__parcel_info_fixer__':
    parcel_info = []
    with open('data/parcel_info.csv', mode='rt', newline='\r\n', encoding='utf-8') as exchange_in_file:
        for line in exchange_in_file:
            line = line.rstrip('\'\r\n')
            parts = line.split('؛')
            for i in range(len(parts)):
                parts[i] = parts[i].strip('\ufeff')
                parts[i] = parts[i].strip()
            parcel_info.append([parts[0], parts[1], parts[2], parts[3], parts[4]])

    with open('data/parcel_info_new.csv', newline='', mode='w') as csv_file:
        writer = csv.writer(csv_file)
        for row in parcel_info:
            writer.writerow(row)

if __name__ == '__delivery_fixer__':
    delivery = []
    with open('data/delivery.csv', mode='rt', newline='\r\n', encoding='utf-8') as exchange_in_file:
        for line in exchange_in_file:
            line = line.rstrip('\'\r\n')
            parts = line.split('؛')
            for i in range(len(parts)):
                parts[i] = parts[i].strip('\ufeff')
                parts[i] = parts[i].strip()
            delivery.append([parts[0], parts[1], parts[8], parts[9], parts[2], parts[3], parts[4], parts[5], parts[6], parts[7]])

    with open('data/delivery_new.csv', newline='', mode='w') as csv_file:
        writer = csv.writer(csv_file)
        for row in delivery:
            writer.writerow(row)

if __name__ == '__parcel_info_stats__':
    data = []
    with open('data/parcel_info.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            data.append(row)

    rows = []
    for row in data:
        rows.append(row[0])
    print('parcels = {}'.format(len(set(rows))))

    # Date
    rows = []
    for row in data:
        rows.append(row[3])
    print('date min = {}'.format(min(rows)))
    print('date max = {}'.format(max(rows)))

    # Time
    rows = []
    for row in data:
        rows.append(row[4])
    print('time min = {}'.format(min(rows)))
    print('time max = {}'.format(max(rows)))

if __name__ == '__delivery_stats__':
    data = []
    with open('data/delivery.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            data.append(row)

    # rows = []
    # for row in data:
    #     rows.append(row[0])
    # print('rows = {}'.format(len(rows)))
    # print('parcels = {}'.format(len(set(rows))))
    #
    # # Date
    # rows = []
    # for row in data:
    #     rows.append(row[5])
    # print('date min = {}'.format(min(rows)))
    # print('date max = {}'.format(max(rows)))
    #
    # # Time
    # rows = []
    # for row in data:
    #     rows.append(row[6])
    # print('time min = {}'.format(min(rows)))
    # print('time max = {}'.format(max(rows)))
    # i = 0
    # for row in rows:
    #     if re.match('[0-9][0-9]:[0-9][0-9]:[0-9][0-9]', row) is None:
    #         print(row)
    #         i += 1
    # print(i)

    # # Delivery Date
    # rows = []
    # for row in data:
    #     rows.append(row[7])
    # print('delivery date min = {}'.format(min(rows)))
    # print('delivery date max = {}'.format(max(rows)))
    # i = 0
    # for row in rows:
    #     if re.match('1396/.*', row) is None:
    #         print(row)
    #         i += 1
    # print('out of range: {}'.format(i))
    # i = 0
    # for row in rows:
    #     if re.match('[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]', row) is None:
    #         print(row)
    #         i += 1
    # print('format mismatch: {}'.format(i))

    # # Delivery Time
    # rows = []
    # for row in data:
    #     rows.append(row[8])
    # print('delivery time min = {}'.format(min(rows)))
    # print('delivery time max = {}'.format(max(rows)))
    # i = 0
    # for row in rows:
    #     if re.match('[0-9][0-9]:[0-9][0-9]:[0-9][0-9]', row) is None:
    #         print(row)
    #         i += 1
    # print(i)

    # Delivery Status
    rows = []
    for row in data:
        rows.append(row[9])
    print('delivery status min = {}'.format(min(rows)))
    print('delivery status max = {}'.format(max(rows)))

if __name__ == '__main__':
    data = []
    with open('data/exchange_out.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            data.append(row)

    rows = []
    for row in data:
        rows.append(row[0])
    print('rows = {}'.format(len(rows)))
    print('parcels = {}'.format(len(set(rows))))

    # Date
    dates = []
    times = []
    for row in data:
        datetime = row[2].split()
        dates.append(datetime[0])
        times.append(datetime[1])
    i = 0
    for date in dates:
        if re.match('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]', date) is None:
            print(date)
            i += 1
    print(i)
    print('date min = {}'.format(min(dates)))
    print('date max = {}'.format(max(dates)))
    i = 0
    for time in times:
        if re.match('[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]', time) is None:
            print(time)
            i += 1
    print(i)
    print('time min = {}'.format(min(times)))
    print('time max = {}'.format(max(times)))

    # # Time
    # rows = []
    # for row in data:
    #     rows.append(row[4])
    # print('time min = {}'.format(min(rows)))
    # print('time max = {}'.format(max(rows)))

    print('Done.')
