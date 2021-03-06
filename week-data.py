# -*- coding: utf-8 -*-
from pandas import read_csv
from pandas import to_datetime
import pandas as pd

import sys

reload(sys)
sys.setdefaultencoding('utf8')

def Week(database):
    origin = read_csv(database, encoding='gbk', low_memory=False)
    origin.sort_values(u"销售日期").head()
    origin[u'销售日期'] = pd.to_datetime(origin[u'销售日期'])
    origin = origin.set_index(u'销售日期')
    # 根据日期排序
    origin = origin[~origin[u'尺码'].isin(['00'])]
    origin = origin[~origin[u'颜色说明'].str.contains(u'不适用')]  # 去掉颜色说明这一列中含有不适用这一行的数据
    origin = origin[~origin[u'数量'].isin([-1])]  # 去掉数量为-1的数据
    origin = origin[~origin[u'销售价格'].isin([0])]  # 去掉销售价格为0的数据
    # 去掉尺码为0的数据

    origin = origin.drop([u'店铺省市', u'店铺简称', u'店铺地址', u'颜色编号', u'货号'], axis=1)

    origin['discount'] = origin[u'销售价格'] / origin[u'吊牌价']  # 增加折扣特征
    # s_M = df_dt.dt.month
    # 对颜色分类
    title_Dict = {}
    title_Dict.update(dict.fromkeys([u'墨色', u'浅水泥灰', u'深灰', u'中麻灰', u'深麻灰', u'深灰', u'草绿灰', u'灰牛'
                                        , u'岩麻灰', u'麻灰', u'原麻色',
                                     u'水泥灰', u'暗夜色', u'浅水泥灰', u'泥灰', u'岩麻灰', u'银蓝灰',
                                     u'褐灰色', u'灰牛', u'朦胧灰'], 'grey'))
    title_Dict.update(dict.fromkeys([u'蓝牛', u'夜蓝', u'夏蓝', u'靛蓝', u'冰水蓝', u'间海蓝', u'海麻蓝',
                                     u'海洋蓝', u'牛仔靛蓝',
                                     u'蓝灰靛蓝', u'朦胧蓝', u'牛仔蓝', u'暗蓝'], 'blue'))
    title_Dict.update(dict.fromkeys([u'黑色', u'黑牛'], 'black'))

    origin[u'颜色说明'] = origin[u'颜色说明'].map(title_Dict)

    # 读取上海市牛仔裤的数据
    origin = origin[origin[u'货品名称'].isin([u'牛仔裤'])]
    # filter = origin[origin[u'店铺省市'].isin([u'上海市上海市市辖区'])]
    origin = origin[origin[u'店铺编号'].isin(['SH01SH07'])]
    # 尺码分类
    size = {}
    size.update(dict.fromkeys(['XS', 'S', '24', '25', '26', '27', '28', '29', '30'], 'small'))
    size.update(dict.fromkeys(['M', 'L', '31', '32', '33'], 'medium'))
    size.update(dict.fromkeys(['XL', 'XXL', '34', '36', '38'], 'large'))
    origin[u'尺码'] = origin[u'尺码'].map(size)

    # print filter
    #### 牛仔裤的颜色只统计黑蓝灰白

    origin['num_grey'] = origin[u'颜色说明']
    origin['num_black'] = origin[u'颜色说明']
    origin['num_blue'] = origin[u'颜色说明']
    origin['num_black'] = origin[u'颜色说明']
    origin['num_small'] = origin[u'尺码']
    origin['num_medium'] = origin[u'尺码']
    origin['num_large'] = origin[u'尺码']
    # print origin.head()

    origin['discount'][origin['discount'] < 1] = 0
    origin.ix[origin['num_large'] == 'large', 'num_large'] = 1
    origin.ix[origin['num_large'] != 'large', 'num_large'] = 0

    origin.ix[origin['num_small'] == 'small', 'num_small'] = 1
    origin.ix[origin['num_small'] != 'small', 'num_small'] = 0

    origin.ix[origin['num_medium'] != 'medium', 'num_medium'] = 0
    origin.ix[origin['num_medium'] == 'medium', 'num_medium'] = 1

    origin.ix[origin['num_blue'] != 'blue', 'num_blue'] = 0
    origin.ix[origin['num_blue'] == 'blue', 'num_blue'] = 1

    origin.ix[origin['num_grey'] == 'grey', 'num_grey'] = 0
    origin.ix[origin['num_grey'] != 'grey', 'num_grey'] = 1

    origin.ix[origin['num_black'] != 'black', 'num_black'] = 0
    origin.ix[origin['num_black'] == 'black', 'num_black'] = 1

    # print origin.head()

    output = origin.resample('w').sum()
    # print output

    output['mean_price'] = origin[u'销售价格'].resample('w').std()
    output['max_price'] = origin[u'销售价格'].resample('w').max()
    output['min_price'] = origin[u'销售价格'].resample('w').min()
    output['rate_dis'] = (output[u'数量'] - output['discount']) / output[u'数量']

    output = output.drop([u'吊牌价', u'销售价格'], axis=1)

    output.to_csv('2012-week.csv')

Week('2012.csv')

#分别得到08-12年的周销量数据后合并到同一个表
'''
week08 = pd.read_csv('2008-week.csv')
week09 = pd.read_csv('2009-week.csv')
week10 = pd.read_csv('2010-week.csv')
week11 = pd.read_csv('2011-week.csv')
week12 = pd.read_csv('2012-week.csv')

df_new = pd.concat([week08,week09,week10,week11,week12],ignore_index=True)

df_new.to_csv('08-12week.csv')
'''
