import StringIO
import csv
import numpy as np
import math
import matplotlib.pyplot as plt

closing_prices = list()
closing_VIX = list()

with open('./sp500.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        closing_prices.append(float(row['Close']))

with open('./vix.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        closing_VIX.append(float(row['Close']))

diff_array = np.empty(len(closing_prices)-1, dtype=object)

for x in range(0, len(closing_prices)-1):
    diff_array[x] = math.log(closing_prices[x]/closing_prices[x+1])

def find_stdev(dayN, time_frame):
    return np.std(diff_array[dayN-time_frame:dayN+1])

hv_21_days = np.empty(len(diff_array))
hv_63_days = np.empty(len(diff_array))
hv_126_days = np.empty(len(diff_array))

def find_21_days_hv():
    for x in range(20, len(closing_prices) - 1):
        hv_21_days[x] = np.sqrt(252) * find_stdev(x, 20)

def find_63_days_hv():
    for x in range(62, len(closing_prices) - 1):
        hv_63_days[x] = np.sqrt(252) * find_stdev(x, 62)

def find_126_days_hv():
    for x in range(125, len(closing_prices) - 1):
        hv_126_days[x] = np.sqrt(252) * find_stdev(x, 125)

mean_hv = np.mean(hv_21_days)
mean_iv = np.mean(closing_VIX)
closing_VIX = [x / 140 for x in closing_VIX]

find_21_days_hv()
find_63_days_hv()
find_126_days_hv()
plt.plot(hv_21_days)
plt.plot(hv_63_days)
plt.plot(hv_126_days)
plt.plot(closing_VIX)
plt.ylabel('Volatility')
plt.xlabel('day')
plt.show()