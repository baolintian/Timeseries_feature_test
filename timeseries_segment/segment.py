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

if __name__ == "__main__":
    timeseries_name = "N00_KAA_0KAA00CP002@OUT.VAL"
    config_path = "../config/" + timeseries_name
    image_path = "../images/" + timeseries_name
    timeseries_path = "../data/" + timeseries_name + ".csv"
    trend_config, threshold_config, resample_frequency = read_config(config_path)
    timeseries = read_timeseries(timeseries_path, str(resample_frequency) + "min")

    res_temp = pelt(normal_mean(pd.to_numeric(timeseries).values, 10), len(timeseries))
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
