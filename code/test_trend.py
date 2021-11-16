import pytest
from feature_judge import *
from util import *

def test_monotone_increase():
    timeseries_name = "root.CNNP.QF.1#.QF1RCP604MP"
    config_path = "../config/" + timeseries_name
    image_path = "../images/" + timeseries_name
    timeseries_path = "../data/" + timeseries_name + ".csv"
    trend_config, threshold_config, resample_frequency = read_config(config_path)
    timeseries = read_timeseries(timeseries_path, str(resample_frequency) + "min")
    Dplot = 'yes'
    s_tf = trend_features(timeseries, timeseries_name + ".numvalue", trend_config, image_path, Dplot)
    assert s_tf == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]


def test_wave():
    timeseries_name = "wave_test"
    config_path = "../config/" + timeseries_name
    image_path = "../images/" + timeseries_name
    timeseries_path = "../data/" + timeseries_name + ".csv"
    trend_config, threshold_config, resample_frequency = read_config(config_path)
    timeseries = read_timeseries(timeseries_path, str(resample_frequency) + "min")
    Dplot = 'yes'
    s_tf = trend_features(timeseries, timeseries_name, trend_config, image_path, Dplot)
    assert s_tf == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
