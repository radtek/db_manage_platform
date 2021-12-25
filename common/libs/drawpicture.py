# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import datetime
import cx_Oracle
import os
import time as t

username = 'xxx'
password = 'xxx'
host = 'xxx'
port = 'xxx'
sid = 'xxx'
base_dir = "E:\\project\\dbmanage_v4\\static"

class DbOper(object):
    def __init__(self,user,pwd,host,port,sid):
        self.user = user
        self.pwd = pwd
        self.host = host
        self.port = port
        self.sid = sid
        self.tns_name = cx_Oracle.makedsn(host=host,port=port,sid=sid)
        self.oracledb = cx_Oracle.connect(user, pwd, self.tns_name)

    def dboper(self,sql):
        try:
            with self.oracledb.cursor() as cursor:
                cursor.execute(sql)
                result_set = cursor.fetchall()
        except Exception as e:
            print('错误信息：{0}'.format(e))
        finally:
            self.oracledb.close()
            return result_set

class DataParse(object):
    @staticmethod
    def tbs_parse(ip,tbs,time):
        sql = '''
select a.used_ratio,to_char(a.gettime,'YYYY-mm-dd') from tablespace_size_new a,server_order b where a.gettime>=sysdate-{0}
and a.ip=b.ip
and a.ip='{1}'
and trim(a.tablespace_name)='{2}'
'''.format(time,ip,tbs)
        obj = DbOper(username, password, host, port, sid)
        result_set = obj.dboper(sql)
        used_ratio_list = []
        gettime_list = []
        for i in range(len(result_set)):
            used_ratio_list.append(result_set[i][0].strip().strip('%'))
        for i in range(len(result_set)):
            gettime_list.append(str(result_set[i][1]).strip())
        data = {
            'gettime': gettime_list,
            'used_ratio': used_ratio_list
        }
        df = pd.DataFrame(data=data)
        df['gettime'] = df['gettime'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
        df['used_ratio'] = df['used_ratio'].apply(lambda x: float(x))
        # 绘图
        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['font.size'] = 8
        plt.rcParams['axes.unicode_minus'] = False
        plt.figure(figsize=(12,5))
        plt.bar(df['gettime'],df['used_ratio'],color='green',width=0.3,label='{0}使用情况'.format(tbs))
        plt.title('表空间使用情况')
        plt.legend()
        plt.xlabel('时间')
        plt.ylabel('使用率')
        pic_path = base_dir + '\\pic'
        if not os.path.exists(pic_path):
            os.mkdir(pic_path)
        plt.savefig(pic_path + '\\common.jpg')
        t.sleep(10)

    @staticmethod
    def aas_parse(ip,time):
        sql = '''
select snap_time,aas_1 from aas_tab
where ip='{0}' 
and to_date(snap_time,'YYYY-mm_dd hh24:mi:ss')>=sysdate-{1}
'''.format(ip,time)
        obj = DbOper(username, password, host, port, sid)
        result_set = obj.dboper(sql)
        snap_time_list = []
        aas_list = []
        for i in range(len(result_set)):
            snap_time_list.append(result_set[i][0].strip())
        for i in range(len(result_set)):
            aas_list.append(str(result_set[i][1]).strip())
        data = {
            'snap_time': snap_time_list,
            'aas': aas_list
        }
        df = pd.DataFrame(data=data)
        df['snap_time'] = df['snap_time'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M'))
        df['aas'] = df['aas'].apply(lambda x: float(x))
        # 绘图
        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['font.size'] = 8
        plt.rcParams['axes.unicode_minus'] = False
        plt.figure(figsize=(12, 5))
        plt.plot(df['snap_time'], df['aas'], color='green',label='aas负载情况')
        plt.title('aas负载情况')
        plt.legend()
        plt.xlabel('时间')
        plt.ylabel('aas负载')
        pic_path = base_dir + '\\pic'
        if not os.path.exists(pic_path):
            os.mkdir(pic_path)
        plt.savefig(pic_path + '\\common.jpg')
        t.sleep(10)
