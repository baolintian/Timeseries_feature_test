import pytest
from feature_judge import *

def test_monotone_increase():
    timeseries_name = "CNNP.QF.1#.QF1RCP604MP"
    config_path = "./config/"+timeseries_name
    image_path = "./images/"+timeseries_name
    timeseries_path = "./data/"+timeseries_name+".csv"
    

    result = trend_judge()
    assert result == True

def test_high_two():
    result = threadshold_judge()
    assert result == True

