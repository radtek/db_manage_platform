# -*- coding:utf-8 -*-

import os
import re
import configparser

class Checklog(object):
    # 日志分类
    @staticmethod
    def logclassify(log_path):
        # 配置正则表达式
        p_alert = r'alter_(?:\d)*\.log'
        p_oslog = r'oslog_(?:\d)*\.log'
        p_db_error = r'.*(TNS-)|(ORA-)|(ERROR)|(Error)|(error).*'
        p_os_error = r'.*(Error)|(error)|(ERROR)|(WARNING)|(warning)|(Warning).*'
        regex_alert = re.compile(p_alert)
        regex_oslog = re.compile(p_oslog)
        regex_db_error = re.compile(p_db_error)
        regex_os_error = re.compile(p_os_error)
        if os.path.exists(log_path):
            logfile_list = os.listdir(log_path)
            logfile_string = ','.join(logfile_list)
            alterlog_list = regex_alert.findall(logfile_string)
            oslog_list = regex_oslog.findall(logfile_string)
            return alterlog_list,oslog_list
        else:
            return None

    # 查找数据库日志报错
    @staticmethod
    def dberror(alterlog_list):
        dblog_path_list = []
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbcheck\\Setup.ini', encoding='utf-8')
        sec2 = config['base']
        # 配置正则表达式
        p_alert = r'alter_(?:\d)*\.log'
        p_oslog = r'oslog_(?:\d)*\.log'
        p_db_error = r'.*(TNS-)|(ORA-)|(ERROR)|(Error)|(error).*'
        p_os_error = r'.*(Error)|(error)|(ERROR)|(WARNING)|(warning)|(Warning).*'
        regex_alert = re.compile(p_alert)
        regex_oslog = re.compile(p_oslog)
        regex_db_error = re.compile(p_db_error)
        regex_os_error = re.compile(p_os_error)
        for i in range(len(alterlog_list)):
            filename = sec2['local_log_dir']  + alterlog_list[i]
            dblog_path_list.append(filename)

        result = []
        if len(dblog_path_list) == 0:
            result.append('找不到数据库告警日志\n')
            return result

        for dbfile in dblog_path_list:
            basename = os.path.basename(dbfile)
            dbname = basename.split('.')[0].split('_')[1]
            result.append('{0}节点数据库告警信息如下：\n'.format(dbname))
            with open(file=dbfile,mode='r',encoding='gbk') as f:
                index = 0
                current_line = f.readline()
                while current_line:
                    if regex_db_error.search(current_line):
                        result.append(current_line)
                        index += 1
                    current_line = f.readline()
                if index == 0:
                    result.append('无错误信息\n')

        with open(file=sec2['local_db_log'],mode='w',encoding='gbk') as f:
            f.writelines(result)


    # 查找系统日志报错
    @staticmethod
    def oserror(oslog_list):
        # 配置正则表达式
        p_alert = r'alter_(?:\d)*\.log'
        p_oslog = r'oslog_(?:\d)*\.log'
        p_db_error = r'.*(TNS-)|(ORA-)|(ERROR)|(Error)|(error).*'
        p_os_error = r'.*(Error)|(error)|(ERROR)|(WARNING)|(warning)|(Warning).*'
        regex_alert = re.compile(p_alert)
        regex_oslog = re.compile(p_oslog)
        regex_db_error = re.compile(p_db_error)
        regex_os_error = re.compile(p_os_error)
        oslog_path_list = []
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbcheck\\Setup.ini', encoding='utf-8')
        sec2 = config['base']
        result = []

        for i in range(len(oslog_list)):
            filename = sec2['local_log_dir'] + oslog_list[i]
            oslog_path_list.append(filename)

        if len(oslog_path_list) == 0:
            result.append('找不到系统日志\n')
            return result

        for osfile in oslog_path_list:
            basename = os.path.basename(osfile)
            osname = basename.split('.')[0].split('_')[1]
            result.append('{0}节点系统告警信息如下：\n'.format(osname))
            with open(file=osfile, mode='r', encoding='gbk') as f:
                index = 0
                current_line = f.readline()
                while current_line:
                    if regex_os_error.search(current_line):
                        result.append(current_line)
                        index += 1
                    current_line = f.readline()
                if index == 0:
                    result.append('无错误信息\n')

        with open(file=sec2['local_os_log'], mode='w', encoding='gbk') as f:
            f.writelines(result)
