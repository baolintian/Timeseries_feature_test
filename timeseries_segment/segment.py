import sys
from util import *
from changepy import pelt
from changepy.costs import normal_mean
import pandas as pd
import matplotlib.pyplot as plt

# parameter
normal_std = 10
# 认为一分钟内被分割的点都是在同一段变化的区间
window_size = 60

def sign(value, pre):
    if value > 0:
        return 1
    elif value == 0:
        return pre
    else:
        return 0

def sign1(value):
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0

if __name__ == "__main__":
    timeseries_path = "./tu_1.csv"
    timeseries = read_timeseries(timeseries_path, str(120) + "min")

    res_temp = pelt(normal_mean(pd.to_numeric(timeseries).values, 100), len(timeseries))
    res = []

    start = res_temp[0]
    used = False
    for i in range(1, len(res_temp)):
        if i == len(res_temp)-1:
            used = True
            res.append(start)
            res.append(res_temp[-1])
        elif res_temp[i]-res_temp[i-1] > window_size and not used:
            res.append(start)
            start = res_temp[i]
            used = True
        else:
            used = False


    if not used:
        res.append(start)
    print(res)
    timeseries_value = timeseries.values
    diff1 = []
    diff2 = []
    window_size = 10
    for _, timeseries_value_ in enumerate(timeseries_value):
        if _ == 0:
            continue
        diff2.append(sign1(timeseries_value[_] - timeseries_value[_ - 1]))
        pre = sum(diff2[max(0, _-window_size): _-1])
        if pre > 0:
            pre = 1
        else:
            pre = 0
        diff1.append(sign(timeseries_value[_]-timeseries_value[_-1], pre))


    plt.scatter(range(len(diff1)), diff1)
    plt.show()
