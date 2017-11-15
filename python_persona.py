# coding: utf-8

import random
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib as mpl
import seaborn as sns
from ggplot import *


os.chdir(u'E:\长帐龄项目\长帐龄数据\data\plot')



guangdabase = pd.read_csv('guangdabase.csv' , header = None)
guangdadzd = pd.read_csv('guangdadzd.csv' , header = None)
guangfabase = pd.read_csv('guangfabase.csv' , header = None)
guangfadzd = pd.read_csv('guangfadzd.csv' , header = None)
jianhangbase = pd.read_csv('jianhangbase.csv' , header = None)
jianhangdzd = pd.read_csv('jianhangdzd.csv' , header = None)
pinganbase = pd.read_csv('pinganbase.csv' , header = None)
pingandzd = pd.read_csv('pingandzd.csv' , header = None)
xingyebase = pd.read_csv('xingyebase.csv' , header = None)
xingyedzd = pd.read_csv('xingyedzd.csv' , header = None)
zhaoshangbase = pd.read_csv('zhaoshangbase.csv' , header = None)
zhaoshangdzd = pd.read_csv('zhaoshangdzd.csv' , header = None)

province = pd.read_excel('province.xlsx')




xybase = pd.concat([guangdabase,guangfabase,jianhangbase,pinganbase,xingyebase,zhaoshangbase],ignore_index=True)
xybase.shape


xydzd = pd.concat([guangdadzd,guangfadzd,jianhangdzd,pingandzd,xingyedzd,zhaoshangdzd],ignore_index=True)
xydzd.shape


def xybasenames(data1):
    data1.colnames=['id', 'UpdateFlag', 'branch', 'ajbh', 'kehu', 'ajlx', 'shfzh', 'shfzh18', 'shebaoID', 'xm', 'pinyin', 'sex',                     'zhiwu', 'zjqkje', 'zjshje', 'zjzxqke', 'zjzxqkerq', 'zjyhlx', 'jdsj', 'dqsj', 'zu', 'ywy', 'states', 'period',                    'yjbl', 'fenpeisj', 'urgent', 'lasttime', 'closetime', 'czy', 'addtime', 'pici', 'inpici', 'shengfen', 'chengshi',                    'remark1', 'remark2', 'remark3', 'lastJzSj', 'kongguan', 'PromisedDate', 'PromisedJe', 'nextStep', 'hint',                     'dingyueTime', 'fabuTime', 'gaNum', 'Ajsx', 'ajInfo', 'kehuAjBh', 'ajStop', 'ajLock', 'yxAj', 'isShare', 'zxxddm',                    'picipizhu']
    return data1



def xydzdnames(data2):
    data2.colnames=['shfzh18','kehu','ajlx','inpici','account','cardno','hkrq','dzrq','hkze','hkmx','rate','huobi',                    'zhrmb','qkbj','yhlx','zxqkje','hkbz','ywy','czy','Lasttime','flag','IsAggregatedCard','ajbh',                    'fabuTime','kehuliushuiNum']
    return data2



xybase =xybasenames(xybase[:])
xybase.columns=xybase.colnames




xydzd =xydzdnames(xydzd[:])
xydzd.columns=xydzd.colnames



xydzd = xydzd[xydzd.hkbz==1]
xydzd = xydzd[xydzd.hkmx>0]


xydzddata =xydzd[['ajbh','kehu','hkrq','hkmx','shfzh18']]


xydzddata["shfzhnum"] = xydzddata["shfzh18"].str.len()
xydzddata = xydzddata[xydzddata.shfzhnum==18]
xydzddata["bornyear"]=xydzddata["shfzh18"].str.slice(6,10)
xydzddata["sex"]=xydzddata["shfzh18"].str.get(16)
xydzddata["address"]=xydzddata["shfzh18"].str.slice(0,2)
xydzddata["shfzhnum"] = xydzddata["shfzh18"].str.len()



xydzddata['year'] = xydzddata['hkrq'].str.slice(0,4).astype(int)
xydzddata['month'] = xydzddata['hkrq'].str.slice(5,7).astype(int)



xydzddata["nnn"] = 1
xydzddata["bornyear"] = xydzddata["bornyear"].astype(int)
xydzddata["age"] = 2017-xydzddata["bornyear"]
xydzddata["sex"] = xydzddata["sex"].astype(int)
xydzddata["sex"][xydzddata["sex"]%2==0]='女'
xydzddata["sex"][xydzddata["sex"]!='女']='男'



xydzddata['address'] = xydzddata['address'].astype(int)



xydzddata = pd.merge(xydzddata,province, left_on='address', right_on='shfnum', left_index=False, right_index=False ,how='left')
xydzddata = xydzddata[['ajbh','kehu','hkrq','hkmx','shfzh18','sex','age','province','year','month','nnn']]
xydzddata = xydzddata[xydzddata.year>2015]





#每个客户每月回款情况
xydzdhkmx = xydzddata['hkmx'].groupby([xydzddata['kehu'], xydzddata['year'], xydzddata['month']]).sum().reset_index()




#每个月还款次数
xydzddata1 = xydzddata[xydzddata.hkmx>0]
hkcsh = xydzddata1['ajbh'].groupby([xydzddata1['kehu'], xydzddata1['year'], xydzddata1['month']]).count().reset_index()





#每个月还款案件
xydzddata2 = xydzddata[xydzddata.hkmx>0]
xydzddata2 = xydzddata2[['ajbh','kehu','year','month']]
xydzddata2 = xydzddata2.drop_duplicates()
hkaj = xydzddata2['ajbh'].groupby([xydzddata1['kehu'], xydzddata1['year'], xydzddata1['month']]).count().reset_index()




#地区图
region = xydzddata1['nnn'].groupby([xydzddata1['kehu'], xydzddata1['year'], xydzddata1['province']]).count().reset_index()



bins = [18,30,40,50,100]

group_names = ['20-30','30-40','40-50','50以上']

xydzddata1['age1']=pd.cut(xydzddata1['age'],bins,labels=group_names)







agedata = xydzddata1['nnn'].groupby([xydzddata1['kehu'], xydzddata1['age1']]).count().reset_index()
agedata = agedata[(agedata.kehu == '兴业') | (agedata.kehu == '广发')]



xybasedata = xybase[['ajbh','kehu','shfzh18','zjqkje','zjshje','jdsj']]
xybasedata = xybasedata[xybasedata.zjqkje>0]


xybasedata['year'] = xybasedata['jdsj'].str.slice(0,4).astype(int)
xybasedata['month'] = xybasedata['jdsj'].str.slice(5,7).astype(int)


xybasedata = xybasedata[xybasedata.year>2015]


#xybase去重
xybasedata = xybasedata.drop_duplicates()



xybasezhanbi = xybasedata[['zjqkje','zjshje']].groupby([xybasedata['kehu'], xybasedata['year'], xybasedata['month']]).sum().reset_index()


xybasezhanbi['zhanbi'] =round(xybasezhanbi['zjshje']/xybasezhanbi['zjqkje'],5)




xingyehkmx = xydzdhkmx[(xydzdhkmx.kehu == '兴业')]
guangfahkmx = xydzdhkmx[(xydzdhkmx.kehu == '广发')]


get_ipython().magic('matplotlib inline')
sns.set_style("whitegrid")
sns.set_context("talk")
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']  
mpl.rcParams['axes.unicode_minus'] = False 
ax = sns.barplot(x="month", y="hkmx", hue="year", data=xingyehkmx)
ax.set_xlabel('月份',fontsize=15)
ax.set_ylabel('还款总额',fontsize=15)
ax.set_title('兴业客户',fontsize=15)
plt.show()



ax1 = sns.barplot(x="month", y="hkmx", hue="year", data=guangfahkmx)
ax1.set_xlabel('月份',fontsize=15)
ax1.set_ylabel('还款总额',fontsize=15)
ax1.set_title('广发客户',fontsize=15)
plt.show()



xingyehkzhb = xybasezhanbi[(xybasezhanbi.kehu == '兴业')]
guangfahkzhb = xybasezhanbi[(xybasezhanbi.kehu == '广发')]
xingyehkzhb['year'] = xingyehkzhb['year'].astype(str)
guangfahkzhb['year'] = guangfahkzhb['year'].astype(str)



ggplot(aes(x='month', y='zhanbi', colour='year'), data=xingyehkzhb) +   geom_point()+    geom_line()+    xlab('月份')+    ylab('还款占比')+    ggtitle('兴业客户还款占比情况')+    scale_x_continuous(breaks=range(1,13))


ggplot(aes(x='month', y='zhanbi', colour='year'), data=guangfahkzhb) +   geom_point()+    geom_line()+    xlab('月份')+    ylab('还款占比')+    ggtitle('广发客户还款占比情况')+    scale_x_continuous(breaks=range(1,13))


plt.figure(1)
plt.figure(2) 
plt1=plt.subplot(221)
plt2=plt.subplot(222)
plt.figure(1) 
ax2 = sns.barplot(x="age1", y="nnn", hue="kehu", data=agedata)
ax2.set_xlabel('年龄段',fontsize=15)
ax2.set_ylabel('数量',fontsize=15)
ax2.set_title('年龄段回款分析',fontsize=15)
plt.sca(plt1)  
explode = [0, 0.1, 0, 0] 
xingyeagedata = agedata[agedata.kehu=='兴业']

plt.pie(x=xingyeagedata['nnn'], labels=xingyeagedata['age1'],  explode=explode, autopct='%3.1f %%',        shadow=True, labeldistance=1.1,   startangle = 90,pctdistance = 0.6)

plt.title('兴业客户年龄段回款情况')

plt.sca(plt2)  
explode = [0, 0.1, 0, 0] 
guangfaagedata = agedata[agedata.kehu=='广发']

plt.title('广发客户年龄段回款情况')
plt.pie(x=guangfaagedata['nnn'], labels=guangfaagedata['age1'], explode=explode,  autopct='%3.1f %%',        shadow=True,  labeldistance=1.1,  startangle = 90,pctdistance = 0.6)

plt.show()
