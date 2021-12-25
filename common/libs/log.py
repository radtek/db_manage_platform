# -*- coding: utf-8 -*-

import paramiko
import os
import re

remote_log_dir = '/oracle/home/alterlog'
base_dir = "E:\\daily_data"

class DownLoad(object):
    def __init__(self,system_user,system_pwd,system_host):
        self.system_user = system_user
        self.system_pwd = system_pwd
        self.system_host = system_host

    def get_all_remote_log_filename(self,ip,type):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(username=self.system_user, password=self.system_pwd, hostname=self.system_host)
        stdin, stdout, stderr = ssh.exec_command('source /oracle/home/.bash_profile;ls %s' % remote_log_dir)
        result_list = stdout.read().decode('utf-8').strip('\n').split('\n')
        log_name = type + '_' + ip.split('.')[-1] + '.log'
        for name in result_list:
            if log_name == name:
                return name

    def get_all_remote_log_file(self,name):
        t = paramiko.Transport((self.system_host, 22))
        t.connect(username=self.system_user, password=self.system_pwd)
        sftp = paramiko.SFTPClient.from_transport(t)
        log_path = base_dir + '\\log'
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        src = remote_log_dir + '/' + name
        des = log_path + '\\' + name
        sftp.get(src, des)
        print("'%s'日志文件已经下载！" % name)
        t.close()

class Checklog(object):
    # 日志分类
    @staticmethod
    def logclassify(log_path):
        p_alert = r'alter_(?:\d)*\.log'
        p_oslog = r'oslog_(?:\d)*\.log'
        regex_alert = re.compile(p_alert)
        regex_oslog = re.compile(p_oslog)
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
    def dberror(alterlog_list,ip):
        dblog_path_list = []
        p_db_error = r'.*(TNS-)|(ORA-)|(ERROR)|(Error)|(error).*'
        regex_db_error = re.compile(p_db_error)
        for i in range(len(alterlog_list)):
            if alterlog_list[i] == 'alter_' + ip.split('.')[-1] + '.log':
                filename = base_dir + '\\log' + '\\' + alterlog_list[i]
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
                    return result
        return result

    # 查找系统日志报错
    @staticmethod
    def oserror(oslog_list,ip):
        p_os_error = r'.*(Error)|(error)|(ERROR)|(WARNING)|(warning)|(Warning).*'
        regex_os_error = re.compile(p_os_error)
        oslog_path_list = []
        result = []
        for i in range(len(oslog_list)):
            if oslog_list[i] == 'oslog_' + ip.split('.')[-1] + '.log':
                filename = base_dir + '\\log' + '\\' + oslog_list[i]
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
                    return result
        return result