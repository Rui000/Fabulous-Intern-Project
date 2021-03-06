# -*- coding: utf-8 -*-
from __future__ import division
import pandas as pd
import numpy as np
from pandas import to_datetime

###################需增加位置聚类信息、节假日、季节、颜色聚类


origin = pd.read_csv('2018.csv',encoding='GBK',low_memory=False)
#print origin
# min-max
def Normalization(x):
    return [(float(i)-min(x))/float(max(x)-min(x)) for i in x]

origin.sort_values(u"销售日期").head()   #根据日期排序
#降序 origins.sort_values(by=u"销售日期", ascending=False).head()
origin = origin[~origin[u'尺码'].isin(['00'])]
#origin = origin[~origin[u'颜色说明'].str.contains(u'不适用')]#去掉颜色说明这一列中含有不适用这一行的数据
origin = origin[~origin[u'数量'].isin([-1])]   #去掉数量为-1的数据
origin = origin[~origin[u'销售价格'].isin([0])]   #去掉销售价格为0的数据
  #去掉尺码为0的数据

origin = origin.drop([u'店铺编号',u'店铺简称',u'店铺地址',u'颜色编号',u'货号'],axis =1)

origin['discount'] = origin[u'销售价格']/origin[u'吊牌价']   #增加折扣特征
#print origin.shape
#获取2012年1月的数据
#origin[u'销售日期'] = pd.to_datetime(origin[u'销售日期'])
origin[u'销售日期'] = to_datetime(origin[u'销售日期'], format="%Y/%m/%d")

origin = origin.set_index(u'销售日期')
#print(origin['2012-1'])

title_Dict = {}
title_Dict.update(dict.fromkeys([u'浅水泥灰',u'深灰',u'中麻灰',u'深麻灰',u'深灰',u'草绿灰',u'灰牛',u'岩麻灰',u'麻灰',u'原麻色',
                                 u'水泥灰',u'暗夜色',u'浅水泥灰',u'泥灰',u'岩麻灰',u'银蓝灰',u'褐灰色',u'灰牛',u'朦胧灰'],'grey'))
title_Dict.update(dict.fromkeys([u'深葡萄紫',u'紫牛',u'粉紫',u'雨紫'],'purple'))
title_Dict.update(dict.fromkeys([u'暗卡其',u'灰卡其',u'典卡其',u'麻芥末',u'中卡其'],'kaqi'))
title_Dict.update(dict.fromkeys([u'蓝牛',u'夜蓝',u'夏蓝',u'靛蓝',u'冰水蓝',u'间海蓝',u'海麻蓝',u'海洋蓝',u'牛仔靛蓝',
                                 u'蓝灰靛蓝',u'朦胧蓝',u'牛仔蓝',u'暗蓝'],'blue'))
title_Dict.update(dict.fromkeys([u'漂白',u'象牙白',u'白色'],'white'))
title_Dict.update(dict.fromkeys([u'麻军绿',u'罗森绿',u'松针绿',u'军绿',u'嫣麻绿',u'浅军绿',u'卡其绿',u'军装绿',
                                 u'正绿'],'green'))
title_Dict.update(dict.fromkeys([u'栗红',u'殷红',u'栗红',u'水红',u'橘红',u'夏红'],'red'))
title_Dict.update(dict.fromkeys([u'土黄',u'春菊黄',u'卡其黄',u'香槟黄'],'yellow'))
title_Dict.update(dict.fromkeys([u'黑色',u'黑牛',u'卡其黄'],'black'))
title_Dict.update(dict.fromkeys([u'深驼色',u'棕色',u'咖啡色',u'咖啡棕'],'brown'))

origin[u'颜色说明'] = origin[u'颜色说明'].map(title_Dict)
origin = origin[origin[u'货品名称'].isin([u'牛仔长裤'])]
filter = origin[origin[u'店铺省市'].isin([u'上海市上海市市辖区'])]

size = {}
size.update(dict.fromkeys(['XS','S','24','25','26','27','28','29','30'],'small'))
size.update(dict.fromkeys(['M','L','31','32','33'],'medium'))
size.update(dict.fromkeys(['XL','XXL','34','36','38'],'large'))
filter[u'尺码'] = filter[u'尺码'].map(size)

jan = filter['2018-1']
feb = filter['2018-2']
mar = filter['2018-3']
apr = filter['2018-4']
may = filter['2018-5']
jun = filter['2018-6']
jul = filter['2018-7']
aug = filter['2018-8']
sept = filter['2018-9']
oct = filter['2018-10']
nov = filter['2018-11']
dec = filter['2018-12']

#month = ['jan','feb','mar','apr','may','jun','jul','aug','sept','oct','nov','dec']

def Process(month):
#统计1各个尺寸个数
    size_small = 0
    size_medium = 0
    size_large = 0
    for i in month[u'尺码']:
        #print i
        if i=='small':
        #print 'aaaaa'
            size_small = size_small+1
        elif i=='medium':
            size_medium = size_medium +1
        elif i=='large':
            size_large = size_large +1
    #print size_small,size_medium,size_large

#def Sum_disc(month):
#统计折扣个数
    num_disc = 0
    num_nodisc = 0
    for i in month['discount']:
        if i == 1:
            num_disc = num_disc+1 #无折扣数量
        else:
            num_nodisc =num_nodisc+ 1 #有折扣数量
    print num_disc,num_nodisc

#def Sum_color(month):
#统计颜色个数
    color = ['grey','purple','kaqi','blue','white', 'green', 'red', 'yellow', 'black', 'brown']

    num_grey = 0; num_purple = 0; num_kaqi = 0;num_blue = 0;num_white = 0;num_green = 0;num_red = 0;
    num_yellow = 0; num_black = 0;num_brown = 0
    for i in month[u'颜色说明']:
        if i == color[0]:
            num_grey = num_grey+1
        elif i == color[1]:
            num_purple = num_purple+1
        elif i == color[2]:
            num_kaqi = num_kaqi+1
        elif i == color[3]:
            num_blue = num_blue+1
        elif i == color[4]:
            num_white = num_white+1
        elif i == color[5]:
            num_green = num_green+1
        elif i == color[6]:
            num_red = num_red+1
        elif i == color[7]:
            num_yellow = num_yellow+1
        elif i == color[8]:
            num_black = num_black+1
        elif i == color[9]:
            num_brown = num_brown+1
    print num_grey,num_purple,num_kaqi,num_blue,num_white,num_green,num_red,num_yellow,num_black,num_brown

#jan['position'] = 1
#print jan
#def price(month):

    max_price = max(month[u'销售价格'])
    min_price = min(month[u'销售价格'])
    mean_price = np.mean(month[u'销售价格'])
    std_price = np.std(month[u'销售价格'])
    sale_vol = sum(month[u'数量'])
    print max_price,min_price ,std_price,sale_vol

    reconstruct = {
        'size_small':size_small,
        'size_medium' :size_small,
        'size_large':size_large,
        'num_disc': num_disc,
        'num_nodisc':num_nodisc,
        'num_grey':num_grey,
        'num_purple':num_purple,
        'num_kaqi':num_kaqi,
        'num_blue':num_blue,
        'num_white':num_white,
        'num_green':num_green,
        'num_red':num_red,
        'num_yellow':num_red,
        'num_black':num_black,
        'num_brown':num_brown,
        'max_price':max_price,
        'min_price':min_price,
        'mean_price':mean_price,
        'std_price':std_price,
        'sale_vol':sale_vol
        }

    month_reconstruct = pd.DataFrame(reconstruct,index=[0])

    return month_reconstruct

data_jan = Process(month = jan)
data_feb = Process(month = feb)
data_mar = Process(month = mar)
data_apr = Process(month = apr)
data_may = Process(month = may)
data_jun = Process(month = jun)
data_jul = Process(month = jul)
data_aug = Process(month = aug)
data_sept = Process(month = sept)
data_oct = Process(month = oct)
data_nov = Process(month = nov)
data_dec = Process(month = dec)

df_new = pd.concat([data_jan,data_feb,data_mar,data_apr,data_may,
                    data_jun,data_jul,data_aug,data_sept,data_oct,data_nov,data_dec],ignore_index=True)

df_new['month'] = np.arange(12)
print df_new

save = df_new.to_csv('2018-pro.csv')








