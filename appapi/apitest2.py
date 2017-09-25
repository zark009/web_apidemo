from appapi.utils import *
import time, datetime
import random

import pymysql

conn = pymysql.connect(host='127.0.0.1',port= 3306,user = 'root',passwd='123456',db='zallsat',charset='utf8') #db：库名
#创建游标
cur = conn.cursor()
#查询lcj表中存在的数据

sql="select * from t_api"
cur.execute(sql)
ret1 = cur.fetchall()
print(ret1)

conn.close()


