# -*- coding:utf-8 -*-

import configparser
from oper import Oper

class PatchInstall(object):
    @staticmethod
    def patch_install(user,pwd,host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbinstall\\setup.conf', encoding='utf-8')
        dbsoft_dir = config.get('db_install','dbsoft_dir')
        opatch_name = config.get('patch_install','opatch_name')
        patch_name = config.get('patch_install','patch_name')
        oracle_home = config.get('pre_oracle_oinstall','oracle_home')
        opatch_file = dbsoft_dir + '/' + opatch_name
        patch_file = dbsoft_dir + '/' + patch_name
        obj = Oper(user, pwd, host)
        is_file = '''if [[ ! -f "{0}" ]]; then echo 0; else echo 1; fi'''
        is_file_result = obj.command(is_file.format(opatch_file))
        if int(is_file_result.strip().strip('\n')) == 1:
            unzip_opatch_result = obj.command('unzip {0} -d {1}> /dev/null 2>&1;echo $?'.format(opatch_file,dbsoft_dir))
            if int(unzip_opatch_result.strip().strip('\n')) == 0:
                print('{0}解压成功！'.format(opatch_file))
            else:
                print('{0}解压失败！'.format(opatch_file))
        else:
            print('{0}文件不存在！'.format(opatch_file))
        is_dir = '''if [[ ! -d "{0}" ]]; then echo 0; else echo 1; fi'''
        is_dir_result = obj.command(is_dir.format(dbsoft_dir + '/OPatch'))
        if int(is_dir_result.strip().strip('\n')) == 1:
            obj.command('chown oracle:oinstall -R {0}'.format(dbsoft_dir + '/OPatch'))
            obj.command('mv {0}/OPatch {1}/OPatch.bak'.format(oracle_home,oracle_home))
            obj.command('mv {0} {1}/'.format(dbsoft_dir + '/OPatch',oracle_home))
            print('OPatch目录替换成功！')
        else:
            print('{0}目录不存在！'.format(dbsoft_dir + '/OPatch'))
        is_file_result = obj.command(is_file.format(patch_file))
        if int(is_file_result.strip().strip('\n')) == 1:
            unzip_patch_result = obj.command('unzip {0} -d {1}> /dev/null 2>&1;echo $?'.format(patch_file,dbsoft_dir))
            if int(unzip_patch_result.strip().strip('\n')) == 0:
                print('{0}解压成功！'.format(patch_file))
            else:
                print('{0}解压失败！'.format(patch_file))
        else:
            print('{0}文件不存在！'.format(patch_file))
        name = patch_name.split('_')[0].strip('p')
        is_dir_result = obj.command(is_dir.format(dbsoft_dir + '/' + name))
        if int(is_dir_result.strip().strip('\n')) == 1:
            obj.command('chown oracle:oinstall -R {0}'.format(dbsoft_dir + '/' + name))
            obj.command("su - oracle -c 'lsnrctl stop'")
            print('监听停止成功！')
            db_shut_cmd ="""
su - oracle -c 'sqlplus -S / as sysdba << EOF
shutdown immediate
exit
EOF'"""
            obj.command(db_shut_cmd)
            print('数据库关闭成功！')
            install_result = obj.command("su - oracle -c 'cd {0};opatch apply -silent'".format(dbsoft_dir + '/' + name))
            print('数据库安装补丁成功！')
            obj.command("su - oracle -c 'lsnrctl start'")
            print('监听开启成功！')
            db_start_cmd ="""
su - oracle -c 'sqlplus -S / as sysdba << EOF
startup
exit
EOF'"""
            obj.command(db_start_cmd)
            print('数据库开启成功！')
            return install_result
        else:
            print('{0}补丁文件不存在！'.format(dbsoft_dir + '/' + name))

    @staticmethod
    def patch_registry(user, pwd, host):
        obj = Oper(user, pwd, host)
        result = obj.command("su - oracle -c 'datapatch -verbose'")
        return result
