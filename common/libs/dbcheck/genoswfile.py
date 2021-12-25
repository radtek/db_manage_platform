# -*- coding:utf-8 -*-

import paramiko
import time
import os
import re
import datetime

class GenOswFile(object):
    @staticmethod
    def gen_osw_file(ip):
        ip_info_list = os.popen('ipconfig').readlines()
        host_ip = ''
        ip_match = r'^10\.122\.*'
        regex_ip = re.compile(ip_match)
        ip_name = ip.split('.')[-1]
        for i in ip_info_list:
            if i.split(':')[0].strip() == 'IPv4 地址 . . . . . . . . . . . .':
                if regex_ip.search(i.split(':')[1].strip().strip('\n')):
                    host_ip = i.split(':')[1].strip().strip('\n')
        mon_dict = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
                    '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
                    '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
                    }
        today = datetime.date.today().strftime('%Y-%m-%d')
        year_today = today.split('-')[0]
        mon_today = today.split('-')[1]
        day_today = today.split('-')[-1]
        dir = ''
        if ip_name == '86' or ip_name == '87':
            dir = '{0}_{1}_{2}_{3}_1200_1200'.format(year_today, mon_today, day_today, ip_name)
        if ip_name == '200' or ip_name == '201' or ip_name == '198' or ip_name == '199':
            dir = '{0}_{1}_{2}_{3}_0700_0700'.format(year_today, mon_today, day_today, ip_name)
        if mon_today in mon_dict:
            mon_today = mon_dict[mon_today]
        yestoday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
        year_yestoday = yestoday.split('-')[0]
        mon_yestoday = yestoday.split('-')[1]
        if mon_yestoday in mon_dict:
            mon_yestoday = mon_dict[mon_yestoday]
        day_yestoday = yestoday.split('-')[-1]
        remote_cmd_1 = 'export DISPLAY={0}:0.0;'.format(host_ip)
        remote_cmd_2 = 'cd /oratools/sw/oswbb;'
        remote_cmd_3 = ''
        if ip_name == '86' or ip_name == '87':
            remote_cmd_3 = '/usr/bin/java -jar \
            oswbba.jar -i archive/{0} \
            -b {1} {2} 12:00:00 {3} \
            -e {4} {5} 12:00:00 {6};'.format(ip_name,mon_yestoday,day_yestoday,year_yestoday,mon_today,day_today,year_today)
        if ip_name == '200' or ip_name == '201' or ip_name == '198' or ip_name == '199':
            remote_cmd_3 = '/usr/bin/java -jar \
                    oswbba.jar -i archive/{0} \
                    -b {1} {2} 07:00:00 {3} \
                    -e {4} {5} 07:00:00 {6};'.format(ip_name, mon_yestoday, day_yestoday, year_yestoday, mon_today,
                                                     day_today, year_today)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(username='oracle',password='oracle',hostname='10.114.130.2')
        stdin,stdout,stderr = ssh.exec_command(remote_cmd_1 + remote_cmd_2 + remote_cmd_3)
        # if ip_name == '86' or ip_name == '87':
        #     time.sleep(300)
        # if ip_name == '200' or ip_name == '201' or ip_name == '198' or ip_name == '199':
        #     time.sleep(300)
        time.sleep(300)
        stdin.write('D\n')
        time.sleep(3)
        stdin.write(dir + '\n')
        time.sleep(30)
        stdin.write('Q\n')
        ssh.close()
