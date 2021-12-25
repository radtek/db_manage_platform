# -*- coding:utf-8 -*-

import paramiko
import os
import time
import configparser

class OswOper(object):
    @staticmethod
    def create_all_osw_zip_file(username,hostname,password):
        remote_os_path = "/oratools/sw/oswbb/analysis"
        remote_ls_cmd = "ls -ltrh %s" % remote_os_path
        remote_tar_cmd = "zip -r %s.zip %s"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(username=username,password=password,hostname=hostname)
        stdin,stdout,stderr = ssh.exec_command(remote_ls_cmd)
        result_list = stdout.read().decode('utf-8').strip('\n').split('\n')
        start_point = len(result_list) - 4
        end_point = len(result_list)
        out_name = []
        print("=======================================================================")
        for index in range(start_point,end_point):
            row_list = result_list[index].split(' ')
            name = row_list[len(row_list) - 1]
            new_name = remote_os_path + '/' + name
            out_name.append(name)
            new_cmd = remote_tar_cmd % (new_name,new_name)
            new_command = 'source /oracle/home/.bash_profile;' + new_cmd
            stdin, stdout, stderr = ssh.exec_command(new_command)
            time.sleep(5)
            print("'%s'压缩osw文件成功！" % name)
        ssh.close()
        return out_name

    #10.114.130.2上下载的指定osw压缩文件到本地
    @staticmethod
    def get_remote_osw_zip_file(host_ip, username, password,out_name):
        t = paramiko.Transport((host_ip, 22))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        print("=======================================================================")
        remote_os_path = "/oratools/sw/oswbb/analysis"
        config = configparser.ConfigParser()
        config.read('D\\project\\dbmanage_v4\\common\\libs\\dbcheck\\Setup.ini', encoding='utf-8')
        sec2 = config['base']
        for index in range(len(out_name)):
            src = remote_os_path + '/' + out_name[index] + '.zip'
            osw_base = sec2['base_dir'] + 'osw'
            osw_file_path = sec2['base_dir'] + 'osw\\' + out_name[index]
            des = osw_file_path + '\\' + out_name[index] + '.zip'
            if not os.path.exists(osw_base):
                os.mkdir(osw_base)
            if not os.path.exists(osw_file_path):
                os.mkdir(osw_file_path)
            sftp.get(src,des)
            print("'%s'压缩文件已经下载！" % out_name[index])
            time.sleep(5)
        t.close()

    #解压本地osw压缩文件
    @staticmethod
    def unzip_local_osw_file(ip_list:list):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbcheck\\Setup.ini', encoding='utf-8')
        sec2 = config['base']
        osw_path = sec2['base_dir'] + 'osw'
        local_unzip_cmd = "unzip %s -d %s"
        if os.path.exists(osw_path):
            osw_name_list = os.listdir(osw_path)
            print("=======================================================================")
            for idx in range(len(ip_list)):
                for index in range(len(osw_name_list)):
                    if ip_list[idx].split('.')[-1] in osw_name_list[index].split('_'):
                        zip_list = os.listdir(osw_path + '\\' + osw_name_list[index])
                        zip_file_name = osw_path + '\\' + osw_name_list[index] + '\\' + zip_list[0]
                        os.system(local_unzip_cmd % (zip_file_name,osw_path + '\\' + osw_name_list[index] + '\\'))
                        print("'%s'压缩文件解压完成" % osw_name_list[index])
                        time.sleep(5)
        else:
            print("'%s'存放的osw压缩文件的文件夹不存在，osw压缩文件没有下载成功！" % osw_path)
