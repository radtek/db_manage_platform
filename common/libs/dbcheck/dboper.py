# -*- coding:utf-8 -*-

import cx_Oracle

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