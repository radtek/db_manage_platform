# -*- coding:utf-8 -*-

import configparser
from oper import Oper

class DBInstall(object):
    @staticmethod
    def unzip_db_file(user,pwd,host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbinstall\\setup.conf', encoding='utf-8')
        dbsoft_dir = config.get('db_install','dbsoft_dir')
        name = config.get('db_install','db_zip_file')
        dest_dir = config.get('pre_oracle_oinstall','oracle_home')
        db_file_name = dbsoft_dir + '/' + name
        obj = Oper(user, pwd, host)
        is_file = '''if [[ ! -f "{0}" ]]; then echo 0; else echo 1; fi'''
        is_file_result = obj.command(is_file.format(db_file_name))
        if int(is_file_result.strip().strip('\n')) == 1:
            unzip_cmd = 'unzip {0} -d {1} > /dev/null 2>&1;echo $?'.format(db_file_name,dest_dir)
            unzip_result = obj.command(unzip_cmd)
            if int(unzip_result.strip().strip('\n')) == 0:
                print('{0}文件解压成功！'.format(name))
                obj.command('chown oracle:oinstall -R {0}'.format(dest_dir))
                return True
            else:
                print('{0}文件解压失败！'.format(name))
                return False
        else:
            print('{0}文件不存在！'.format(name))
            return False

    @staticmethod
    def db_software_install(user,pwd,host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbinstall\\setup.conf', encoding='utf-8')
        oracle_base = config.get('pre_oracle_oinstall', 'oracle_base')
        oracle_home = config.get('pre_oracle_oinstall', 'oracle_home')
        root_pwd = config.get('db_install', 'root_pwd')
        dbsoft_dir = config.get('db_install', 'dbsoft_dir')
        db_resp_file = dbsoft_dir + '/' + '19c_db_software_install.rsp'
        response_str = '''
cat > {3} <<EOF
oracle.install.responseFileVersion=/oracle/install/rspfmt_dbinstall_response_schema_v19.0.0 
oracle.install.option=INSTALL_DB_SWONLY 
UNIX_GROUP_NAME=oinstall 
INVENTORY_LOCATION={0}/oraInventory
ORACLE_BASE={1}
ORACLE_HOME={2}
oracle.install.db.InstallEdition=EE 
oracle.install.db.OSDBA_GROUP=dba 
oracle.install.db.OSOPER_GROUP=oper 
oracle.install.db.OSBACKUPDBA_GROUP=backupdba 
oracle.install.db.OSDGDBA_GROUP=dgdba 
oracle.install.db.OSKMDBA_GROUP=kmdba 
oracle.install.db.OSRACDBA_GROUP=racdba 
oracle.install.db.rootconfig.executeRootScript=true 
oracle.install.db.rootconfig.configMethod=ROOT
EOF
echo $?'''.format(oracle_base, oracle_base, oracle_home,db_resp_file)
        obj = Oper(user, pwd, host)
        gen_rsp_result = obj.command(response_str)
        if int(gen_rsp_result.strip().strip('\n')) == 0:
            print('19c_db_software_install.rsp响应文件制作成功！')
            obj.command('chown oracle:oinstall {0}'.format(db_resp_file))
        else:
            print('19c_db_software_install.rsp响应文件制作失败！')
        is_file = '''if [[ ! -f "{0}" ]]; then echo 0; else echo 1; fi'''
        is_file_result = obj.command(is_file.format(db_resp_file))
        if int(is_file_result.strip().strip('\n')) == 1:
            install_cmd = "su - oracle -c 'echo {0} | {1}/runInstaller -silent -force \
                -noconfig -ignorePrereq -responseFile {2}'".format(root_pwd, oracle_home, db_resp_file)
            install_result = obj.command(install_cmd)
            return install_result
        else:
            print('{0}响应文件不存在！'.format(db_resp_file))

    @staticmethod
    def listener_install(user,pwd,host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbinstall\\setup.conf', encoding='utf-8')
        dbsoft_dir = config.get('db_install', 'dbsoft_dir')
        listener_resp_file = dbsoft_dir + '/' + '19c_listener_install.rsp'
        listener_str = """
cat > %s <<EOF
[GENERAL]
RESPONSEFILE_VERSION="19.3"
CREATE_TYPE="CUSTOM"
[oracle.net.ca]
INSTALLED_COMPONENTS={"server","net8","javavm"}
INSTALL_TYPE=""typical""
LISTENER_NUMBER=1
LISTENER_NAMES={"LISTENER"}
LISTENER_PROTOCOLS={"TCP;1521"}
LISTENER_START=""LISTENER""
NAMING_METHODS={"TNSNAMES","ONAMES","HOSTNAME"}
NSN_NUMBER=1
NSN_NAMES={"EXTPROC_CONNECTION_DATA"}
NSN_SERVICE={"PLSExtProc"}
NSN_PROTOCOLS={"TCP;HOSTNAME;1521"}
EOF
echo $?""" % (listener_resp_file)
        obj = Oper(user, pwd, host)
        gen_rsp_result = obj.command(listener_str)
        if int(gen_rsp_result.strip().strip('\n')) == 0:
            print('19c_listener_install.rsp响应文件制作成功！')
            obj.command('chown oracle:oinstall {0}'.format(listener_resp_file))
        else:
            print('19c_listener_install.rsp响应文件制作失败！')
        is_file = '''if [[ ! -f "{0}" ]]; then echo 0; else echo 1; fi'''
        is_file_result = obj.command(is_file.format(listener_resp_file))
        if int(is_file_result.strip().strip('\n')) == 1:
            install_cmd = "su - oracle -c 'netca -silent -responsefile {0}'".format(listener_resp_file)
            install_result = obj.command(install_cmd)
            return install_result
        else:
            print('{0}响应文件不存在！'.format(listener_resp_file))

    @staticmethod
    def db_install(user,pwd,host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbinstall\\setup.conf', encoding='utf-8')
        oracle_sid = config.get('pre_oracle_oinstall', 'oracle_sid')
        sys_passwd = config.get('db_install', 'sys_pwd')
        system_pwd = config.get('db_install', 'system_pwd')
        data_dir = config.get('pre_oracle_oinstall', 'data_dir')
        archive_dir = config.get('pre_oracle_oinstall', 'archive_dir')
        lang = config.get('db_install', 'lang')
        db_total_mem = config.get('db_install', 'db_total_mem')
        db_mem_size = 0
        if db_total_mem.upper().endswith('G'):
            db_mem_size = int(round(float(db_total_mem.strip('G').strip('g')) * 1024))
        if db_total_mem.upper().endswith('M'):
            db_mem_size = int(round(float(db_total_mem.strip('M').strip('m'))))
        template_file = config.get('pre_oracle_oinstall','oracle_home') + '/assistants/dbca/templates/General_Purpose.dbc'
        db_ins_cmd = """
su - oracle -c 'dbca -silent -createDatabase \
-responseFile NO_VALUE \
-gdbName {0} \
-sid {1} \
-characterSet {2} \
-nationalCharacterSet AL16UTF16 \
-sysPassword {3} \
-systemPassword {4} \
-databaseConfigType SINGLE \
-templateName {5} \
-storageType FS \
-datafileDestination {6} \
-recoveryAreaDestination {7}/flash_recovery_area \
-databaseType OLTP \
-createAsContainerDatabase false \
-redoLogFileSize 50 \
-sampleSchema true \
-automaticMemoryManagement false \
-totalMemory {8}'""".format(oracle_sid, oracle_sid, lang, sys_passwd, system_pwd, template_file, data_dir,
                            archive_dir, db_mem_size)
        obj = Oper(user, pwd, host)
        is_file = '''if [[ ! -f "{0}" ]]; then echo 0; else echo 1; fi'''
        is_file_result = obj.command(is_file.format(template_file))
        if int(is_file_result.strip().strip('\n')) == 1:
            install_result = obj.command(db_ins_cmd)
            return install_result
        else:
            print('{0}模板文件不存在！'.format(template_file))
