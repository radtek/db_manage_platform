# -*- coding:utf-8 -*-

import time
import cx_Oracle
import xlrd
import xlwt
import os
import paramiko
from xlutils.copy import copy
import xlwings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import logging.config
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import datetime
import pythoncom

#配置信息
username = 'xxx'
password = 'xxx'
host = 'xxx'
port = 'xxx'
sid = 'xxx'
xls_name = r"E:\daily_data\数据库日常监控通报-2021-08-08.xls"
new_xls_name = r"E:\daily_data\数据库日常监控通报-2021-08-08_new.xls"
db_info = {'xxx':'T_130_9','xxx':'T_130_8','xxx':'T_130_85_REP','xxx':'T_130_85_ARC'}
ip_list = ['xxx','xxx','xxx','xxx']
arch_dest_1 = "归档路径：\nUSE_DB_RECOVERY_FILE_DEST=+ARCHDG\n"
arch_dest_2 = "归档路径：\n/oracle_data/app/oracle/fast_recovery_area\n"
arch_dest_3 = "归档路径：\n/oracle_data/app/oracle/fast_recovery_area/archivedb\n"
arch_info = {'xxx':arch_dest_1,'xxx':arch_dest_1,'xxx':arch_dest_2,'xxx':arch_dest_3}
remote_os_path = "/oratools/sw/oswbb/analysis"
base_dir = r"E:\daily_data"
remote_alertlog_path = "/oracle/home/alterlog"
osw_sheet_list = ['OSW-xxx','OSW-xxx','OSW-xxx','OSW-xxx']
dblog_sheet_list = ['Alterlog-xxx','Alterlog-xxx','Alterlog-xxx','Alterlog-xxx']
oslog_sheet_list = ['OSlog-xxx','OSlog-xxx','OSlog-xxx','OSlog-xxx']
LOG_PATH = r'E:\daily_data\alertlog'

# 日志配置
logging.config.fileConfig('E:\\project\\dbmanage_v4\\common\\libs\\daily\\logger.conf')
logger = logging.getLogger('logger1')

# 配置正则表达式
p_alert = r'alter_(?:\d)*\.log'
p_oslog = r'oslog_(?:\d)*\.log'
p_db_error = r'.*(TNS-)|(ORA-)|(ERROR)|(Error)|(error).*'
p_os_error = r'.*(Error)|(error)|(ERROR)|(WARNING)|(warning)|(Warning).*'
regex_alert = re.compile(p_alert)
regex_oslog = re.compile(p_oslog)
regex_db_error = re.compile(p_db_error)
regex_os_error = re.compile(p_os_error)

# 邮箱配置
mail_host = 'xxx'
mail_user = 'xxx'
mail_pass = 'xxx'
sender = 'xxx'
receivers = ['xxx','xxx']

#excel表格设置写入字体
style = xlwt.XFStyle()
font = xlwt.Font()
font.name = "Microsoft YaHei UI"
font.bold = False        #是否加粗
font.underline = False   #是否有下划线
font.italic = False      #是否为斜体
font.height = 20*9       #字体高度
font.escapement = xlwt.Font.ESCAPEMENT_NONE     #无字体效果
style.font = font

#excel表格设置写入对齐
aligment = xlwt.Alignment()
aligment.vert = xlwt.Alignment.VERT_CENTER       #水平方向向上对齐
aligment.horz = xlwt.Alignment.HORZ_CENTER       #垂直方向向右对齐
style.alignment = aligment

#excel表格设置边框
borders = xlwt.Borders()
borders.top = 1                 #上边框粗细
borders.bottom = 1              #下边框粗细
borders.left = 1                #左边框粗细
borders.right = 1               #右边框粗细
style.borders = borders

#命令
sql_1 = "select distinct(a.startup_time) from table_startup a,server_order b \
where a.gettime>=sysdate-1/24 and a.ip=b.ip and a.ip='%s'"

sql_2 = "select distinct a.tablespace_name,a.used_ratio from tablespace_size_new a,server_order b where a.gettime>=sysdate-1/24 \
and a.ip=b.ip and a.tablespace_name not in ('                TEMP','               TEMP1') \
and a.ip='%s'"

sql_3 = "select distinct a.count_tab \
from count_tab a,server_order b \
where a.ip=b.ip and a.ip='%s' and a.gettime>=sysdate-1/24"

sql_4 = "select distinct distinct a.job_name from mon_scheduler_job a,server_order b \
where a.ip=b.ip and a.ip='%s' and a.gettime>=sysdate-1/24"

sql_5 = "select count(*) from mon_scheduler_job a,server_order b \
where a.ip=b.ip and a.gettime>=sysdate-1/24 \
order by b.id"

sql_6 = "select * from (\
SELECT to_char(a.start_time,'yyyy-mm-dd hh24:mi:ss'),a.STATUS \
FROM new_backup_status a,server_order b \
WHERE  a.ip=b.ip and a.gettime>sysdate-10/24 and a.INPUT_TYPE='DB INCR' and a.ip='%s' \
and to_char(start_time,'YYYY-MM-DD HH24:MI:SS')>= to_char(sysdate-1,'YYYY-MM-DD HH24:MI:SS') \
ORDER BY to_char(a.start_time,'YYYY-MM-DD HH24:MI:SS') desc) \
where rownum=1"

sql_7 = "SELECT distinct a.A \
FROM archive_log a,server_order b \
WHERE a.ip=b.ip and a.gettime>sysdate-1/24 \
and a.ip='%s'and A like '最近一次归档%s'"

sql_8 = "select distinct a.hit from hit_table a ,server_order b ,hit_order c \
WHERE  a.ip=b.ip and a.gettime>sysdate-1/24 and a.ip='%s'\
and substr(a.hit,1,7)=substr(c.name,1,7)"

remote_ls_cmd = "ls -ltrh %s" % remote_os_path
remote_tar_cmd = "zip -r %s.zip %s"
local_unzip_cmd = "unzip %s -d %s"

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

'''oracle监控数据获取写入excel表'''
#获取数据库startup_time监控数据
def get_startuptime_data(db_list,new_workbook):
    try:
        #excel表中获取和写入"startup_time"监控数据
        logger.info("=======================================================================")
        new_sheet = new_workbook.get_sheet(2)
        for index in range(len(list(db_list))):
            new_sql_1 = sql_1 % db_list[index]
            obj = DbOper(user=username,pwd=password,host=host,port=port,sid=sid)
            data = obj.dboper(new_sql_1)
            startup_time = str(data[0][0])
            new_sheet.write(index+2,1,startup_time,style)
            logger.info("'%s'的startup_time时间为'%s'" % (db_list[index],startup_time))
            logger.info("'%s'获取和写入startup_time监控指标数据成功！" % db_list[index])
    except Exception as e:
        logger.info("'%s'获取和写入startup_time监控指标数据失败！\n错误信息：'%s'" % (db_list[index],str(e)))

# 获取表空间使用率监控数据
def get_tbs_used_data(db_list,new_workbook):
    try:
        #excel表中获取和写入"表空间使用率"监控数据
        logger.info("=======================================================================")
        for index in range(len(db_list)):
            message = {}
            new_sql_2 = sql_2 % db_list[index]
            obj = DbOper(user=username, pwd=password, host=host, port=port, sid=sid)
            data = obj.dboper(new_sql_2)
            for tmp_data in data:
                tbs_name = tmp_data[0].strip()
                pct_used = tmp_data[1].strip().split('%')[0]
                if float(pct_used) >= 90:
                    message[tbs_name] = 'abnormal'
                    logger.info("'%s'的'%s'表空间使用率为'%s',不正常!" % (db_list[index],tbs_name,tmp_data[1].strip()))
                else:
                    message[tbs_name] = 'normal'
                    logger.info("'%s'的'%s'表空间使用率为'%s',正常!" % (db_list[index],tbs_name,tmp_data[1].strip()))
            new_sheet = new_workbook.get_sheet(2)
            if 'abnormal' in message.values():
                new_sheet.write(index+2,2,'异常',style)
            else:
                new_sheet.write(index+2,2,'正常',style)
            logger.info("'%s'获取和写入tbs_used监控指标数据成功！" % db_list[index])
    except Exception as e:
        logger.info("'%s'获取和写入tbs_used监控指标数据失败！\n错误信息：'%s'" % (db_list[index],str(e)))

#获取数据库更新对象监控数据
def get_update_obj_data(db_list,new_workbook):
    try:
        #excel表中获取和写入"更新对象"监控数据
        logger.info("=======================================================================")
        new_sheet = new_workbook.get_sheet(2)
        for index in range(len(db_list)):
            new_sql_3 = sql_3 % db_list[index]
            obj = DbOper(user=username, pwd=password, host=host, port=port, sid=sid)
            data = obj.dboper(new_sql_3)
            update_object = '更新' + data[0][0] + '个对象'
            new_sheet.write(index+2,3,update_object,style)
            logger.info("'%s'数据库更新了'%s'个对象！" % (db_list[index],update_object))
            logger.info("'%s'获取和写入更新对象监控指标数据成功！" % db_list[index])
    except Exception as e:
        logger.info("'%s'获取和写入更新对象监控指标数据失败！\n错误信息：'%s'" % (db_list[index],str(e)))

#获取数据库作业调度监控数据
def get_scheduler_job_data(db_list,new_workbook):
    try:
        #excel表中获取和写入"作业调度"监控数据
        obj = DbOper(user=username, pwd=password, host=host, port=port, sid=sid)
        cnt = obj.dboper(sql_5)
        if int(cnt[0][0]) == 0:
            logger.info("=======================================================================")
            new_sheet = new_workbook.get_sheet(2)
            for index in range(len(db_list)):
                new_sheet.write(index + 2, 4, '正常', style)
                logger.info("'%s'数据库作业调度正常！" % db_list[index])
                logger.info("'%s'获取和写入作业调度监控指标数据成功！" % db_list[index])
        elif int(cnt[0][0]) > 0:
            logger.info("=======================================================================")
            new_sheet = new_workbook.get_sheet(2)
            for index in range(len(db_list)):
                new_sql_4 = sql_4 % db_list[index]
                cursor.execute(new_sql_4)
                data = cursor.fetchall()
                new_sheet.write(index + 2, 4, '异常', style)
                logger.info("'%s'数据库作业'%s'调度异常！" % (db_list[index],data[0][0]))
                logger.info("'%s'获取和写入作业调度监控指标数据成功！" % db_list[index])
    except Exception as e:
        logger.info("'%s'获取和写入作业调度监控指标数据失败！\n错误信息：'%s'" % (db_list[index], str(e)))

#获取数据库备份监控数据
def get_dbbackup_data(db_list,new_workbook):
    try:
        #excel表中获取和写入"数据库备份"监控数据
        logger.info("=======================================================================")
        new_sheet = new_workbook.get_sheet(2)
        for index in range(len(db_list)):
            new_sql_6 = sql_6 % db_list[index]
            obj = DbOper(user=username, pwd=password, host=host, port=port, sid=sid)
            data = obj.dboper(new_sql_6)
            msg = "每天%s点执行0级备份\n已于%s执行备份" % (data[0][0].split(' ')[-1],data[0][0])
            new_sheet.write(index + 2, 5, msg, style)
            new_sheet.write(index + 2, 6, data[0][1], style)
            logger.info("'%s'获取和写入备份信息监控指标数据成功！" % db_list[index])
    except Exception as e:
        logger.info("'%s'获取和写入备份信息指标数据失败！\n错误信息：'%s'" % (db_list[index], str(e)))

#获取数据库归档日志指标数据
def get_archlog_data(db_list,new_workbook):
    try:
        #excel表中获取和写入"数据库备份"监控数据
        logger.info("=======================================================================")
        for index in range(len(db_list)):
            new_sql_7 = sql_7 % (db_list[index],'%')
            obj = DbOper(user=username, pwd=password, host=host, port=port, sid=sid)
            data = obj.dboper(new_sql_7)
            new_sheet = new_workbook.get_sheet(2)
            if db_list[index] == 'xxx':
                msg1 = arch_info['xxx'] + data[0][0]
                new_sheet.write(index + 2, 7, msg1, style)
                logger.info("'%s'获取和写入归档相关监控指标数据成功！" % db_list[index])
            elif db_list[index] == 'xxx':
                msg2 = arch_info['xxx'] + data[0][0]
                new_sheet.write(index + 2, 7, msg2, style)
                logger.info("'%s'获取和写入归档相关监控指标数据成功！" % db_list[index])
            elif db_list[index] == 'xxx':
                msg3 = arch_info['xxx'] + data[0][0]
                new_sheet.write(index + 2, 7, msg3, style)
                logger.info("'%s'获取和写入归档相关监控指标数据成功！" % db_list[index])
            elif db_list[index] == 'xxx':
                msg4 = arch_info['xxx'] + data[0][0]
                new_sheet.write(index + 2, 7, msg4, style)
                logger.info("'%s'获取和写入归档相关监控指标数据成功！" % db_list[index])
            elif db_list[index] == 'xxx':
                msg5 = arch_info['xxx'] + data[0][0]
                new_sheet.write(index + 2, 7, msg5, style)
                logger.info("'%s'获取和写入归档相关监控指标数据成功！" % db_list[index])
    except Exception as e:
        logger.info("'%s'获取和写入归档相关监控指标数据失败！\n错误信息：'%s'" % (db_list[index], str(e)))

#获取数据库性能相关指标数据
def get_db_perform_data(db_list,new_workbook):
    try:
        #excel表中获取和写入"数据库性能"监控数据
        logger.info("=======================================================================")
        new_sheet = new_workbook.get_sheet(2)
        for index in range(len(db_list)):
            new_sql_8 = sql_8 % db_list[index]
            obj = DbOper(user=username, pwd=password, host=host, port=port, sid=sid)
            data = obj.dboper(new_sql_8)
            tmp_list = []
            for idx in range(len(data)):
                string = data[idx][0] + '\n'
                tmp_list.append(string)
            tmp_data = ''.join(tmp_list).strip('\n')
            new_sheet.write(index + 2, 8, tmp_data, style)
            logger.info("'%s'获取和写入数据库性能相关监控指标数据成功！" % db_list[index])
    except Exception as e:
        logger.info("'%s'获取和写入数据库性能相关监控指标数据失败！\n错误信息：'%s'" % (db_list[index], str(e)))

'''获取osw图片写入excel表'''
#远程生成osw文件
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
    ssh.connect(username='xxx',password='xxx',hostname='xxx')
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

#10.114.130.2上压缩osw文件夹
def create_all_osw_zip_file(username,hostname,password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(username=username,password=password,hostname=hostname)
    stdin,stdout,stderr = ssh.exec_command(remote_ls_cmd)
    result_list = stdout.read().decode('utf-8').strip('\n').split('\n')
    start_point = len(result_list) - 4
    end_point = len(result_list)
    out_name = []
    logger.info("=======================================================================")
    for index in range(start_point,end_point):
        row_list = result_list[index].split(' ')
        name = row_list[len(row_list) - 1]
        new_name = remote_os_path + '/' + name
        out_name.append(name)
        new_cmd = remote_tar_cmd % (new_name,new_name)
        new_command = 'source /oracle/home/.bash_profile;' + new_cmd
        stdin, stdout, stderr = ssh.exec_command(new_command)
        time.sleep(5)
        logger.info("'%s'压缩osw文件成功！" % name)
    ssh.close()
    return out_name

#10.114.130.2上下载的指定osw压缩文件到本地
def get_remote_osw_zip_file(host_ip, username, password,out_name):
    t = paramiko.Transport((host_ip, 22))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    logger.info("=======================================================================")
    for index in range(len(out_name)):
        src = remote_os_path + '/' + out_name[index] + '.zip'
        osw_base = base_dir + '\\' + 'osw'
        osw_file_path = base_dir + '\\osw\\' + out_name[index]
        des = osw_file_path + '\\' + out_name[index] + '.zip'
        if not os.path.exists(osw_base):
            os.mkdir(osw_base)
        if not os.path.exists(osw_file_path):
            os.mkdir(osw_file_path)
        sftp.get(src,des)
        logger.info("'%s'压缩文件已经下载！" % out_name[index])
        time.sleep(5)
    t.close()

#解压本地osw压缩文件
def unzip_local_osw_file(ip_list:list):
    osw_path = base_dir + '\\osw'
    if os.path.exists(osw_path):
        osw_name_list = os.listdir(osw_path)
        logger.info("=======================================================================")
        for idx in range(len(ip_list)):
            for index in range(len(osw_name_list)):
                if ip_list[idx].split('.')[-1] in osw_name_list[index].split('_'):
                    zip_list = os.listdir(osw_path + '\\' + osw_name_list[index])
                    zip_file_name = osw_path + '\\' + osw_name_list[index] + '\\' + zip_list[0]
                    os.system(local_unzip_cmd % (zip_file_name,osw_path + '\\' + osw_name_list[index] + '\\'))
                    logger.info("'%s'压缩文件解压完成" % osw_name_list[index])
                    time.sleep(5)
    else:
        logger.info("'%s'存放的osw压缩文件的文件夹不存在，osw压缩文件没有下载成功！" % osw_path)

#osw网页截图功能函数
def osw_snapshot(xml_path_file:str,img_dir:str,ip:str):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="E:\\tools\\lenovo_2.exe")
    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    driver.set_window_size(width + 300, height + 400)
    driver.set_page_load_timeout(300)
    driver.set_script_timeout(300)
    driver.get(xml_path_file)
    driver.find_element_by_link_text('CPU').click()
    time.sleep(5)
    driver.save_screenshot(img_dir + '\\%s_cpu.jpg' % ip.split('.')[-1])
    driver.find_element_by_link_text('MEMORY').click()
    time.sleep(5)
    driver.save_screenshot(img_dir + '\\%s_memory.jpg'% ip.split('.')[-1])
    driver.find_element_by_link_text('I/O').click()
    time.sleep(5)
    driver.save_screenshot(img_dir + '\\%s_io.jpg' % ip.split('.')[-1])
    driver.find_element_by_link_text('NETWORK').click()
    driver.find_element_by_xpath('//a[contains(text(),"Network IP Graphs")]').click()
    time.sleep(5)
    driver.save_screenshot(img_dir + '\\%s_network.jpg' % ip.split('.')[-1])
    driver.close()

#生成osw网页截图
def gen_osw_img(ip_list:list):
    osw_path = base_dir + '\\osw'
    img_dir = base_dir + '\\osw_img'
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    if os.path.exists(osw_path):
        osw_list = os.listdir(osw_path)
        for idx1 in range(len(ip_list)):
            logger.info("=======================================================================")
            for idx2 in range(len(osw_list)):
                if ip_list[idx1].split('.')[-1] == osw_list[idx2].split('_')[3]:
                    xml_path_file = "file:///E:/daily_data/osw/" + osw_list[idx2] + "/oratools/sw/oswbb/analysis/" + \
                               osw_list[idx2] + "/dashboard/index.html"
                    osw_snapshot(xml_path_file,img_dir,ip_list[idx1])
                    logger.info("'%s'的osw截图已经生成！" % ip_list[idx1])
    else:
        logger.info("osw压缩文件没有下载成功，请检查！")

#osw截图写入到excel表
def write_osw_img_to_excel(osw_sheet_list:list,wb):
    logger.info("=======================================================================")
    osw_path = base_dir + '\\osw_img'
    if os.path.exists(osw_path):
        osw_img_list = os.listdir(osw_path)
        if len(osw_img_list) > 0:
            for idx1 in range(len(osw_img_list)):
                for idx2 in range(len(osw_sheet_list)):
                    if osw_img_list[idx1].split('_')[0] == osw_sheet_list[idx2].split('-')[1].split('.')[-1]:
                        if osw_img_list[idx1].split('_')[1].split('.')[0] == 'cpu':
                            sht = wb.sheets[osw_sheet_list[idx2]]
                            value = osw_path + '\\' + osw_img_list[idx1]
                            sht.pictures.add(value, left=sht.range('A2').left, top=sht.range('A2').top, width=500,height=500)
                            logger.info("'%s'表已经成功写入'%s'监控图片！" % (osw_sheet_list[idx2],osw_img_list[idx1]))
                        if osw_img_list[idx1].split('_')[1].split('.')[0] == 'memory':
                            sht = wb.sheets[osw_sheet_list[idx2]]
                            value = osw_path + '\\' + osw_img_list[idx1]
                            sht.pictures.add(value, left=sht.range('A36').left, top=sht.range('A36').top, width=500,height=500)
                            logger.info("'%s'表已经成功写入'%s'监控图片！" % (osw_sheet_list[idx2], osw_img_list[idx1]))
                        if osw_img_list[idx1].split('_')[1].split('.')[0] == 'io':
                            sht = wb.sheets[osw_sheet_list[idx2]]
                            value = osw_path + '\\' + osw_img_list[idx1]
                            sht.pictures.add(value, left=sht.range('A71').left, top=sht.range('A71').top, width=500,height=500)
                            logger.info("'%s'表已经成功写入'%s'监控图片！" % (osw_sheet_list[idx2], osw_img_list[idx1]))
                        if osw_img_list[idx1].split('_')[1].split('.')[0] == 'network':
                            sht = wb.sheets[osw_sheet_list[idx2]]
                            value = osw_path + '\\' + osw_img_list[idx1]
                            sht.pictures.add(value, left=sht.range('A107').left, top=sht.range('A107').top, width=500,height=500)
                            logger.info("'%s'表已经成功写入'%s'监控图片！" % (osw_sheet_list[idx2], osw_img_list[idx1]))
        else:
            logger.info('osw图片没有下载！')
    else:
        logger.info('找不到存放osw图片文件夹！')

'''获取所有数据库os和alert日志写入excel表'''
#获取所有需要下载的日志的名称
def get_all_remote_alertlog_filename(username,hostname,password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(username=username, password=password, hostname=hostname)
    stdin, stdout, stderr = ssh.exec_command('source /oracle/home/.bash_profile;ls %s' % remote_alertlog_path)
    result_list = stdout.read().decode('utf-8').strip('\n').split('\n')
    return result_list

#下载10.114.130.2上alert文件夹所有内容
def get_all_remote_alertlog_file(host_ip, username, password,result_list):
    t = paramiko.Transport((host_ip, 22))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    logger.info("=======================================================================")
    alertlog_path = base_dir + '\\alertlog'
    if not os.path.exists(alertlog_path):
        os.mkdir(alertlog_path)
    for file_name in result_list:
        src = remote_alertlog_path + '/' + file_name
        des = alertlog_path + '\\' + file_name
        sftp.get(src, des)
        logger.info("'%s'日志文件已经下载！" % file_name)
        time.sleep(5)
    t.close()

#写入所有数据库的日志文件到excel表
#写入数据库alert日志到excel表
def write_dblog_to_excel(dblog_sheet_list:list,wb):
    logger.info("=======================================================================")
    db_log_path = base_dir + '\\alertlog'
    if os.path.exists(db_log_path):
        db_log_list = os.listdir(db_log_path)
        if len(db_log_list) > 0:
            for idx1 in range(len(db_log_list)):
                for idx2 in range(len(dblog_sheet_list)):
                    db_log_ip = db_log_list[idx1].split('.')[0]
                    dblog_sheet_ip = dblog_sheet_list[idx2].split('-')[1]
                    if db_log_ip.split('_')[1] == dblog_sheet_ip.split('.')[-1]:
                        if db_log_list[idx1].split('.')[0].split('_')[0] == 'alter':
                            file_name = db_log_path + '\\' + db_log_list[idx1]
                            sh = wb.sheets[dblog_sheet_list[idx2]]
                            with open(file_name, mode='r', encoding='gbk') as fd:
                                current_line = fd.readline()
                                index = 2
                                while current_line:
                                    #sh.range('A' + str(index)).api.Font.Size = 9
                                    sh.range('A' + str(index)).value = current_line
                                    index = index + 1
                                    current_line = fd.readline()
                            logger.info("'%s'表已经成功写入'%s'日志" % (dblog_sheet_list[idx2],db_log_list[idx1]))
        else:
            logger.info('alert告警日志没有下载！')
    else:
        logger.info('找不到存放数据库alertlog日志的文件夹！')

#写入服务器oslog日志到excel表
def write_oslog_to_excel(oslog_sheet_list:list,wb):
    logger.info("=======================================================================")
    os_log_path = base_dir + '\\alertlog'
    if os.path.exists(os_log_path):
        os_log_list = os.listdir(os_log_path)
        if len(os_log_list) > 0:
            for idx1 in range(len(os_log_list)):
                for idx2 in range(len(oslog_sheet_list)):
                    os_log_ip = os_log_list[idx1].split('.')[0]
                    oslog_sheet_ip = oslog_sheet_list[idx2].split('-')[1]
                    if os_log_ip.split('_')[1] == oslog_sheet_ip.split('.')[-1]:
                        if os_log_list[idx1].split('.')[0].split('_')[0] == 'oslog':
                            file_name = os_log_path + '\\' + os_log_list[idx1]
                            sh = wb.sheets[oslog_sheet_list[idx2]]
                            with open(file_name, mode='r', encoding='gbk') as fd:
                                current_line = fd.readline()
                                index = 2
                                while current_line:
                                    #sh.range('A' + str(index)).api.Font.Size = 9
                                    sh.range('A' + str(index)).value = current_line
                                    index = index + 1
                                    current_line = fd.readline()
                            logger.info("'%s'表已经成功写入'%s'日志" % (oslog_sheet_list[idx2],os_log_list[idx1]))
        else:
            logger.info('服务器oslog日志没有下载！')
    else:
        logger.info('找不到存放服务器oslog日志的文件夹！')

'''获取sqlserver监控图片写入excel表'''
#插入sqlserver监控图片到excel
def write_sqlserver_img_to_excel(wb):
    img_path = base_dir + "\\sqlserver_img"
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    logger.info("=======================================================================")
    if os.path.exists(img_path):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="E:\\tools\\lenovo_2.exe")
        width = driver.execute_script("return document.documentElement.scrollWidth")
        height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.set_window_size(width + 700, height + 300)
        driver.set_page_load_timeout(300)
        driver.set_script_timeout(300)
        driver.get(r"http://xxx:xxx@xxx/ReportServer_SQL2012/Pages/ReportViewer.aspx?%2fDBA%2fDBA%e6%80%bb%e4%bd%93%e7%9b%91%e6%8e%a7&rs:Command=Render")
        time.sleep(5)
        Select(driver.find_element_by_id('ReportViewerControl_ctl04_ctl03_ddValue')).select_by_visible_text('8820')
        time.sleep(5)
        driver.find_element_by_id('ReportViewerControl_ctl04_ctl00').click()
        time.sleep(5)
        driver.save_screenshot(img_path + '\\sqlserver.jpg')
        driver.close()
        sht = wb.sheets[r'SQL Server监控']
        value = img_path + '\\sqlserver.jpg'
        sht.pictures.add(value, left=sht.range('A2').left, top=sht.range('A2').top, width=800, height=300)
        logger.info("sqlserver监控图片已经插入到excel表！")
    else:
        os.mkdir(img_path)
        logger.info("查找不到sqlserver存放图片的路径！")

'''检查系统和数据库告警日志'''
class Checklog(object):
    # 日志分类
    @staticmethod
    def logclassify(log_path):
        if os.path.exists(log_path):
            logfile_list = os.listdir(log_path)
            logfile_string = ','.join(logfile_list)
            alterlog_list = regex_alert.findall(logfile_string)
            oslog_list = regex_oslog.findall(logfile_string)
            return alterlog_list,oslog_list
        else:
            logger.info('{0}日志路径不存在\n'.format(LOG_PATH))
            return None

    # 查找数据库日志报错
    @staticmethod
    def dberror(alterlog_list):
        dblog_path_list = []
        for i in range(len(alterlog_list)):
            filename = LOG_PATH + '\\' + alterlog_list[i]
            dblog_path_list.append(filename)

        if len(dblog_path_list) == 0:
            logger.info('找不到数据库告警日志！\n')
            return '找不到数据库告警日志！'

        result = []
        for dbfile in dblog_path_list:
            logger.info('=========================================================================')
            basename = os.path.basename(dbfile)
            dbname = basename.split('.')[0].split('_')[1]
            logger.info('{0}节点数据库告警信息如下：'.format(dbname))
            result.append('{0}节点数据库告警信息如下：\n'.format(dbname))
            with open(file=dbfile,mode='r',encoding='gbk') as f:
                index = 0
                current_line = f.readline()
                while current_line:
                    if regex_db_error.search(current_line):
                        index += 1
                        logger.info(current_line)
                        result.append(current_line)
                    current_line = f.readline()
                if index == 0:
                    logger.info('无告警信息。\n')
                    result.append('无告警信息。\n')
        return result

    # 查找系统日志报错
    @staticmethod
    def oserror(oslog_list):
        oslog_path_list = []
        for i in range(len(oslog_list)):
            filename = LOG_PATH + '\\' + oslog_list[i]
            oslog_path_list.append(filename)

        if len(oslog_path_list) == 0:
            logger.info('找不到系统告警日志！\n')
            return None

        result = []
        for osfile in oslog_path_list:
            logger.info('=========================================================================')
            basename = os.path.basename(osfile)
            osname = basename.split('.')[0].split('_')[1]
            logger.info('{0}节点系统告警信息如下：'.format(osname))
            result.append('{0}节点系统告警信息如下：\n'.format(osname))
            with open(file=osfile, mode='r', encoding='gbk') as f:
                index = 0
                current_line = f.readline()
                while current_line:
                    if regex_os_error.search(current_line):
                        index += 1
                        logger.info(current_line)
                        result.append(current_line)
                    current_line = f.readline()
                if index == 0:
                    logger.info('无告警信息。\n')
                    result.append('无告警信息。\n')
        return result

'''发送周报检查结果'''
class SendMail(object):
    def __init__(self,mail_host,mail_user,mail_pass,sender,receivers):
        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_pass = mail_pass
        self.sender = sender
        self.receivers = receivers

    def sendmail(self):
        message = MIMEMultipart()
        message['From'] = self.sender
        message['To'] = self.receivers[0]
        subject = '每日日报输出日志'
        message['Subject'] = Header(subject,'utf-8')
        message.attach(MIMEText('每日日报已经完成，输出日志详见附件！', 'plain', 'utf-8'))
        att = MIMEText(open('E:\\project\\dbmanage_v4\\common\\libs\\daily\\check.log', 'r',encoding='gbk').read(), 'base64', 'gbk')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="check_{0}.log"'.format(datetime.date.today().strftime('%Y-%m-%d'))
        message.attach(att)
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host, 25)
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()
            # logger.info('每日日报输出日志邮件发送成功！')
        except smtplib.SMTPException as e:
            logger.info('错误信息：%s', e)

def write_oracle_parameter(db_list):
    workbook = xlrd.open_workbook(xls_name, formatting_info=True)
    new_workbook = copy(workbook)
    get_startuptime_data(db_list,new_workbook)
    get_tbs_used_data(db_list,new_workbook)
    get_update_obj_data(db_list,new_workbook)
    get_scheduler_job_data(db_list,new_workbook)
    get_dbbackup_data(db_list,new_workbook)
    get_archlog_data(db_list,new_workbook)
    get_db_perform_data(db_list,new_workbook)
    new_workbook.save(new_xls_name)

def write_osw_img():
    pythoncom.CoInitialize()
    app = xlwings.App(visible=False, add_book=False)
    wb = app.books.open(new_xls_name)
    write_osw_img_to_excel(osw_sheet_list,wb)
    wb.save(new_xls_name)
    wb.close()
    app.quit()
    pythoncom.CoUninitialize()

def write_sqlserver_img():
    pythoncom.CoInitialize()
    app = xlwings.App(visible=False, add_book=False)
    wb = app.books.open(new_xls_name)
    write_sqlserver_img_to_excel(wb)
    wb.save(new_xls_name)
    wb.close()
    app.quit()
    pythoncom.CoUninitialize()

def write_dblog():
    pythoncom.CoInitialize()
    app = xlwings.App(visible=False, add_book=False)
    wb = app.books.open(new_xls_name)
    write_dblog_to_excel(dblog_sheet_list,wb)
    wb.save(new_xls_name)
    wb.close()
    app.quit()
    pythoncom.CoUninitialize()

def write_oslog():
    pythoncom.CoInitialize()
    app = xlwings.App(visible=False, add_book=False)
    wb = app.books.open(new_xls_name)
    write_oslog_to_excel(oslog_sheet_list,wb)
    wb.save(new_xls_name)
    wb.close()
    app.quit()
    pythoncom.CoUninitialize()
