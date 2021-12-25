# -*- coding: utf-8 -*-

import cx_Oracle

#配置信息
username = 'xxx'
password = 'xxx'
host = 'xxx'
port = 'xxx'
sid = 'xxx'
arch_dest_1 = "归档路径：USE_DB_RECOVERY_FILE_DEST=+ARCHDG\n"
arch_dest_2 = "归档路径：/oracle_data/app/oracle/fast_recovery_area\n"
arch_dest_3 = "归档路径：/oracle_data/app/oracle/fast_recovery_area/archivedb\n"
arch_info = {'xxx':arch_dest_1,'xxx':arch_dest_1,'xxx':arch_dest_1,'xxx':arch_dest_2,'xxx':arch_dest_3}

#命令
sql_1 = "select a.* from table_startup a,server_order b where a.gettime>=sysdate-%s \
and a.ip=b.ip and a.ip='%s'"

sql_2 = "select a.* from tablespace_size_new a,server_order b where a.gettime>=sysdate-%s \
and a.ip=b.ip and a.tablespace_name not in ('                TEMP','               TEMP1') \
and a.ip='%s'"

sql_3 = "select a.* \
from count_tab a,server_order b \
where a.ip=b.ip and a.ip='%s' and a.gettime>=sysdate-%s"

sql_4 = "select a.* from mon_scheduler_job a,server_order b \
where a.ip=b.ip and a.ip='%s' and a.gettime>=sysdate-%s"

sql_5 = "select count(*) from mon_scheduler_job a,server_order b \
where a.ip=b.ip and a.gettime>=sysdate-1/24 \
order by b.id"

sql_6 = '''
SELECT a.ip,a.START_TIME,to_char(a.END_TIME,'yyyy-mm-dd hh24:mi:ss'),a.STATUS
FROM backup_status a,server_order b 
WHERE  a.ip=b.ip and a.gettime>sysdate-%s
and to_char(start_time,'YYYY-MM-DD HH24:MI:SS')>= to_char(sysdate-%s,'YYYY-MM-DD HH24:MI:SS')
and a.ip='%s'
'''

sql_7 = """SELECT a.*
FROM archive_log a,server_order b 
WHERE  a.ip=b.ip and a.gettime>sysdate-{0} 
and a like '最近一次归档%'
and a.ip='{1}'
"""

sql_8 = "select a.* from hit_table a ,server_order b ,hit_order c \
WHERE  a.ip=b.ip and a.ip='%s' and a.gettime>sysdate-%s  and substr(a.hit,1,7)=substr(c.name,1,7) \
ORDER BY b.id,c.id"

#获取数据库startup_time监控数据
def get_startuptime_data(ip,time):
    try:
        tns_name = cx_Oracle.makedsn(host=host, port=port, sid=sid)
        oracledb = cx_Oracle.connect(username, password, tns_name)
        cursor = oracledb.cursor()
        new_sql_1 = sql_1 % (time,ip)
        cursor.execute(new_sql_1)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print("'%s'获取startup_time监控指标数据失败！\n错误信息：'%s'" % (ip,str(e)))
    finally:
        cursor.close()
        oracledb.close()

# 获取表空间使用率监控数据
def get_tbs_used_data(ip,time):
    try:
        tns_name = cx_Oracle.makedsn(host=host, port=port, sid=sid)
        oracledb = cx_Oracle.connect(username, password, tns_name)
        cursor = oracledb.cursor()
        message = {}
        new_sql_2 = sql_2 % (time,ip)
        cursor.execute(new_sql_2)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print("'%s'获取tbs_used监控指标数据失败！\n错误信息：'%s'" % (ip,str(e)))
    finally:
        cursor.close()
        oracledb.close()

#获取数据库更新对象监控数据
def get_update_obj_data(ip,time):
    try:
        tns_name = cx_Oracle.makedsn(host=host, port=port, sid=sid)
        oracledb = cx_Oracle.connect(username, password, tns_name)
        cursor = oracledb.cursor()
        new_sql_3 = sql_3 % (ip,time)
        cursor.execute(new_sql_3)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print("'%s'获取更新对象监控指标数据失败！\n错误信息：'%s'" % (ip,str(e)))
    finally:
        cursor.close()
        oracledb.close()

#获取数据库作业调度监控数据
def get_scheduler_job_data(ip,time):
    try:
        tns_name = cx_Oracle.makedsn(host=host, port=port, sid=sid)
        oracledb = cx_Oracle.connect(username, password, tns_name)
        cursor = oracledb.cursor()
        new_sql_4 = sql_4 % (ip, time)
        cursor.execute(new_sql_4)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print("'%s'获取作业调度监控指标数据失败！\n错误信息：'%s'" % (ip, str(e)))
    finally:
        cursor.close()
        oracledb.close()

#获取数据库备份监控数据
def get_dbbackup_data(ip,time):
    try:
        tns_name = cx_Oracle.makedsn(host=host, port=port, sid=sid)
        oracledb = cx_Oracle.connect(username, password, tns_name)
        cursor = oracledb.cursor()
        new_sql_6 = sql_6 % (time,time,ip)
        cursor.execute(new_sql_6)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print("'%s'获取备份信息指标数据失败！\n错误信息：'%s'" % (ip,str(e)))
    finally:
        cursor.close()
        oracledb.close()

#获取数据库归档日志指标数据
def get_archlog_data(ip,time):
    try:
        tns_name = cx_Oracle.makedsn(host=host, port=port, sid=sid)
        oracledb = cx_Oracle.connect(username, password, tns_name)
        cursor = oracledb.cursor()
        new_sql_7 = sql_7.format(time,ip)
        cursor.execute(new_sql_7)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print("'%s'获取归档相关监控指标数据失败！\n错误信息：'%s'" % (ip, str(e)))
    finally:
        cursor.close()
        oracledb.close()

#获取数据库性能相关指标数据
def get_db_perform_data(ip,time):
    try:
        tns_name = cx_Oracle.makedsn(host=host, port=port, sid=sid)
        oracledb = cx_Oracle.connect(username, password, tns_name)
        cursor = oracledb.cursor()
        new_sql_8 = sql_8 % (ip,time)
        cursor.execute(new_sql_8)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print("'%s'获取数据库性能相关监控指标数据失败！\n错误信息：'%s'" % (ip, str(e)))
    finally:
        cursor.close()
        oracledb.close()