import pytest
from feature_judge import *
from util import *

# def test_monotone_increase():
#     timeseries_name = "root.CNNP.QF.1#.QF1RCP604MP"
#     config_path = "../config/"+timeseries_name
#     image_path = "../images/"+timeseries_name
#     timeseries_path = "../data/"+timeseries_name+".csv"
#     trend_config, threshold_config = read_config(config_path)
#     timeseries = read_timeseries(timeseries_path)
#
#     # result = trend_judge()
#     # assert result == True
#
# def test_high_two():
#     # result = threadshold_judge()
#     # assert result == True
#     pass

if __name__ == "__main__":
    timeseries_name = "root.CNNP.QF.1#.QF1RCP604MP"
    config_path = "../config/" + timeseries_name
    image_path = "../images/" + timeseries_name
    timeseries_path = "../data/" + timeseries_name + ".csv"
    trend_config, threshold_config = read_config(config_path)
    timeseries = read_timeseries(timeseries_path)
