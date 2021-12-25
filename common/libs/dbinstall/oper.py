# -*- coding:utf-8 -*-

import paramiko
import datetime

class Oper(object):
    def __init__(self,system_user,system_pwd,system_host):
        self.system_user = system_user
        self.system_pwd = system_pwd
        self.system_host = system_host

    def command(self,cmd):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(username=self.system_user, password=self.system_pwd, hostname=self.system_host)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            return stdout.read().decode('utf-8').strip('\n')
        except Exception as e:
            print('错误信息：{0}'.format(e))

    def upload(self,local_file,remote_file):
        try:
            t = paramiko.Transport((self.system_host, 22))
            t.connect(username=self.system_user, password=self.system_pwd)
            sftp = paramiko.SFTPClient.from_transport(t)
            print('开始上传文件%s ' % datetime.datetime.now())
            try:
                sftp.put(local_file, remote_file)
            except Exception as e:
                print('错误信息：{0}'.format(e))
                print("从本地：{0}上传到：{1}操作失败！".format(local_file, remote_file))
            print('文件上传成功 %s ' % datetime.datetime.now())
            t.close()
        except Exception as e:
            print('错误信息：{0}'.format(e))
