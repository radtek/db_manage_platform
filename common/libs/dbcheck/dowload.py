# -*- coding:utf-8 -*-

import paramiko
import os
import configparser

class DownLoad(object):
    def __init__(self,system_user,system_pwd,system_host):
        self.system_user = system_user
        self.system_pwd = system_pwd
        self.system_host = system_host

    def get_all_remote_log_filename(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(username=self.system_user, password=self.system_pwd, hostname=self.system_host)
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbcheck\\Setup.ini', encoding='utf-8')
        sec2 = config['base']
        stdin, stdout, stderr = ssh.exec_command('source /oracle/home/.bash_profile;ls %s' % sec2['remote_log_dir'])
        result_list = stdout.read().decode('utf-8').strip('\n').split('\n')
        return result_list

    def get_all_remote_log_file(self,result_list):
        t = paramiko.Transport((self.system_host, 22))
        t.connect(username=self.system_user, password=self.system_pwd)
        sftp = paramiko.SFTPClient.from_transport(t)
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbcheck\\Setup.ini', encoding='utf-8')
        sec2 = config['base']
        log_path = sec2['base_dir'] + 'log'
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        for file_name in result_list:
            src = sec2['remote_log_dir'] + file_name
            des = log_path + '\\' + file_name
            sftp.get(src, des)
            print("'%s'日志文件已经下载！" % file_name)
        t.close()