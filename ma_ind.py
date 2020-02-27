# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 22:34:37 2019

@author: sky
"""
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
#from matplotlib.pyplot import plot
#from matplotlib.pyplot import show
#import exchangeConnection.huobi.huobiService913
from exchangeConnection.huobi.huobiService913 import *
import time

##r = pd.read_csv('data1.csv',
#                index_col=0,
#                parse_dates=True,
#                infer_datetime_format=True)

#r = pd.read_csv('mpl_finance-master/examples/data/yahoofinance-SPY-20080101-20180101.csv',
#                index_col=0,
#                parse_dates=True,
#                infer_datetime_format=True)
def moving_average(x, n, type='simple'):
    """
    compute an n period moving average.

    type is 'simple' | 'exponential'

    """
    x = np.asarray(x)
    if type == 'simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))

    weights /= weights.sum()
#    print ("Weights", weights)
    a = np.convolve(x, weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a

def get_kline_csv(symbol, timeframe, size=150):

    #print "字典值 : %s" %  dict_dict.items()
    #print(res_dict['data'])
    #res=res_dict.values()
    
    res_dict=get_kline(symbol, timeframe, size)
#    print(res_dict)
    data=res_dict['data']#降序

    '''
    r['data']
    Out[15]:
    [{'id': 1566662400,
      'open': 9993.0,
      'close': 10143.0,
      'low': 9950.0,
      'high': 10195.89,
      'amount': 6758.235854083652,
      'vol': 68191572.78316337,
      'count': 101529},
     {'id': 1566576000,
      'open': 10397.33,
      'close': 9993.0,
      'low': 9880.0,
      'high': 10440.0,
      'amount': 25055.344445915318,
      'vol': 254843829.21270415,
      'count': 389131},
     {'id': 1566489600,
      'open': 10113.89,
      'close': 10395.65,
      'low': 10020.0,
      'high': 10448.0,
      'amount': 24219.348535304358,
      'vol': 246996004.42081875,
      'count': 272127}]

    '''
    data_list=[]
    #data_list= np.ones((len(data),len(col)))
    for row in data:
    #    print(item.values())
        data_list.append(list(row.values()))
    data_list.reverse()    #列表元素翻转
    return data_list

def get_close(listObj):
    x = np.asarray(listObj)
    t=[]
    close=[]
#    print (type(x))
#    a=np.hsplit(x,8)#按列拆分数组
#    close=a[2]#2：close
#    multiple_list = [[100, 200, 300], [400, 500, 600], [700], [800,900]]
#    multiple_list =a[2]
#    reslut_list =[]


    for sublist in x :
        # time.strftime(要转换成的格式，时间元组)
        tTemp=time.strftime("%Y-%m-%d", time.localtime(sublist[0]))
        t.append(tTemp)
#        t.append(sublist[0])
        close.append(sublist[2])

    return t,close
#''''
#自动运行模块
#''''

import sys
import time
import matplotlib.font_manager as font_manager

def get_ma(symbol="btcusdt",frametime='1day',period=0,shift=0):
        '''
        frametime:图表周期，可选项1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
        period:ma周期长度
        shift : 偏移K线柱数
        '''
#    left, width = 0.1, 1
#    rect2 = [left, 0.3, width, 1]
#    fig = plt.figure(facecolor='white')
#    axescolor = '#f6f6f6'  # the axes background color
#
#    ax2 = fig.add_axes(rect2, facecolor=axescolor)
#    # 设置x轴刻度的数量
#    ax2 = plt.gca()
#    # 设置x轴每个刻度的间隔天数
#    xlocator = mpl.ticker.MultipleLocator(30)
#    ax2.xaxis.set_major_locator(xlocator)
#    # 为了避免x轴日期刻度标签的重叠，设置x轴刻度自动展现，并且45度倾斜
#    fig.autofmt_xdate(rotation = 45)
#    while 1:
        # do your stuff...
#        print('ok')
        r1=get_kline_csv(symbol, frametime, 300)
        #c = r["close"]
        #print(r)
        t,c=get_close(r1)        
        #print (res_dict)
        resList=[]
        list_len=len(r1)
#        print(list_len)
        if list_len>300:
            arrLen=299
        else:
            arrLen=list_len-1
            
        if period == 0:
            ma1 = 5
            ma2 = 10
            ma3= 30
            ma4 = 60            
            ma5 = 120
            if list_len<ma4:
                ma4 = ma3
            if list_len<ma5:
                ma5 = ma4
#            if frametime=='1week':
#                ma5 = ma4
            ma20_list = moving_average(c, ma1, type='simple')
            ma200_list = moving_average(c, ma2, type='simple')
            ma300_list = moving_average(c, ma3, type='simple')
            ma400_list = moving_average(c, ma4, type='simple')
            ma500_list = moving_average(c, ma5, type='simple')
#            print(ma20_list[arrLen-shift])
#            print(ma200_list[arrLen-shift])
    
            resList.append(ma20_list[arrLen-shift])
            resList.append(ma200_list[arrLen-shift])
            resList.append(ma300_list[arrLen-shift])
            resList.append(ma400_list[arrLen-shift])
            resList.append(ma500_list[arrLen-shift])
        else:
            ma20_list = moving_average(c, period, type='simple')
            resList.append(ma20_list[arrLen-shift])            
            # turn off upper axis tick labels, rotate the lower ones, etc

        #plot(t, c, lw=1.0)
        #plot(t, ma20_list, lw=2.0)
        #plot(t, ma200_list, lw=2.0)
        #plot(t, ma300_list, lw=2.0)

#        fig.add_subplot(G[:,:],facecolor='red')
#
#        ax2.plot(t, ma20_list, color='blue', lw=2, label='MA ('+str(ma1)+'):'+str(ma20_list[299]))
#        ax2.plot(t, ma200_list, color='red', lw=2, label='MA ('+str(ma2)+')')
#        ax2.plot(t, ma300_list, color='#336666', lw=2, label='MA ('+str(ma3)+')')
#        ax2.plot(t, ma400_list, color='#336666', lw=2, label='MA ('+str(ma4)+')')
#
##        linema20, = ax2.plot(t, ma20_list, color='blue', lw=2, label='MA (2)')
##        linema200, = ax2.plot(t, ma200_list, color='red', lw=2, label='MA (200)')
##        last = r1.tail(1)
##        s = '%s O:%1.2f H:%1.2f L:%1.2f C:%1.2f, V:%1.1fM Chg:%+1.2f' % (
##            last.index.strftime('%Y.%m.%d')[0],
##            last.Open, last.High,
##            last.Low, last.Close,
##            last.Close - last.Open)
##        t4 = ax2.text(0.3, 0.9, s, transform=ax2.transAxes, fontsize=9)
#
#        props = font_manager.FontProperties(size=10)
#        leg = ax2.legend(loc='center left', shadow=True, fancybox=True, prop=props)
#        leg.get_frame().set_alpha(0.5)
#        plt.show()
#        time.sleep(1)
        return resList

if __name__ == '__main__':
    try:
        res=get_ma("btcusdt",'1day',0,2)
        print(res)
    except KeyboardInterrupt:
        print(sys.stderr, '\nExiting by user request.\n')
        sys.exit(0)