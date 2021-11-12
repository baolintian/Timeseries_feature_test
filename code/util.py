import datetime
import matplotlib.pyplot as plt

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
    ts_start=datetime.datetime.strptime(ts_start,'%Y-%m-%d %H:%M:%S') #格式化时间字符串 --> datetime对象时间格式

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
