from feature_judge import *
from util import *


if __name__ == "__main__":
    timeseries_name = "root.CNNP.QF.1#.QF1RCP604MP"
    config_path = "../config/" + timeseries_name
    image_path = "../images/" + timeseries_name
    timeseries_path = "../data/" + timeseries_name + ".csv"
    trend_config, threshold_config = read_config(config_path)
    timeseries = read_timeseries(timeseries_path)
    Dplot = False
    s_tf = trend_features(timeseries, timeseries_name+".numvalue", trend_config, image_path, Dplot)
    print(s_tf)

