import  csv

import datetime
import matplotlib.pyplot as plt

import Conv

PARCEL_INFO_PATH = '/Users/makbn/Documents/University/Term 7/Data Mining/Data/data/parcel_info.csv'
DELIVERY_PATH='/Users/makbn/Documents/University/Term 7/Data Mining/Data/data/delivery.csv'

csvFile = open(DELIVERY_PATH, 'rt')

result = csv.reader(csvFile)

date = []
index = 0

index=0
for row in result:
    if index % 5 == 0:
        date.append((Conv.Persian(row[7]).gregorian_datetime()- datetime.datetime(1970,1,1)).total_seconds())
    index += 1;


date.sort()

size = len(date)

DATE_MEDIAN = 0
DATE_Q1 = 0
DATE_Q3 = 0


DATE_MEDIAN = date[int((size/2)+1)]
DATE_Q1 = date[int((size/4)+1)]
DATE_Q3 = date[int(((size/4)*3)+1)]
DATE_START = date[0]
DATE_END = date[int(len(date)-1)]


Date_IQR = date[(int((size/4)+1)):(int(((size/4)*3)+1))]


print(DATE_START)
print(DATE_Q1)
print(DATE_MEDIAN)
print(DATE_Q3)
print(DATE_END)



fig = plt.figure()
plt.boxplot(date)
plt.savefig('date.pdf')
fig.show()






