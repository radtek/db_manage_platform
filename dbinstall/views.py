# -*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse
import os
from common.libs.Helper import ops_renderJSON,ops_renderErrJSON
from common.libs.oracle_install import oracle_install
from common.libs.oracle_install.oper import Oper
import configparser
from common.libs.daily import daily
from common.libs.daily.daily import DbOper
from common.libs.daily.daily import Checklog
from common.libs.daily.daily import SendMail
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
from common.libs.GetData import get_startuptime_data,get_tbs_used_data,get_update_obj_data,get_scheduler_job_data,get_dbbackup_data,get_archlog_data,get_db_perform_data
from common.libs.drawpicture import DataParse
from common.libs.oswatch import gen_sqlserver_img

# 配置信息
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

nr_hugepages = None

# Create your views here.
def dbinstall(request):
    if request.method == 'GET':
        username = request.GET.get('username',None)
        return render(request,'dbinstall/dbinstall.html',context={"username":username})
    if request.method == 'POST':
        global nr_hugepages
        tag = request.POST.get('tag')
        # if tag == 'dbinstall':
        #     cmd_result = os.system('python E:\project\dbmanage_v4\common\libs\dbinstall\install.py')
        #     if cmd_result == 0:
        #         result = ops_renderJSON(msg="操作成功！")
        #         return HttpResponse(result)
        if tag == '1.1-系统版本检查':
            user = request.POST.get('user').strip()
            pwd = request.POST.get('pwd').strip()
            ip = request.POST.get('ip').strip()
            if ip == '' or user == '' or pwd == '':
                result = ops_renderErrJSON(msg='请把输入框填写完整！退出安装！')
                return HttpResponse(result)
            msg = oracle_install.DbInstall.os_release_check(user,pwd,ip)
            result = ops_renderJSON(msg=msg)
            return HttpResponse(result)
        if tag == '1.2-系统内存检查':
            user = request.POST.get('user').strip()
            pwd = request.POST.get('pwd').strip()
            ip = request.POST.get('ip').strip()
            if ip == '' or user == '' or pwd == '':
                result = ops_renderErrJSON(msg='请把输入框填写完整！退出安装！')
                return HttpResponse(result)
            msg = oracle_install.DbInstall.os_memory_check(user,pwd,ip)
            result = ops_renderJSON(msg=msg)
            return HttpResponse(result)
        if tag == '1.3-系统swap检查':
            user = request.POST.get('user').strip()
            pwd = request.POST.get('pwd').strip()
            ip = request.POST.get('ip').strip()
            if ip == '' or user == '' or pwd == '':
                result = ops_renderErrJSON(msg='请把输入框填写完整！退出安装！')
                return HttpResponse(result)
            msg = oracle_install.DbInstall.os_swap_check(user,pwd,ip)
            result = ops_renderJSON(msg=msg)
            return HttpResponse(result)
        if tag == '1.4-安装目录检查':
            user = request.POST.get('user').strip()
            pwd = request.POST.get('pwd').strip()
            ip = request.POST.get('ip').strip()
            if ip == '' or user == '' or pwd == '':
                result = ops_renderErrJSON(msg='请把输入框填写完整！退出安装！')
                return HttpResponse(result)
            msg = oracle_install.DbInstall.oracle_installdir_check(user,pwd,ip)
            result = ops_renderJSON(msg=msg)
            return HttpResponse(result)
        if tag == '2-安装软件上传':
            user = request.POST.get('user').strip()
            pwd = request.POST.get('pwd').strip()
            ip = request.POST.get('ip').strip()
            if ip == '' or user == '' or pwd == '':
                result = ops_renderErrJSON(msg='请把输入框填写完整！退出安装！')
                return HttpResponse(result)
            dbsoft_base_dir = 'E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\dbsoft\\'
            remote_soft_dir = '/dbsoft/'
            dbsoft_file = 'LINUX.X64_193000_db_home.zip'
            opatch_file = 'p6880880_190000_Linux-x86-64.zip'
            patch_file = 'p32545013_190000_Linux-x86-64.zip'
            mkdir_cmd = 'mkdir -p {0};echo $?'.format(remote_soft_dir)
            obj = Oper(user, pwd, ip)
            mkdir_result = obj.command(mkdir_cmd)
            if int(mkdir_result.strip('\n').strip()) == 0:
                print('{0}远程服务器创建目录{1}成功！'.format(ip, remote_soft_dir))
                print('{0}正在上传！'.format(dbsoft_file))
                db_local_file = dbsoft_base_dir + dbsoft_file
                db_remote_file = remote_soft_dir + dbsoft_file
                obj.upload(db_local_file, db_remote_file)
                print('{0}上传成功！'.format(dbsoft_file))
                print('{0}正在上传！'.format(opatch_file))
                opatch_local_file = dbsoft_base_dir + opatch_file
                opatch_remote_file = remote_soft_dir + opatch_file
                obj.upload(opatch_local_file, opatch_remote_file)
                print('{0}上传成功！'.format(opatch_file))
                print('{0}正在上传！'.format(patch_file))
                patch_local_file = dbsoft_base_dir + patch_file
                patch_remote_file = remote_soft_dir + patch_file
                obj.upload(patch_local_file, patch_remote_file)
                print('{0}上传成功！'.format(patch_file))
            else:
                print('{0}远程服务器创建目录{1}失败！'.format(ip, remote_soft_dir))
                result = ops_renderErrJSON(msg='远程服务器创建oracle软件目录失败！')
                return HttpResponse(result)
            result = ops_renderJSON(msg='oracle所有安装软件上传成功！')
            return HttpResponse(result)
        if tag == '3-生成安装配置文件':
            ora_ins_dir = request.POST.get('ora_ins_dir').strip()
            ora_tool_dir = request.POST.get('ora_tool_dir').strip()
            ora_data_dir = request.POST.get('ora_data_dir').strip()
            ora_arch_dir = request.POST.get('ora_arch_dir').strip()
            oracle_base = request.POST.get('oracle_base').strip()
            oracle_home = request.POST.get('oracle_home').strip()
            ora_pwd = request.POST.get('ora_pwd').strip()
            ora_sid = request.POST.get('ora_sid').strip()
            client_lang = request.POST.get('client_lang').strip()
            sga_size = request.POST.get('sga_size').strip()
            ip = request.POST.get('ip').strip()
            host = request.POST.get('host').strip()
            soft_dir = request.POST.get('soft_dir').strip()
            root_pwd = request.POST.get('root_pwd').strip()
            db_soft = request.POST.get('db_soft').strip()
            sys_pwd = request.POST.get('sys_pwd').strip()
            system_pwd = request.POST.get('system_pwd').strip()
            db_mem = request.POST.get('db_mem').strip()
            db_lang = request.POST.get('db_lang').strip()
            opatch_file = request.POST.get('opatch_file').strip()
            opatch = request.POST.get('opatch').strip()
            if ora_ins_dir == '' or ora_tool_dir == '' or ora_data_dir == '' or ora_arch_dir == '' or oracle_base == '' or oracle_home == '' \
                or ora_pwd == '' or ora_sid == '' or client_lang == '' or sga_size == '' or ip == '' or host == '' or soft_dir == '' \
                or root_pwd == '' or db_soft == '' or sys_pwd == '' or system_pwd == '' or db_mem == '' or db_lang == '' or opatch_file == '' or opatch == '':
                result = ops_renderErrJSON(msg='请把输入框填写完整！退出安装！')
                return HttpResponse(result)
            oracle_dir = 'oracle_dir = ' + ora_ins_dir + '\n'
            oracle_tool = 'oracle_tool = ' + ora_tool_dir + '\n'
            data_dir = 'data_dir = ' + ora_data_dir + '\n'
            archive_dir = 'archive_dir = ' + ora_arch_dir + '\n'
            oracle_base = 'oracle_base = ' + oracle_base + '\n'
            oracle_home = 'oracle_home = ' + oracle_home + '\n'
            oracle_pwd = 'oracle_pwd = ' + ora_pwd + '\n'
            oracle_sid = 'oracle_sid = ' + ora_sid + '\n'
            nls_lang = 'nls_lang = ' + client_lang + '\n'
            sga_size = 'sga_size = ' + sga_size + '\n'
            ip = 'ip = ' + ip + '\n'
            hostname = 'hostname = ' + host + '\n'
            dbsoft_dir = 'dbsoft_dir = ' + soft_dir + '\n'
            root_pwd = 'root_pwd = ' + root_pwd + '\n'
            db_zip_file = 'db_zip_file = ' + db_soft + '\n'
            sys_pwd = 'sys_pwd = ' + sys_pwd + '\n'
            system_pwd = 'system_pwd = ' + system_pwd + '\n'
            db_total_mem = 'db_total_mem = ' + db_mem + '\n'
            lang = 'lang = ' + db_lang + '\n'
            opatch_name = 'opatch_name = ' + opatch_file + '\n'
            patch_name = 'patch_name = ' + opatch + '\n'
            config_list = []
            config_list.append('[pre_oracle_oinstall]\n')
            config_list.append(oracle_dir)
            config_list.append(oracle_tool)
            config_list.append(data_dir)
            config_list.append(archive_dir)
            config_list.append(oracle_base)
            config_list.append(oracle_home)
            config_list.append(oracle_pwd)
            config_list.append(oracle_sid)
            config_list.append(nls_lang)
            config_list.append(sga_size)
            config_list.append(ip)
            config_list.append(hostname)
            config_list.append('\n')
            config_list.append('[db_install]\n')
            config_list.append(dbsoft_dir)
            config_list.append(root_pwd)
            config_list.append(db_zip_file)
            config_list.append(sys_pwd)
            config_list.append(system_pwd)
            config_list.append(db_total_mem)
            config_list.append(lang)
            config_list.append('\n')
            config_list.append('[patch_install]\n')
            config_list.append(opatch_name)
            config_list.append(patch_name)
            base_dir = 'E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\'
            config_file = base_dir + 'setup.conf'
            try:
                with open(file=config_file, mode='w', encoding='utf-8') as f:
                    f.writelines(config_list)
            except Exception as e:
                print('配置文件写入失败！')
                print('错误信息：{0}'.format(e))
                result = ops_renderErrJSON(msg='数据库安装配置文件生成失败！')
                return HttpResponse(result)
            result = ops_renderJSON(msg='数据库安装配置文件已经生成！')
            return HttpResponse(result)
        if tag == '4.1-禁用防火墙':
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            msg = oracle_install.DbInstall.stop_firewall('root', sec2['root_pwd'], sec1['ip'])
            result = ops_renderJSON(msg=msg)
            return HttpResponse(result)
        if tag == '4.2-禁用selinux':
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            msg = oracle_install.DbInstall.stop_selinux('root', sec2['root_pwd'], sec1['ip'])
            result = ops_renderJSON(msg=msg)
            return HttpResponse(result)
        if tag == '5-rpm包安装':
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            msg = oracle_install.DbInstall.rpm_install('root', sec2['root_pwd'], sec1['ip'])
            result = ops_renderJSON(msg=msg)
            return HttpResponse(result)
        if tag == '6.1-创建用户和组':
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            msg = oracle_install.DbInstall.user_group_add('root', sec2['root_pwd'], sec1['ip'])
            result = ops_renderJSON(msg=msg)
            return HttpResponse(result)
        if tag == '6.2-创建目录':
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            msg = oracle_install.DbInstall.create_dir('root', sec2['root_pwd'], sec1['ip'])
            result = ops_renderJSON(msg=msg)
            return HttpResponse(result)
        if tag == '7.1-bash_profile配置':
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            msg = oracle_install.DbInstall.modify_oracle_profile('root', sec2['root_pwd'], sec1['ip'])
            result = ops_renderJSON(msg=msg)
            return HttpResponse(result)
        if tag == '7.2-sysctl.conf配置':
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            msg,nr_hugepages = oracle_install.DbInstall.modify_os_parameter_1('root', sec2['root_pwd'], sec1['ip'])
            result = ops_renderJSON(msg=msg)
            return HttpResponse(result)
        if tag == '7.3-limits.conf配置':
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            msg = oracle_install.DbInstall.modify_os_parameter_2('root', sec2['root_pwd'], sec1['ip'])
            result = ops_renderJSON(msg=msg)
            return HttpResponse(result)
        if tag == '7.4-profile配置':
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            msg = oracle_install.DbInstall.modify_profile('root', sec2['root_pwd'], sec1['ip'])
            result = ops_renderJSON(msg=msg)
            return HttpResponse(result)
        if tag == '7.5-hosts配置':
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            msg = oracle_install.DbInstall.modify_host('root', sec2['root_pwd'], sec1['ip'])
            result = ops_renderJSON(msg=msg)
            return HttpResponse(result)
        if tag == '8-关闭透明大页':
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            msg = oracle_install.DbInstall.stop_transparent_hugepage('root', sec2['root_pwd'], sec1['ip'],nr_hugepages)
            result = ops_renderJSON(msg=msg)
            return HttpResponse(result)
        if tag == '9-数据库软件安装':
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            oracle_install.DbInstall.unzip_db_file('root', sec2['root_pwd'], sec1['ip'])
            install_result = oracle_install.DbInstall.db_software_install('root', sec2['root_pwd'], sec1['ip'])
            result = ops_renderJSON(msg=install_result)
            return HttpResponse(result)
        if tag == '10-数据库监听安装':
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            install_result = oracle_install.DbInstall.listener_install('root', sec2['root_pwd'], sec1['ip'])
            result = ops_renderJSON(msg=install_result)
            return HttpResponse(result)
        if tag == '11-数据库安装':
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            install_result = oracle_install.DbInstall.db_install('root', sec2['root_pwd'], sec1['ip'])
            result = ops_renderJSON(msg=install_result)
            return HttpResponse(result)
        if tag == '12-补丁安装':
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            install_result = oracle_install.DbInstall.patch_install('root', sec2['root_pwd'], sec1['ip'])
            result = ops_renderJSON(msg=install_result)
            return HttpResponse(result)
        if tag == '1-获取alert和os日志':
            result_list = daily.get_all_remote_alertlog_filename(username='xxx', password='xxx', hostname='xxx')
            daily.get_all_remote_alertlog_file(host_ip='xxx', username='xxx', password='xxx',result_list=result_list)
            result = ops_renderJSON(msg='alert和os日志下载完成！')
            return HttpResponse(result)
        if tag == '2.1-远程生成osw文件':
            for i in ip_list:
                daily.gen_osw_file(i)
                logger.info('{0}节点oswatch文件已经生成！'.format(i))
            result = ops_renderJSON(msg='远程已经生成osw文件！')
            return HttpResponse(result)
        if tag == '2.2-远程压缩获取osw文件':
            out_name = daily.create_all_osw_zip_file(username='xxx', password='xxx', hostname='xxx')
            daily.get_remote_osw_zip_file(host_ip='xxx', username='xxx', password='xxx', out_name=out_name)
            result = ops_renderJSON(msg='远程压缩获取osw文件成功！')
            return HttpResponse(result)
        if tag == '2.3-本地解压osw文件':
            daily.unzip_local_osw_file(ip_list)
            result = ops_renderJSON(msg='本地解压osw文件成功！')
            return HttpResponse(result)
        if tag == '2.4-生成osw截图':
            daily.gen_osw_img(ip_list)
            result = ops_renderJSON(msg='本地生成osw截图成功！')
            return HttpResponse(result)
        if tag == '3-oracle监控指标获取并写入excel表':
            db_list = list(db_info)
            daily.write_oracle_parameter(db_list)
            result = ops_renderJSON(msg='oracle监控指标获取并写入excel表成功！')
            return HttpResponse(result)
        if tag == '4-osw图片写入到excel表':
            daily.write_osw_img()
            result = ops_renderJSON(msg='osw图片写入到excel表成功！')
            return HttpResponse(result)
        if tag == '5-sqlserver图片写入到excel表':
            daily.write_sqlserver_img()
            result = ops_renderJSON(msg='sqlserver图片写入到excel表成功！')
            return HttpResponse(result)
        if tag == '6-alert日志写入到excel表':
            daily.write_dblog()
            result = ops_renderJSON(msg='alert日志写入到excel表成功！')
            return HttpResponse(result)
        if tag == '7-os日志写入到excel表':
            daily.write_oslog()
            result = ops_renderJSON(msg='os日志写入到excel表成功！')
            return HttpResponse(result)
        if tag == '8-alert日志错误检查':
            alterlog_list, _ = Checklog.logclassify(LOG_PATH)
            resu = Checklog.dberror(alterlog_list)
            msg = ''.join(resu)
            result = ops_renderJSON(msg=msg)
            return HttpResponse(result)
        if tag == '9-os日志错误检查':
            _, oslog_list = Checklog.logclassify(LOG_PATH)
            resu = Checklog.oserror(oslog_list)
            msg = ''.join(resu)
            result = ops_renderJSON(msg=msg)
            return HttpResponse(result)
        if tag == '10-发送日报日志':
            mail = SendMail(mail_host, mail_user, mail_pass, sender, receivers)
            mail.sendmail()
            result = ops_renderJSON(msg='发送日报日志成功！')
            return HttpResponse(result)
        if tag == '实例启动时间':
            ip = request.POST.get('ip',None)
            tm = request.POST.get('tm',None)
            result = get_startuptime_data(ip.strip(), tm.strip())
            new_result = []
            for index in range(len(result)):
                temp_list = list(result[index])
                new_result.append(temp_list)
            for index in range(len(new_result)):
                new_result[index][-1] = str(new_result[index][-1])
                new_result[index][-2] = str(new_result[index][-2])
            result = ops_renderJSON(data=new_result)
            return HttpResponse(result)
        if tag == '表空间检查':
            ip = request.POST.get('ip', None)
            tm = request.POST.get('tm', None)
            result = get_tbs_used_data(ip.strip(), tm.strip())
            new_result = []
            for index in range(len(result)):
                temp_list = list(result[index])
                new_result.append(temp_list)
            for index in range(len(new_result)):
                new_result[index][-1] = str(new_result[index][-1])
            result = ops_renderJSON(data=new_result)
            return HttpResponse(result)
        if tag == '更新对象检查':
            ip = request.POST.get('ip', None)
            tm = request.POST.get('tm', None)
            result = get_update_obj_data(ip.strip(), tm.strip())
            new_result = []
            for index in range(len(result)):
                temp_list = list(result[index])
                new_result.append(temp_list)
            for index in range(len(new_result)):
                new_result[index][-1] = str(new_result[index][-1])
            result = ops_renderJSON(data=new_result)
            return HttpResponse(result)
        if tag == '作业调度检查':
            ip = request.POST.get('ip', None)
            tm = request.POST.get('tm', None)
            result = get_scheduler_job_data(ip.strip(), tm.strip())
            new_result = []
            for index in range(len(result)):
                temp_list = list(result[index])
                new_result.append(temp_list)
            for index in range(len(new_result)):
                new_result[index][1] = str(new_result[index][1])
                new_result[index][-1] = str(new_result[index][-1])
            result = ops_renderJSON(data=new_result)
            return HttpResponse(result)
        if tag == '备份检查':
            ip = request.POST.get('ip', None)
            tm = request.POST.get('tm', None)
            result = get_dbbackup_data(ip.strip(), tm.strip())
            new_result = []
            for index in range(len(result)):
                temp_list = list(result[index])
                new_result.append(temp_list)
            for index in range(len(new_result)):
                new_result[index][1] = str(new_result[index][1])
            result = ops_renderJSON(data=new_result)
            return HttpResponse(result)
        if tag == '归档检查':
            ip = request.POST.get('ip', None)
            tm = request.POST.get('tm', None)
            result = get_archlog_data(ip.strip(), tm.strip())
            new_result = []
            for index in range(len(result)):
                temp_list = list(result[index])
                new_result.append(temp_list)
            for index in range(len(new_result)):
                new_result[index][-1] = str(new_result[index][-1])
            result = ops_renderJSON(data=new_result)
            return HttpResponse(result)
        if tag == '性能检查':
            ip = request.POST.get('ip', None)
            tm = request.POST.get('tm', None)
            result = get_db_perform_data(ip.strip(), tm.strip())
            new_result = []
            for index in range(len(result)):
                temp_list = list(result[index])
                new_result.append(temp_list)
            for index in range(len(new_result)):
                new_result[index][-1] = str(new_result[index][-1])
            result = ops_renderJSON(data=new_result)
            return HttpResponse(result)
        if tag == '表空间报表':
            ip = request.POST.get('ip', None)
            tm = request.POST.get('tm', None)
            tbs = request.POST.get('tbs', None)
            DataParse.tbs_parse(ip, tbs, tm)
            result = ops_renderJSON(msg='表空间报表已生成！')
            return HttpResponse(result)
        if tag == 'aas报表':
            ip = request.POST.get('ip', None)
            tm = request.POST.get('tm', None)
            DataParse.aas_parse(ip, tm)
            result = ops_renderJSON(msg='aas报表已生成！')
            return HttpResponse(result)
        if tag == 'sqlserver巡检':
            gen_sqlserver_img()
            result = ops_renderJSON(msg='sqlserver巡检图片已生成！')
            return HttpResponse(result)
        # if tag == 'dbcheck':
        #     cmd_result = os.system('python E:\project\dbmanage_v4\common\libs\dbcheck\dbcheck.py')
        #     if cmd_result == 0:
        #         result = ops_renderJSON(msg="操作成功！")
        #         return HttpResponse(result)
        # if tag == 'daily':
        #     cmd_result = os.system('python E:\project\dbmanage_v4\common\libs\daily\daily.py')
        #     if cmd_result == 0:
        #         result = ops_renderJSON(msg="操作成功！")
        #         return HttpResponse(result)
        result = ops_renderErrJSON(msg="操作失败！")
        return HttpResponse(result)
