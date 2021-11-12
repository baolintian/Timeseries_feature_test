# python 3.9 (>=3.7)
# encoding=UTF-8
# author: xyb
#---------------------------------------------------------------
# 功能：进行趋势离散分析
#

import sys
import os
import json
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller as ADF
from util import *


def peakvalley(ts_analyze): # 数据的波峰波谷
    diff1 = ts_analyze.diff(1)
    num = np.size(diff1)
    #print(np.size(diff1))
    peakvalley = 0
    index_peakvalley=[]
    for i in range(num - 1):
        mult = diff1[i] * diff1[i + 1]
        if mult <= 0:
            peakvalley = peakvalley + 1
            index_peakvalley.append(i)
    print('--波峰波谷个数：%s' % (peakvalley))
    return index_peakvalley

def trend_features(df_analyze,valuename,trend_features_inputdata,DPlot_dir,Dplot):
    # 判断准则 ： trend_features_inputdata
    # 时序序列 ： df_analyze
    # 时序序列在iotdb中的路径名：valuename
    # 调试输出路径：DPlot_dir
    # 调试输出判断：Dplot
    print('==>>>数据测点：%s' % (valuename))

    # 波动性判断滤波准则
    rolmean_window4vibrate = trend_features_inputdata['rolmean_window4vibrate']  # type：int; 降噪平均的滑窗窗口长度,不能超过数据个数，用于判断震动，建议给的小一些
    # 单调性判断滤波准则
    rolmean_window4monotonicity = trend_features_inputdata[
        'rolmean_window4monotonicity']  # type：int; 降噪平均的滑窗窗口长度,不能超过数据个数，用于判断单调性，可适当稍大
    monotonicity_peakvalleys=trend_features_inputdata['monotonicity_peakvalleys']# type：int; 单调性加窗滤波后，单调性序列允许的最大波峰波谷数（该值取1，表示严格单调）

    ADF_pvalue = trend_features_inputdata['ADF_pvalue']  # type：float;ADF 检验时得p-value
    ADF_pvalue_tf = 'unknown'

    S04_std_lower = trend_features_inputdata['S04_std_lower']  # type：float; 判断是否稳定不变时用到得方差上限
    S12_vibrate_range = trend_features_inputdata['S12_vibrate_range']  # type：float; 判定为震荡时用到得四分位距下限（四分位距相对于均值的百分比）
    S12_vibrate_rate = trend_features_inputdata['S12_vibrate_rate']  # type：float; 振荡条件时，波峰波谷数目占总数据点数的比例（滤去小波后）
    S11_drop_range = trend_features_inputdata['S11_drop_range']  # type：float; 波动下降时，下降幅度（起点减终点绝对值）占起点绝对值的比例应大于这个数
    S11_vibrate_rate = trend_features_inputdata['S11_vibrate_rate']  # type：float; 波动下降时，波峰波谷数目占总数据点数的比例（滤去小波后）
    S10_rise_range = trend_features_inputdata['S10_rise_range']  # type：float; 波动上升时，下降幅度（起点减终点绝对值）占起点绝对值的比例应大于这个数
    S10_vibrate_rate = trend_features_inputdata['S10_vibrate_rate']  # type：float; 波动上升时，波峰波谷数目占总数据点数的比例（滤去小波后）
    S07_drop_range = trend_features_inputdata['S07_drop_range']  # type：float; 单调快速下降时，下降幅度（起点减终点绝对值）占起点绝对值的比例应大于这个数
    S05_drop_range = trend_features_inputdata['S05_drop_range']  # type：float; 单调缓慢下降时，下降幅度（起点减终点绝对值）占起点绝对值的比例应小于这个数
    S01_rise_range = trend_features_inputdata['S01_rise_range']  # type：float; 单调快速上升时，上升幅度（起点减终点绝对值）占起点绝对值的比例应大于这个数
    S03_rise_range = trend_features_inputdata['S03_rise_range']  # type：float; 单调缓慢上升时，上升幅度（起点减终点绝对值）占起点绝对值的比例应小于这个数
    S08_location_range = trend_features_inputdata['S08_location_range']  # type:floatlist; 单凸峰值所处的相对位置
    S09_location_range = trend_features_inputdata['S09_location_range']  # type:floatlist; 单凹峰值所处的相对位置

    ts_numeric = pd.to_numeric(df_analyze[valuename])
    print('==>>>用于趋势判断的时序数据：')
    # tsinfo = ts_info(ts_numeric)
    if Dplot == 'yes': timeseries_plot(ts_numeric, 'g', valuename+'_oir', pathsave=DPlot_dir)

    s_tf = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ADF_pvalue_tf = 'unknown'

    # 根据波动性判断滤波准则滤波
    # 预处理：滑窗均值降噪,去掉微小波动，避免影响波动频率的估计
    if np.size(df_analyze) < int(rolmean_window4vibrate):
        print('Warning:‘波动性’滑窗降噪的窗口长度（长度指数据点个数）太大，大于读入的数据点个数！\n直接跳过滑窗降噪')
        rolmean_window4vibrate=1
    ts_numeric_rolmean = ts_numeric.rolling(window=int(rolmean_window4vibrate)).mean()
    ts_numeric_rolmean = ts_numeric_rolmean.dropna(inplace=False)
    ts_analyze = ts_numeric_rolmean
    if Dplot == 'yes': timeseries_plot(ts_analyze, 'g',valuename +'_rollmean_vibrate', pathsave=DPlot_dir)

    print('序列的平稳性检验(ADF检验结)果为：')
    test_result = ADF(ts_analyze)
    p_value = test_result[1]
    print('p-value:', p_value)
    if p_value >= ADF_pvalue:
        print('--原始序列是非平稳序列')
        ADF_pvalue_tf = 'unstationary'
    else:
        print('--原始序列是平稳序列')
        ADF_pvalue_tf = 'stationary'

    # 判断分支： 平稳不变序列
    if ADF_pvalue_tf == 'stationary':
        print('标准差判断：')
        std_value = np.std(ts_analyze, ddof=1)
        if std_value >= S04_std_lower:
            # print('--标准差：s,大于下限：{:.8%}'.format(S04_S04_std_lower))
            print('--标准差：%f,大于下限：%f' % (std_value, S04_std_lower))
        if std_value < S04_std_lower:
            print('--标准差：%f,小于下限：%f' % (std_value, S04_std_lower))
            print('--原始序列是平稳不变序列')
            s_tf[4-1] = 1  # 失效特征趋势：平稳不变 ,s_04=1

    # 判断分支： 平稳震荡序列(并非平稳不变序列的补集，但不能有交集)
    if ADF_pvalue_tf == 'stationary' and s_tf[4-1] == 0:
        print('判断是否震荡：')
        mean_value = np.mean(ts_analyze)
        lower_q = np.quantile(ts_analyze, 0.25, interpolation='lower')  # 下四分位数
        higher_q = np.quantile(ts_analyze, 0.75, interpolation='higher')  # 上四分位数
        int_r = higher_q - lower_q  # 四分位距
        if int_r / abs(mean_value) >= S12_vibrate_range:
            print('根据波动性判断滤波准则滤波后：')
            num_peakvalley = np.size(peakvalley(ts_analyze))  # 计算波峰波谷数
            vibrate_rate = num_peakvalley / np.size(ts_analyze)  # 计算波动率，(过滤掉小波后)
            if vibrate_rate >= S12_vibrate_rate:
                print('--原始序列是平稳震荡序列')
                s_tf[12-1] = 1  # 失效特征趋势：平稳震荡 ,s_12=1

    # 判断分支： 波动性 (波峰波谷数，起止点变化范围)
    if ADF_pvalue_tf == 'unstationary':
        print('根据波动性判断滤波准则滤波后：')
        index_peakvalley = peakvalley(ts_analyze)
        num_peakvalley = np.size(index_peakvalley)  # 计算波峰波谷数
        vibrate_rate = num_peakvalley / np.size(ts_analyze)  # 计算波动率，(过滤掉小波后)
        if vibrate_rate >= S11_vibrate_rate:
            drop_range = ts_analyze[0] - ts_analyze[np.size(ts_analyze) - 1]
            if drop_range > 0 and abs(drop_range / ts_analyze[0]) >= S11_drop_range:
                print('--原始序列是波动下降序列')
                s_tf[11-1] = 1  # 失效特征趋势：波动下降 ,s_11=1

        if vibrate_rate >= S10_vibrate_rate:
            rise_range = ts_analyze[0] - ts_analyze[np.size(ts_analyze) - 1]
            if rise_range < 0 and abs(rise_range / ts_analyze[0]) >= S10_rise_range:
                print('--原始序列是波动上升序列')
                s_tf[10-1] = 1  # 失效特征趋势：波动上升 ,s_10=1

    # 判断分支： 判断单调性
    if ADF_pvalue_tf == 'unstationary' and s_tf[10-1] == 0 and s_tf[11-1] == 0:
        # 根据波动性判断滤波准则滤波
        if rolmean_window4monotonicity >= np.size(ts_numeric):
            print('Error: ‘单调性’滑窗降噪的窗口长度（长度指数据点个数）太大，大于读入的数据点个数！')
            #print('Warning:‘单调性’滑窗降噪的窗口长度（长度指数据点个数）太大，大于读入的数据点个数！\n直接跳过滑窗降噪')
            #rolmean_window4monotonicity = 1
            os._exit()
        ts_numeric_rolmean = ts_numeric.rolling(window=int(rolmean_window4monotonicity)).mean()
        ts_numeric_rolmean = ts_numeric_rolmean.dropna(inplace=False)
        ts_analyze = ts_numeric_rolmean
        if Dplot == 'yes': timeseries_plot(ts_analyze, 'g',valuename+'_rollmean_monotonicity', pathsave=DPlot_dir)
        print('根据单调性判断滤波准则滤波后：')

        index_peakvalley = peakvalley(ts_analyze)  # 计算波峰波位置索引
        if np.size(index_peakvalley) <= monotonicity_peakvalleys:  # 趋势(近似)是单调的
            change_range = ts_analyze[0] - ts_analyze[np.size(ts_analyze) - 1]
            if change_range > 0:  # 单调下降
                print("计算出来的斜率")
                print(abs(change_range / ts_analyze[0]))
                print(S05_drop_range)
                # print(change_range)
                # print(ts_analyze[0])
                # print(ts_analyze[np.size(ts_analyze) - 1])
                if abs(change_range / ts_analyze[0]) >= S07_drop_range:
                    print('--原始序列是单调急剧下降序列')
                    s_tf[7-1] = 1  # 失效特征趋势：单调急剧下降 ,s_07=1
                elif abs(change_range / ts_analyze[0]) < S05_drop_range:
                    print('--原始序列是单调缓慢下降序列')
                    s_tf[5-1] = 1  # 失效特征趋势：单调缓慢下降 ,s_05=1
                else:
                    print('--原始序列是单调下降序列')
                    s_tf[6-1] = 1  # 失效特征趋势：单调下降 ,s_06=1
            if change_range < 0:  # 单调上升
                if abs(change_range / ts_analyze[0]) >= S01_rise_range:
                    print('--原始序列是单调急剧上升序列')
                    s_tf[1-1] = 1  # 失效特征趋势：单调急剧上升 ,s_01=1
                elif abs(change_range / ts_analyze[0]) < S03_rise_range:
                    print('--原始序列是单调缓慢上升序列')
                    s_tf[3-1] = 1  # 失效特征趋势：单调缓慢上升 ,s_03=1
                else:
                    print('--原始序列是单调上升序列')
                    s_tf[2-1] = 1  # 失效特征趋势：单调上升 ,s_02=1

        if np.size(index_peakvalley) <= monotonicity_peakvalleys and max(s_tf)==0 :  # 趋势(近似)是单凹或单凸
        # 第一版中，通过唯一波峰波谷的位置来判断
            # index = index_peakvalley[0]
            # location = index / np.size(ts_analyze)
        # 第二版中，改为通过最大值，最小值来判断。弱化了对波峰波谷数的要求
            list = ts_analyze.values.tolist()
            max_list = max(list)
            min_list = min(list)
            min_index = list.index(min_list)
            max_index = list.index(max_list)
            max_location = max_index / np.size(ts_analyze)
            min_location = min_index / np.size(ts_analyze)
            if ts_analyze[max_index] <= ts_analyze[0] or ts_analyze[max_index] <= ts_analyze[np.size(ts_analyze) - 1]:
                if min_location <= S09_location_range[1] and min_location >= S09_location_range[0]:  # 单凹
                    print('--原始序列是单凹（下降后上升）')
                    s_tf[9-1] = 1  # 失效特征趋势：单凹（下降后上升） ,s_09=1

            if ts_analyze[min_index] >= ts_analyze[0] or ts_analyze[min_index] >= ts_analyze[np.size(ts_analyze) - 1]:  # 单凸
                if max_location <= S08_location_range[1] and max_location >= S08_location_range[0]:  # 单凸
                    print('--原始序列是单凸（下降后上升）')
                    s_tf[8-1] = 1  # 失效特征趋势：单凸（上升后下降） ,s_08=1

    print('趋势征兆向量:', s_tf)
    return s_tf


def threshold_features(df_analyze,valuename,threshold_features_inputdata,DPlot_dir,Dplot):
    # 判断准则 ： threshold_features_inputdata
    # 时序序列 ： df_analyze
    # 时序序列在iotdb中的路径名：valuename
    # 调试输出路径：DPlot_dir
    # 调试输出判断：Dplot

    print('==>>>数据测点：%s'%(valuename))
    T03_range = threshold_features_inputdata['T03_range']   #高高高
    T02_range = threshold_features_inputdata['T02_range']   # 高高
    T01_range = threshold_features_inputdata['T01_range']   # 高
    T04_range = threshold_features_inputdata['T04_range']   #低
    T05_range = threshold_features_inputdata['T05_range']   #低低
    T06_range = threshold_features_inputdata['T06_range']   #低低低

    # 若不落在以上区域中，均为正常
    T_used    = threshold_features_inputdata['T_used']

    t_tf = [0, 0, 0, 0, 0, 0]

    ts_numeric = pd.to_numeric(df_analyze[valuename])
    print('==>>>用于阈值判断的时序数据：')
    tsinfo = ts_info(ts_numeric)
    # 阈值判断区间是否合理
    ranking=[]
    if not T_used[3-1] == 0:
        ranking.append(T03_range[1])
        ranking.append(T03_range[0])
    if not T_used[2-1] == 0:
        ranking.append(T02_range[1])
        ranking.append(T02_range[0])
    if not T_used[1-1] == 0:
        ranking.append(T01_range[1])
        ranking.append(T01_range[0])
    if not T_used[4-1] == 0:
        ranking.append(T04_range[1])
        ranking.append(T04_range[0])
    if not T_used[5-1] == 0:
        ranking.append(T05_range[1])
        ranking.append(T05_range[0])
    if not T_used[6-1] == 0:
        ranking.append(T06_range[1])
        ranking.append(T06_range[0])

    for i in range(np.size(ranking)-1):
        if ranking[i] < ranking[i+1]:
            print('Error：检查各失效阈值的判定区间是否满足规律要求！（T3>T2>T1>T4>T5>T6）')
            os._exit()
    mean_value = np.mean(df_analyze)
    mean_value =mean_value.values[0]
    if not T_used[3-1] == 0:
        if mean_value >= T03_range[0] and mean_value <= T03_range[1]:
            t_tf[3-1]=1
    if not T_used[2-1] == 0:
        if mean_value >= T02_range[0] and mean_value <= T02_range[1]:
            t_tf[2-1]=1
    if not T_used[1-1] == 0:
        if mean_value >= T01_range[0] and mean_value <= T01_range[1]:
            t_tf[1-1]=1
    if not T_used[4-1] == 0:
        if mean_value >= T04_range[0] and mean_value <= T04_range[1]:
            t_tf[4-1]=1
    if not T_used[5-1] == 0:
        if mean_value >= T05_range[0] and mean_value <= T05_range[1]:
            t_tf[5-1]=1
    if not T_used[6-1] == 0:
        if mean_value >= T06_range[0] and mean_value <= T06_range[1]:
            t_tf[6-1]=1
    print('阈值征兆向量:', t_tf)
    return t_tf


if __name__ == '__main__':
    jsonfile ={
        'rolmean_window4vibrate': 20,   # type：int; 降噪平均的滑窗窗口长度,不能超过数据个数，用于判断震动，建议给的小一些
        'rolmean_window4monotonicity':50,  # type：int; 降噪平均的滑窗窗口长度,不能超过数据个数，用于判断单调性，可适当稍大
        'monotonicity_peakvalleys':20,  # type：int; 单调性加窗滤波后，单调性序列允许的最大波峰波谷数（该值取1，表示严格单调）
        'ADF_pvalue':0.05,          # type：float;ADF 检验时的p-value

        'S04': {'std_lower':0.10},    # type：float; 判断是否稳定不变时用到得方差上限
        'S12': {'vibrate_range': 0.05,'vibrate_rate': 0.05},  # type：float; 判定为震荡时用到得四分位距下限（四分位距相对于均值的百分比）
                                                              # type：float; 振荡条件时，波峰波谷数目占总数据点数的比例（滤去小波后）

        'S11': {'drop_range': 0.01, 'vibrate_rate': 0.09},   # type：float; 波动下降时，下降幅度（起点减终点绝对值）占起点绝对值的比例应大于这个数
                                                             # type：float; 波动下降时，波峰波谷数目占总数据点数的比例（滤去小波后）
        'S10': {'rise_range': 0.01, 'vibrate_rate': 0.05},   # type：float; 波动上升时，下降幅度（起点减终点绝对值）占起点绝对值的比例应大于这个数
                                                             # type：float; 波动上升时，波峰波谷数目占总数据点数的比例（滤去小波后）
        'S01': {'rise_range': 0.05},   # type：float; 单调快速上升时，上升幅度（起点减终点绝对值）占起点绝对值的比例应大于这个数
        'S02': {},
        'S03': {'rise_range': 0.01},   # type：float; 单调缓慢上升时，上升幅度（起点减终点绝对值）占起点绝对值的比例应小于这个数

        'S05': {'drop_range': 0.04},   # type：float; 单调快速下降时，下降幅度（起点减终点绝对值）占起点绝对值的比例应大于这个
        'S06': {},
        'S07': {'drop_range': 0.05},   # type：float; 单调缓慢下降时，下降幅度（起点减终点绝对值）占起点绝对值的比例应小于这个

        'S08': {'range': [0.01, 0.99]},  # type:floatlist; 单凸峰值所处的相对位置
        'S09': {'range': [0.01, 0.99]},  # type:floatlist; 单凹峰值所处的相对位置
    }

    with open("trend.json", "w") as f:
        json.dump(jsonfile, f)
        print("加载入文件完成...")

    # jsonfile = { # for FQ1RCP604MP
    #     'T03': {'lower': 10000001, 'upper': 10000002, },  # type：float; 高高高，上限建议给默认的极大值
    #     'T02': {'lower': 10000000, 'upper': 10000001, },       # type：float; 高高
    #     'T01': {'lower': 100, 'upper': 10000000, },       # type：float; 高
    #     'T04': {'lower': -1000001, 'upper':-1000000, },       # type：float; 低
    #     'T05': {'lower': -1000003, 'upper': -1000002, },       # type：float; 低低
    #     'T06': {'lower': -1000005, 'upper': -1000004, }, # type：float; 低低低，下限建议给默认的极小值
    #     'T_used':[1,1,1,1,1,1]   # type：int; 使用到的征兆通道给非零值
    # }

    jsonfile = {  # for 1APA136MT_1
        'T03': {'lower': 1000003, 'upper': 1000004, },  # type：float; 高高高，上限建议给默认的极大值
        'T02': {'lower': 1000001, 'upper': 1000002, },  # type：float; 高高
        'T01': {'lower': 100, 'upper': 1000000, },  # type：float; 高
        'T04': {'lower': 4.7, 'upper': 5, },  # type：float; 低
        'T05': {'lower': 4.5, 'upper': 4.7, },  # type：float; 低低
        'T06': {'lower': -1000005, 'upper': 4.5, },  # type：float; 低低低，下限建议给默认的极小值
        'T_used': [1, 0, 0, 0, 0, 0]  # type：int; 使用到的征兆通道给非零值
    }

    with open("threshold.json", "w") as f:
        json.dump(jsonfile, f)
        print("加载入文件完成...")