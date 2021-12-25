# -*- coding:utf-8 -*-

from oper import Oper
import datetime
import configparser

class PreOracleInstall(object):
    @staticmethod
    def stop_firewall(user,pwd,host):
        stop_firewall_cmd = 'systemctl stop firewalld.service > /dev/null 2>&1;echo $?'
        disable_firewall_cmd = 'systemctl disable firewalld.service > /dev/null 2>&1;echo $?'
        obj = Oper(user, pwd, host)
        stop_result = obj.command(stop_firewall_cmd)
        disable_result = obj.command(disable_firewall_cmd)
        if int(stop_result.strip().strip('\n')) == 0 and int(disable_result.strip().strip('\n')) == 0:
            print('系统防火墙关闭和禁用成功！')
            return True
        else:
            print('系统防火墙关闭和禁用失败！')
            return False

    @staticmethod
    def stop_selinux(user,pwd,host):
        selinux_conf_file = '/etc/selinux/config'
        obj = Oper(user, pwd, host)
        cp_result = obj.command('cp {0} {1}.bak{2};echo $?'.format(selinux_conf_file, selinux_conf_file,
                                                datetime.datetime.today().strftime('%Y%m%d%H%M%S')))
        if int(cp_result.strip().strip('\n')) == 0:
            print('{0}文件拷贝成功！'.format(selinux_conf_file))
        else:
            print('{0}文件拷贝失败！'.format(selinux_conf_file))
        modify_result = obj.command("sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' {0};echo $?".format(selinux_conf_file))
        if int(modify_result.strip().strip('\n')) == 0:
            print('{0}文件修改成功！'.format(selinux_conf_file))
        else:
            print('{0}文件修改失败！'.format(selinux_conf_file))
        set_result = obj.command('setenforce 0;echo $?')
        if int(set_result.strip().strip('\n')) == 0:
            print('setenforce 0命令执行成功！')
        else:
            print('setenforce 0命令执行失败！')
        if int(cp_result.strip().strip('\n')) == 0 and \
                int(modify_result.strip().strip('\n')) == 0 and \
                int(set_result.strip().strip('\n')) == 0:
            return True
        else:
            return False

    @staticmethod
    def rpm_install(user,pwd,host):
        yum_cmd_1 = 'yum clean all > /dev/null 2>&1;echo $?'
        yum_cmd_2 = 'yum list all > /dev/null 2>&1;echo $?'
        yum_cmd_3 = '''
yum -y install \
bc* \
binutils* \
compat-libcap1* \
compat-libstdc++-33* \
elfutils-libelf* \
elfutils-libelf-devel* \
fontconfig-devel* \
glibc* \
glibc-devel* \
ksh* \
libaio* \
libaio-devel* \
libXrender* \
libXrender-devel* \
libX11* \
libXau* \
libXi* \
libXtst* \
libgcc* \
libstdc++* \
libstdc++-devel* \
libxcb* \
make* \
policycoreutils* \
policycoreutils-python* \
smartmontools* \
sysstat* \
ipmiutil* \
net-tools* \
libvirt-libs* \
nfs-utils* \
python* \
python-configshell* \
python-rtslib* \
python-six* \
targetcli* \
binutils-devel.i686 \
binutils-devel.x86_64 \
compat-libstdc++-296.i686 \
compat-libstdc++-33.i686 \
compat-libstdc++-33.x86_64 \
elfutils-libelf.i686 \
elfutils-libelf-devel.i686 \
elfutils-libelf-devel.x86_64 \
glibc.i686 glibc-devel.i686 \
glibc-utils.x86_64 \
gcc.x86_64 \
gcc-c++.x86_64 \
gcc-gfortran.x86_64 \
gcc-gnat.x86_64 \
gcc-java.x86_64 \
gcc-objc.x86_64 \
gcc-objc++.x86_64 \
libaio-devel.i686 \
libaio-devel.x86_64 \
libaio.i686 \
libgcc.i686 \
libstdc++.i686 \
libstdc++-devel.i686 \
libstdc++-devel.x86_64 \
libstdc++-docs.x86_64 \
makebootfat.x86_64 \
unixODBC.i686 \
unixODBC.x86_64 \
unixODBC-devel.i686 \
unixODBC-devel.x86_64 \
compat-libcap1.i686 \
compat-libcap1.x86_64 \
perl-Env* \
numactl-devel* > /dev/null 2>&1;echo $?
'''
        obj = Oper(user, pwd, host)
        yum_clean_result = obj.command(yum_cmd_1)
        if int(yum_clean_result.strip().strip('\n')) == 0:
            print('yum缓存清理成功！')
        else:
            print('yum缓存清理失败！')
        yum_list_result = obj.command(yum_cmd_2)
        if int(yum_list_result.strip().strip('\n')) == 0:
            print('yum源查看成功！')
        else:
            print('yum源查看失败！')
        rpm_install_result = obj.command(yum_cmd_3)
        if int(rpm_install_result.strip().strip('\n')) == 0:
            print('yum包安装成功！')
        else:
            print('yum包安装失败！')
        if int(yum_clean_result.strip().strip('\n')) == 0 and \
                int(yum_list_result.strip().strip('\n')) == 0 and \
                int(rpm_install_result.strip().strip('\n')) == 0:
            print('yum所有操作成功！')
            return True
        else:
            print('yum操作失败，请检查yum源！')
            return False

    @staticmethod
    def user_group_add(user,pwd,host):
        is_group = "egrep '^{0}' /etc/group > /dev/null 2>&1;echo $?"
        is_user = "egrep '^{0}' /etc/passwd > /dev/null 2>&1;echo $?"
        oinstall_cmd = '/usr/sbin/groupadd -g 54321 oinstall;echo $?'
        asmdba_cmd = '/usr/sbin/groupadd -g 54327 asmdba;echo $?'
        asmoper_cmd = '/usr/sbin/groupadd -g 54328 asmoper;echo $?'
        dba_cmd = '/usr/sbin/groupadd -g 54322 dba;echo $?'
        oper_cmd = '/usr/sbin/groupadd -g 54323 oper;echo $?'
        backupdba_cmd = '/usr/sbin/groupadd -g 54324 backupdba;echo $?'
        dgdba_cmd = '/usr/sbin/groupadd -g 54325 dgdba;echo $?'
        kmdba_cmd = '/usr/sbin/groupadd -g 54326 kmdba;echo $?'
        racdba_cmd = '/usr/sbin/groupadd -g 54330 racdba;echo $?'
        oracle_cmd = '/usr/sbin/useradd -u 54321 -g oinstall -G dba,asmdba,backupdba,dgdba,kmdba,racdba,oper oracle;echo $?'
        oracle_pwd_cmd = '''echo "{0}" | passwd --stdin oracle > /dev/null 2>&1;echo $?'''
        obj = Oper(user, pwd, host)
        oinstall_result = obj.command(is_group.format('oinstall'))
        if int(oinstall_result.strip().strip('\n')) == 0:
            print('oinstall组已经存在！')
        else:
            obj.command(oinstall_cmd)
            print('oinstall组创建成功！')
        asmdba_result = obj.command(is_group.format('asmdba'))
        if int(asmdba_result.strip().strip('\n')) == 0:
            print('asmdba组已经存在！')
        else:
            obj.command(asmdba_cmd)
            print('asmdba组创建成功！')
        asmoper_result = obj.command(is_group.format('asmoper'))
        if int(asmoper_result.strip().strip('\n')) == 0:
            print('asmoper组已经存在！')
        else:
            obj.command(asmoper_cmd)
            print('asmoper组创建成功！')
        dba_result = obj.command(is_group.format('dba'))
        if int(dba_result.strip().strip('\n')) == 0:
            print('dba组已经存在！')
        else:
            obj.command(dba_cmd)
            print('dba组创建成功！')
        oper_result = obj.command(is_group.format('oper'))
        if int(oper_result.strip().strip('\n')) == 0:
            print('oper组已经存在！')
        else:
            obj.command(oper_cmd)
            print('oper组创建成功！')
        backupdba_result = obj.command(is_group.format('backupdba'))
        if int(backupdba_result.strip().strip('\n')) == 0:
            print('backupdba组已经存在！')
        else:
            obj.command(backupdba_cmd)
            print('backupdba组创建成功！')
        dgdba_result = obj.command(is_group.format('dgdba'))
        if int(dgdba_result.strip().strip('\n')) == 0:
            print('dgdba组已经存在！')
        else:
            obj.command(dgdba_cmd)
            print('dgdba组创建成功！')
        kmdba_result = obj.command(is_group.format('kmdba'))
        if int(kmdba_result.strip().strip('\n')) == 0:
            print('kmdba组已经存在！')
        else:
            obj.command(kmdba_cmd)
            print('kmdba组创建成功！')
        racdba_result = obj.command(is_group.format('racdba'))
        if int(racdba_result.strip().strip('\n')) == 0:
            print('racdba组已经存在！')
        else:
            obj.command(racdba_cmd)
            print('racdba组创建成功！')
        oracle_result = obj.command(is_user.format('oracle'))
        if int(oracle_result.strip().strip('\n')) == 0:
            print('oracle用户已经存在！')
        else:
            obj.command(oracle_cmd)
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbinstall\\setup.conf', encoding='utf-8')
            oracle_pwd = config.get('pre_oracle_oinstall', 'oracle_pwd')
            obj.command(oracle_pwd_cmd.format(oracle_pwd))
            print('oracle用户创建和设置密码成功！')
        if int(oinstall_result.strip().strip('\n')) != 0 and \
                int(asmdba_result.strip().strip('\n')) != 0 and \
                int(asmoper_result.strip().strip('\n')) != 0 and \
                int(dba_result.strip().strip('\n')) !=0 and \
                int(oper_result.strip().strip('\n')) != 0 and \
                int(backupdba_result.strip().strip('\n')) != 0 and \
                int(dgdba_result.strip().strip('\n')) != 0 and \
                int(kmdba_result.strip().strip('\n')) != 0 and \
                int(racdba_result.strip().strip('\n')) !=0 and \
                int(oracle_result.strip().strip('\n')) != 0:
            return True
        else:
            return False

    @staticmethod
    def create_dir(user,pwd,host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbinstall\\setup.conf', encoding='utf-8')
        oracle_dir = config.get('pre_oracle_oinstall', 'oracle_dir')
        oracle_tool = config.get('pre_oracle_oinstall', 'oracle_tool')
        data_dir = config.get('pre_oracle_oinstall', 'data_dir')
        archive_dir = config.get('pre_oracle_oinstall', 'archive_dir')
        oracle_base = config.get('pre_oracle_oinstall', 'oracle_base')
        oracle_home = config.get('pre_oracle_oinstall', 'oracle_home')
        is_dir = '''if [[ ! -d "{0}" ]]; then echo 0; else echo 1; fi'''
        obj = Oper(user, pwd, host)
        oracle_dir_result = obj.command(is_dir.format(oracle_dir))
        if int(oracle_dir_result.strip().strip('\n')) == 0:
            obj.command('mkdir -p {0}'.format(oracle_dir))
            print('目录{0}创建成功！'.format(oracle_dir))
        else:
            print('目录{0}已经存在！'.format(oracle_dir))
        oracle_tool_result = obj.command(is_dir.format(oracle_tool))
        if int(oracle_tool_result.strip().strip('\n')) == 0:
            obj.command('mkdir -p {0}'.format(oracle_tool))
            print('目录{0}创建成功！'.format(oracle_tool))
        else:
            print('目录{0}已经存在！'.format(oracle_tool))
        data_dir_result = obj.command(is_dir.format(data_dir))
        if int(data_dir_result.strip().strip('\n')) == 0:
            obj.command('mkdir -p {0}'.format(data_dir))
            print('目录{0}创建成功！'.format(data_dir))
        else:
            print('目录{0}已经存在！'.format(data_dir))
        archive_dir_result = obj.command(is_dir.format(archive_dir))
        if int(archive_dir_result.strip().strip('\n')) == 0:
            obj.command('mkdir -p {0}'.format(archive_dir))
            print('目录{0}创建成功！'.format(archive_dir))
        else:
            print('目录{0}已经存在！'.format(archive_dir))
        oracle_base_result = obj.command(is_dir.format(oracle_base))
        if int(oracle_base_result.strip().strip('\n')) == 0:
            obj.command('mkdir -p {0}'.format(oracle_base))
            print('目录{0}创建成功！'.format(oracle_base))
        else:
            print('目录{0}已经存在！'.format(oracle_base))
        oracle_home_result = obj.command(is_dir.format(oracle_home))
        if int(oracle_home_result.strip().strip('\n')) == 0:
            obj.command('mkdir -p {0}'.format(oracle_home))
            print('目录{0}创建成功！'.format(oracle_home))
        else:
            print('目录{0}已经存在！'.format(oracle_home))
        obj.command('chown -R oracle:oinstall {0}'.format(oracle_dir))
        obj.command('chmod -R 755 {0}'.format(oracle_dir))
        print('目录{0}赋权成功！'.format(oracle_dir))
        obj.command('chown -R oracle:oinstall {0}'.format(oracle_tool))
        obj.command('chmod -R 755 {0}'.format(oracle_tool))
        print('目录{0}赋权成功！'.format(oracle_tool))
        obj.command('chown -R oracle:oinstall {0}'.format(data_dir))
        obj.command('chmod -R 755 {0}'.format(data_dir))
        print('目录{0}赋权成功！'.format(data_dir))
        obj.command('chown -R oracle:oinstall {0}'.format(archive_dir))
        obj.command('chmod -R 755 {0}'.format(archive_dir))
        print('目录{0}赋权成功！'.format(archive_dir))
        if int(oracle_dir_result.strip().strip('\n')) == 0 and \
                int(oracle_tool_result.strip().strip('\n')) == 0 and \
                int(data_dir_result.strip().strip('\n')) == 0 and \
                int(archive_dir_result.strip().strip('\n')) == 0 and \
                int(oracle_base_result.strip().strip('\n')) == 0 and \
                int(oracle_home_result.strip().strip('\n')) == 0:
            return True
        else:
            return False

    @staticmethod
    def modify_oracle_profile(user,pwd,host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbinstall\\setup.conf', encoding='utf-8')
        oracle_sid = config.get('pre_oracle_oinstall', 'oracle_sid')
        oracle_base = config.get('pre_oracle_oinstall', 'oracle_base')
        oracle_home = config.get('pre_oracle_oinstall', 'oracle_home')
        nls_lang = config.get('pre_oracle_oinstall', 'nls_lang')
        oracle_bash_profile = '/home/oracle/.bash_profile'
        oracle_profile_config = '''
cat >> {4} <<EOF
umask 022
export ORACLE_SID={0}
export ORACLE_BASE={1}
export ORACLE_HOME={2}
export NLS_LANG="{3}"
export LD_LIBRARY_PATH=\$ORACLE_HOME/lib:\$ORACLE_HOME/network/lib:/lib:/usr/lib:/usr/local/lib
export LIBPATH=\$ORACLE_HOME/lib:\$ORACLE_HOME/network/lib:/lib:/usr/lib:/usr/local/lib
export PATH=\$PATH:/sbin:/usr/lbin:/usr/sbin:\$JAVA_HOME/bin:\$ORACLE_HOME/bin:\$ORACLE_HOME/lib:\$HOME/bin:\$ORACLE_HOME/OPatch:.
export PS1='\$LOGNAME@'`hostname`:'\$PWD''\$ '
if [ -t 0 ]; then
    stty intr ^C
fi
stty erase ^H
set -o vi
EOF
echo $?'''.format(oracle_sid, oracle_base, oracle_home, nls_lang,oracle_bash_profile)
        obj = Oper(user, pwd, host)
        is_file = '''if [[ ! -f "{0}" ]]; then echo 0; else echo 1; fi'''
        is_file_result = obj.command(is_file.format(oracle_bash_profile))
        if int(is_file_result.strip().strip('\n')) == 1:
            cp_result = obj.command('cp {0} {1}.bak{2};echo $?'.format(oracle_bash_profile, oracle_bash_profile,
                                                             datetime.datetime.today().strftime('%Y%m%d%H%M%S')))
            if int(cp_result.strip().strip('\n')) == 0:
                print('{0}文件备份成功！'.format(oracle_bash_profile))
                modify_result = obj.command(oracle_profile_config)
                if int(modify_result.strip().strip('\n')) == 0:
                    print('{0}文件修改成功！'.format(oracle_bash_profile))
                    return True
                else:
                    print('{0}文件修改失败！'.format(oracle_bash_profile))
                    return False
            else:
                print('{0}文件备份失败！'.format(oracle_bash_profile))
                return False
        else:
            print('oracle用户的{0}文件不存在，cp备份该文件失败！'.format(oracle_bash_profile))
            return False

    @staticmethod
    def modify_os_parameter_1(user,pwd,host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbinstall\\setup.conf', encoding='utf-8')
        get_mem_cmd = "free -b | awk '/Mem/ {print $2}'"
        get_page_cmd = "getconf PAGE_SIZE"
        get_huge_page_cmd = "cat /proc/meminfo | grep '^Hugepagesize' | awk '{print $2'}"
        sga = config.get('pre_oracle_oinstall', 'sga_size')
        obj = Oper(user, pwd, host)
        mem = obj.command(get_mem_cmd).strip().strip('\n')
        page = obj.command(get_page_cmd).strip().strip('\n')
        huge_page = obj.command(get_huge_page_cmd).strip().strip('\n')
        shmall = int(mem) * 0.75 / int(page) + 1
        shmmax = shmall * int(page)
        nr_hugepages = 0
        if sga.upper().endswith('G'):
            sga_size = float(sga.strip('G').strip('g'))
            nr_hugepages = sga_size * 1024 * 1024 / int(huge_page)
        if sga.upper().endswith('M'):
            sga_size = float(sga.strip('M').strip('m'))
            nr_hugepages = sga_size * 1024 / int(huge_page)
        sysctl_file = '/etc/sysctl.conf'
        sysctl_config = '''
cat >> {3} <<EOF
#adjust for ORACLE
kernel.shmall = {0}
kernel.shmmax = {1}
fs.file-max = 6815744
kernel.shmmni = 4096
kernel.sem = 250 32000 100 128
kernel.panic_on_oops = 1
fs.aio-max-nr = 1048576
net.ipv4.ip_local_port_range = 9000 65500
net.core.rmem_default = 262144
net.core.rmem_max = 4194304
net.core.wmem_default = 262144
net.core.wmem_max = 1048576
vm.swappiness = 0
vm.dirty_background_ratio = 3
vm.dirty_ratio = 80
vm.dirty_expire_centisecs = 500
vm.dirty_writeback_centisecs = 100

#add for hugepage
vm.nr_hugepages = {2}
vm.hugetlb_shm_group = 54321
EOF
echo $?'''.format(str(int(round(shmall))), str(int(round(shmmax))),str(int(round(nr_hugepages))),sysctl_file)
        is_file = '''if [[ ! -f "{0}" ]]; then echo 0; else echo 1; fi'''
        is_file_result = obj.command(is_file.format(sysctl_file))
        if int(is_file_result.strip().strip('\n')) == 1:
            cp_result = obj.command('cp {0} {1}.bak{2};echo $?'.format(sysctl_file, sysctl_file,
                                                             datetime.datetime.today().strftime('%Y%m%d%H%M%S')))
            if int(cp_result.strip().strip('\n')) == 0:
                print('{0}文件备份成功！'.format(sysctl_file))
                modify_result = obj.command(sysctl_config)
                if int(modify_result.strip().strip('\n')) == 0:
                    print('{0}文件修改成功！'.format(sysctl_file))
                    obj.command('sysctl -p >& /devnull')
                    return True,str(int(round(nr_hugepages)))
                else:
                    print('{0}文件修改失败！'.format(sysctl_file))
                    return False
            else:
                print('{0}文件备份失败！'.format(sysctl_file))
                return False
        else:
            print('{0}文件不存在，cp备份该文件失败！'.format(sysctl_file))
            return False

    @staticmethod
    def modify_os_parameter_2(user,pwd,host):
        config = configparser.ConfigParser()
        config.read('D\\project\\dbmanage_v4\\common\\libs\\dbinstall\\setup.conf', encoding='utf-8')
        sga = config.get('pre_oracle_oinstall', 'sga_size')
        memlock = 0
        limit_conf_file = '/etc/security/limits.conf'
        if sga.upper().endswith('G'):
            sga_size = float(sga.strip('G').strip('g'))
            memlock = sga_size * 1024 * 1024
        if sga.upper().endswith('M'):
            sga_size = float(sga.strip('M').strip('m'))
            memlock = sga_size * 1024
        limit_conf = '''
cat >> {2} <<EOF
oracle soft nproc 2047
oracle hard nproc 16384
oracle soft nofile 1024
oracle hard nofile 65536
oracle soft stack 10240
oracle hard stack 32768
oracle soft memlock {0}
oracle hard memlock {1}
EOF
echo $?'''.format(str(int(round(memlock))), str(int(round(memlock))),limit_conf_file)
        obj = Oper(user, pwd, host)
        is_file = '''if [[ ! -f "{0}" ]]; then echo 0; else echo 1; fi'''
        is_file_result = obj.command(is_file.format(limit_conf_file))
        if int(is_file_result.strip().strip('\n')) == 1:
            cp_result = obj.command('cp {0} {1}.bak{2};echo $?'.format(limit_conf_file, limit_conf_file,
                                                             datetime.datetime.today().strftime('%Y%m%d%H%M%S')))
            if int(cp_result.strip().strip('\n')) == 0:
                print('{0}文件备份成功！'.format(limit_conf_file))
                modify_result = obj.command(limit_conf)
                if int(modify_result.strip().strip('\n')) == 0:
                    print('{0}文件修改成功！'.format(limit_conf_file))
                    tag_1 = 1
                else:
                    print('{0}文件修改失败！'.format(limit_conf_file))
                    return False
            else:
                print('{0}文件备份失败！'.format(limit_conf_file))
                return False
        else:
            print('{0}文件不存在，cp备份该文件失败！'.format(limit_conf_file))
            return False

        limit_pam_file = '/etc/pam.d/login'
        limit_pam = '''
cat >> {0} <<EOF
#ORACLE SETTING
session required pam_limits.so
EOF
echo $?
'''.format(limit_pam_file)
        is_file_result = obj.command(is_file.format(limit_pam_file))
        if int(is_file_result.strip().strip('\n')) == 1:
            cp_result = obj.command('cp {0} {1}.bak{2};echo $?'.format(limit_pam_file, limit_pam_file,
                                                             datetime.datetime.today().strftime('%Y%m%d%H%M%S')))
            if int(cp_result.strip().strip('\n')) == 0:
                print('{0}文件备份成功！'.format(limit_pam_file))
                modify_result = obj.command(limit_pam)
                if int(modify_result.strip().strip('\n')) == 0:
                    print('{0}文件修改成功！'.format(limit_pam_file))
                    tag_2 = 1
                else:
                    print('{0}文件修改失败！'.format(limit_pam_file))
                    return False
            else:
                print('{0}文件备份失败！'.format(limit_pam_file))
                return False
        else:
            print('{0}文件不存在，cp备份该文件失败！'.format(limit_pam_file))
            return False

        if tag_1 == 1 and tag_2 == 1:
            return True
        else:
            return False

    @staticmethod
    def modify_profile(user,pwd,host):
        profile = '/etc/profile'
        profile_str = '''
cat >> {0} <<EOF
if [ $USER = "oracle" ]; then
    if [ $SHELL = "/bin/ksh" ]; then
        ulimit -p 16384
        ulimit -n 65536
    else
        ulimit -u 16384 -n 65536
    fi
fi
EOF
echo $?'''.format(profile)
        obj = Oper(user, pwd, host)
        is_file = '''if [[ ! -f "{0}" ]]; then echo 0; else echo 1; fi'''
        is_file_result = obj.command(is_file.format(profile))
        if int(is_file_result.strip().strip('\n')) == 1:
            cp_result = obj.command('cp {0} {1}.bak{2};echo $?'.format(profile, profile,
                                                             datetime.datetime.today().strftime('%Y%m%d%H%M%S')))
            if int(cp_result.strip().strip('\n')) == 0:
                print('{0}文件备份成功！'.format(profile))
                modify_result = obj.command(profile_str)
                if int(modify_result.strip().strip('\n')) == 0:
                    print('{0}文件修改成功！'.format(profile))
                    obj.command('source /etc/profile')
                    return True
                else:
                    print('{0}文件修改失败！'.format(profile))
                    return False
            else:
                print('{0}文件备份失败！'.format(profile))
                return False
        else:
            print('{0}文件不存在，cp备份该文件失败！'.format(profile))
            return False

    @staticmethod
    def modify_host(user,pwd,host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbinstall\\setup.conf', encoding='utf-8')
        host_profile = '/etc/hosts'
        ip = config.get('pre_oracle_oinstall', 'ip')
        hostname = config.get('pre_oracle_oinstall', 'hostname')
        host_str = '''
cat >> {2} <<EOF
##############For DB#################
{0} {1}
##############End for DB#############
EOF
echo $?'''.format(ip, hostname,host_profile)
        obj = Oper(user, pwd, host)
        is_file = '''if [[ ! -f "{0}" ]]; then echo 0; else echo 1; fi'''
        is_file_result = obj.command(is_file.format(host_profile))
        if int(is_file_result.strip().strip('\n')) == 1:
            cp_result = obj.command('cp {0} {1}.bak{2};echo $?'.format(host_profile, host_profile,
                                                             datetime.datetime.today().strftime('%Y%m%d%H%M%S')))
            if int(cp_result.strip().strip('\n')) == 0:
                print('{0}文件备份成功！'.format(host_profile))
                modify_result = obj.command(host_str)
                if int(modify_result.strip().strip('\n')) == 0:
                    print('{0}文件修改成功！'.format(host_profile))
                    obj.command('hostnamectl set-hostname {}'.format(hostname))
                    return True
                else:
                    print('{0}文件修改失败！'.format(host_profile))
                    return False
            else:
                print('{0}文件备份失败！'.format(host_profile))
                return False

    @staticmethod
    def stop_transparent_hugepage(user,pwd,host,nr_hugepages):
        obj = Oper(user, pwd, host)
        kernel_file = obj.command('grubby --default-kernel').strip().strip('\n')
        cmd_1 = '''grubby --args="transparent_hugepage=never" --update-kernel {0};echo $?'''.format(kernel_file)
        cmd_2 = '''grubby --args="hugepages={0}" --update-kernel {1};echo $?'''.format(nr_hugepages, kernel_file)
        result_1 = obj.command(cmd_1)
        if int(result_1.strip().strip('\n')) == 0:
            print('透明大页禁用成功！')
            tag_1 = 1
        else:
            print('透明大页禁用失败！')
            return False
        result_2 = obj.command(cmd_2)
        if int(result_2.strip().strip('\n')) == 0:
            print('内核文件中大页参数的配置成功！')
            tag_2 = 1
        else:
            print('内核文件中大页参数的配置失败！')
            return False
        if tag_1 == 1 and tag_2 == 1:
            return True
        else:
            return False
