import datetime
import matplotlib.pyplot as plt
import json
import pandas as pd

def ts_info(timeseries):
    # 注意传入的是以时间为index的 Parse_data格式的参数
    # 屏幕打印出时间序列的长度，起点，终点，步长
    ts_size =timeseries.size
    ts_start=timeseries.index[0]
    if ts_size == 1:
        ts_end = ts_start
    else:
        ts_end  =timeseries.index[ts_size-1]
    print('timeseries size is :', ts_size)
    print('timeseries start at:',ts_start)
    print('timeseries end at:  ',ts_end)

    #ts_start_tamp = int(ts_start.value / (1000 * 1000 * 1000))  # error： 这样转化,直接忽略微妙，可能会由于解析方式不同，多算8小时，需注意
    # ts_start=time.localtime(ts_start_tamp)   #时间戳 --> 时间元组
    #ts_start=time.strftime('%Y-%m-%d %H:%M:%S',ts_start)  # 时间元组 --> 格式化时间字符串

    ##ts_start=ts_start._short_repr  # Parse_data格式 -->#格式化时间字符串
    ts_start=ts_start._repr_base  # Parse_data格式 -->#格式化时间字符串
    ts_start=datetime.datetime.strptime(ts_start, '%Y-%m-%d %H:%M:%S') #格式化时间字符串 --> datetime对象时间格式

    # ts_end_tamp = int(ts_end.value / (1000 * 1000 * 1000))  # error： 这样转化,直接忽略微妙，可能会由于解析方式不同，多算8小时，需注意
    # ts_end = time.localtime(ts_end_tamp)  # 时间戳 --> 时间元组
    # ts_end = time.strftime('%Y-%m-%d %H:%M:%S', ts_end)  # 时间元组 --> 格式化时间字符串

    ##ts_end = ts_end._short_repr  # Parse_data格式 -->#格式化时间字符串
    ts_end = ts_end._repr_base  # Parse_data格式 -->#格式化时间字符串
    ts_end = datetime.datetime.strptime(ts_end, '%Y-%m-%d %H:%M:%S')  # 格式化时间字符串 --> datetime对象时间格式
    print('timeseries time range is:', ts_end-ts_start)

    if ts_size == 1:
        ts_step = 0
    else:
        ts_start1=timeseries.index[1]
        ##ts_start1 = ts_start1._short_repr  # Parse_data格式 -->#格式化时间字符串
        ts_start1 = ts_start1._repr_base
        ts_start1 = datetime.datetime.strptime(ts_start1, '%Y-%m-%d %H:%M:%S')  # 格式化时间字符串 --> datetime对象时间格式
        ts_step=ts_start1 - ts_start
    print('timeseries time step is:', ts_step)

    # tsinfo = pd.DataFrame({
    #     'size': ts_size, 'start': ts_start, 'end': ts_end
    # })

    tsinfo = {
        'size': ts_size, 'start': ts_start, 'end': ts_end,'range':ts_end-ts_start,'step':ts_step
    }
    return tsinfo

def timeseries_plot(y, color, y_label,pathsave):
    # y is Series with index of datetime
    # days = dates.DayLocator()
    # dfmt_minor = dates.DateFormatter('%m-%d')
    # weekday = dates.WeekdayLocator(byweekday=(), interval=1)

    fig, ax = plt.subplots()
    # ax.xaxis.set_minor_locator(days)
    # ax.xaxis.set_minor_formatter(dfmt_minor)
    #
    # ax.xaxis.set_major_locator(weekday)
    # ax.xaxis.set_major_formatter(dates.DateFormatter('\n\n%a'))
    #
    # ax.set_ylabel(y_label)
    color_type=color+'o:'
    ax.plot(y.index, y, color_type)
    fig.set_size_inches(12, 8)
    plt.tight_layout()
    #plt.savefig(pathsave+y_label + '.png', dpi=300)
    plt.savefig(pathsave + y_label + '.png')
    # plt.show()
    plt.close()

def judge_timeseries_validation():
    pass

def judge_trend_validation():
    pass

def judge_threshold_validation():
    pass

def read_config(config_path):
    # config_path: 测试该时间序列的文件夹路径
    # 返回：时间序列的配置，趋势征兆配置，阈值征兆配置

    timeseries_config_file = config_path+"/timeseries.json"
    trend_config_file = config_path+"/trend.json"
    threshold_file = config_path+"/threshold.json"

    # 读取时间序列配置相关的参数
    with open(timeseries_config_file, 'r', encoding='utf8')as fp:
        timeseries_config_raw = json.load(fp)

    with open(trend_config_file, 'r', encoding='utf8')as fp:
        trend_config_raw = json.load(fp)

    with open(threshold_file, 'r', encoding='utf8')as fp:
        threshold_config_raw = json.load(fp)

    rolmean_window4vibrate = timeseries_config_raw["rolmean_window4vibrate"]
    rolmean_window4monotonicity = timeseries_config_raw["rolmean_window4monotonicity"]
    monotonicity_peakvalleys = timeseries_config_raw["monotonicity_peakvalleys"]
    ADF_pvalue = timeseries_config_raw["ADF_pvalue"]

    S04_std_lower = trend_config_raw['S04']['std_lower']  # type：float; 判断是否稳定不变时用到得方差上限

    S12_vibrate_range = trend_config_raw['S12']['vibrate_range']  # type：float; 判定为震荡时用到得四分位距下限（四分位距相对于均值的百分比）
    S12_vibrate_rate = trend_config_raw['S12']['vibrate_rate']  # type：float; 振荡条件时，波峰波谷数目占总数据点数的比例（滤去小波后）

    S11_drop_range = trend_config_raw['S11']['drop_range']  # type：float; 波动下降时，下降幅度（起点减终点绝对值）占起点绝对值的比例应大于这个数
    S11_vibrate_rate = trend_config_raw['S11']['vibrate_rate']  # type：float; 波动下降时，波峰波谷数目占总数据点数的比例（滤去小波后）

    S10_rise_range = trend_config_raw['S10']['rise_range']  # type：float; 波动上升时，下降幅度（起点减终点绝对值）占起点绝对值的比例应大于这个数
    S10_vibrate_rate = trend_config_raw['S10']['vibrate_rate']  # type：float; 波动上升时，波峰波谷数目占总数据点数的比例（滤去小波后）

    S07_drop_range = trend_config_raw['S07']['drop_range']  # type：float; 单调快速下降时，下降幅度（起点减终点绝对值）占起点绝对值的比例应大于这个数
    S05_drop_range = trend_config_raw['S05']['drop_range']  # type：float; 单调缓慢下降时，下降幅度（起点减终点绝对值）占起点绝对值的比例应小于这个数

    S01_rise_range = trend_config_raw['S01']['rise_range']  # type：float; 单调快速上升时，上升幅度（起点减终点绝对值）占起点绝对值的比例应大于这个数
    S03_rise_range = trend_config_raw['S03']['rise_range']  # type：float; 单调缓慢上升时，上升幅度（起点减终点绝对值）占起点绝对值的比例应小于这个数

    S08_location_range = trend_config_raw['S08']['range']  # type:floatlist; 单凸峰值所处的相对位置
    S09_location_range = trend_config_raw['S09']['range']  # type:floatlist; 单凹峰值所处的相对位置

    trend_config = {
        'rolmean_window4vibrate': rolmean_window4vibrate,
        'rolmean_window4monotonicity': rolmean_window4monotonicity,
        'monotonicity_peakvalleys': monotonicity_peakvalleys,
        'ADF_pvalue': ADF_pvalue,
        'S04_std_lower': S04_std_lower,
        'S12_vibrate_range': S12_vibrate_range,
        'S12_vibrate_rate': S12_vibrate_rate,
        'S11_drop_range': S11_drop_range,
        'S11_vibrate_rate': S11_vibrate_rate,
        'S10_rise_range': S10_rise_range,
        'S10_vibrate_rate': S10_vibrate_rate,
        'S07_drop_range': S07_drop_range,
        'S05_drop_range': S05_drop_range,
        'S01_rise_range': S01_rise_range,
        'S03_rise_range': S03_rise_range,
        'S08_location_range': S08_location_range,
        'S09_location_range': S09_location_range
    }

    T03_range = [threshold_config_raw['T03']['lower'], threshold_config_raw['T03']['upper']]  # 高高高
    T02_range = [threshold_config_raw['T02']['lower'], threshold_config_raw['T02']['upper']]  # 高高
    T01_range = [threshold_config_raw['T01']['lower'], threshold_config_raw['T01']['upper']]  # 高
    T04_range = [threshold_config_raw['T04']['lower'], threshold_config_raw['T04']['upper']]  # 低
    T05_range = [threshold_config_raw['T05']['lower'], threshold_config_raw['T05']['upper']]  # 低低
    T06_range = [threshold_config_raw['T06']['lower'], threshold_config_raw['T06']['upper']]  # 低低低

    # 若不落在以上区域中，均为正常
    T_used = threshold_config_raw['T_used']

    threshold_config = {
        'T03_range': T03_range,
        'T02_range': T02_range,
        'T01_range': T01_range,
        'T04_range': T04_range,
        'T05_range': T05_range,
        'T06_range': T06_range,
        'T_used': T_used
    }
    return trend_config, threshold_config, timeseries_config_raw["resample_fre"]

def read_timeseries(timeseries_path, resample_frequency):
    timestamp = []
    timeseries_value = []

    with open(timeseries_path, "r") as f:
        for line_number, line in enumerate(f.readlines()):
            if line_number == 0:
                timeseries_name = line.split(',')[1]
                timeseries_name = timeseries_name.replace('\n', '')
            else:
                values = line.split(',')
                timestamp.append(values[0])
                timeseries_value.append(eval(values[1]))

    df_analyze = pd.DataFrame(data=timeseries_value, index=timestamp, columns=[timeseries_name])

    df_analyze = pd.Series(df_analyze.iloc[:, 0].values, index=pd.DatetimeIndex(df_analyze.index))
    df_analyze = df_analyze.resample(resample_frequency).mean().ffill()
    return df_analyze
