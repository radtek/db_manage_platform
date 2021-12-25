# -*- coding:UTF-8 -*-

from common.libs.oracle_install.oper import Oper
import datetime
import configparser

# 硬件配置检查
class DbInstall(object):
    @staticmethod
    def os_release_check(user,pwd,host):
        obj = Oper(user, pwd, host)
        cmd = 'cat /etc/oracle-release'
        str = obj.command(cmd)
        result = str.split(' ')[-1].strip('\n')
        if float(result) >= 7.4:
            result = '当前系统版本为：{0}，检查通过！'.format(result)
            return result
        else:
            result = '当前系统版本为：{0}，检查失败！'.format(result)
            return result

    @staticmethod
    def os_memory_check(user, pwd, host):
        obj = Oper(user, pwd, host)
        cmd = 'cat /proc/meminfo | head -1'
        str = obj.command(cmd)
        result = str.split(':')[-1].strip().strip('\n').split(' ')[0]
        if float(result) / 1024 / 1024 > 16:
            result = '当前系统内存为：{0}G，检查通过！'.format(float(result) / 1024 / 1024)
            return result
        else:
            result = '当前系统内存为：{0}G，检查失败！'.format(float(result) / 1024 / 1024)
            return result

    @staticmethod
    def os_swap_check(user, pwd, host):
        obj = Oper(user, pwd, host)
        cmd1 = "swapon -s | sed -n '2p' | awk '{print $3}'"
        str1 = obj.command(cmd1)
        result1 = str1.strip().strip('\n')
        swap_size = float(result1) / 1024 / 1024
        cmd2 = 'cat /proc/meminfo | head -1'
        str2 = obj.command(cmd2)
        result2 = str2.split(':')[-1].strip().strip('\n').split(' ')[0]
        memory_size = float(result2) / 1024 / 1024
        if memory_size > 1 and memory_size < 2:
            if swap_size >= memory_size * 1.5:
                result = '当前系统swap大小为：{0}G，检查通过！'.format(swap_size)
                return result
            else:
                result = '当前系统swap大小为：{0}G，检查失败！'.format(swap_size)
                return result
        if memory_size > 2 and memory_size < 16:
            if swap_size == 16:
                result = '当前系统swap大小为：{0}G，检查通过！'.format(swap_size)
                return result
            else:
                result = '当前系统swap大小为：{0}G，检查失败！'.format(swap_size)
                return result
        if memory_size > 16:
            if swap_size >= 16:
                result = '当前系统swap大小为：{0}G，检查通过！'.format(swap_size)
                return result
            else:
                result = '当前系统swap大小为：{0}G，检查失败！'.format(swap_size)
                return result

    @staticmethod
    def oracle_installdir_check(user, pwd, host):
        obj = Oper(user, pwd, host)
        oracle_install_dir = '/oracle'
        cmd = "df -h | grep '%s$' | awk '{print $1}'" % (oracle_install_dir)
        str = obj.command(cmd)
        result = str.strip('\n')
        if result.endswith('G'):
            if float(result.strip('G')) >= 100:
                result = '当前系统oracle安装目录为：{0}，大小：{1}，检查通过！'.format(oracle_install_dir, result)
                return result
            else:
                result = '当前系统oracle安装目录为：{0}，大小：{1}，检查失败！'.format(oracle_install_dir, result)
                return result
        if result.endswith('T'):
            result = '当前系统oracle安装目录为：{0}，大小为：{1}，检查通过！'.format(oracle_install_dir, result)
            return result
        if result.endswith('M'):
            result = '当前系统oracle安装目录为：{0}，大小为：{1}，检查失败！'.format(oracle_install_dir, result)
            return result

    @staticmethod
    def stop_firewall(user, pwd, host):
        stop_firewall_cmd = 'systemctl stop firewalld.service > /dev/null 2>&1;echo $?'
        disable_firewall_cmd = 'systemctl disable firewalld.service > /dev/null 2>&1;echo $?'
        obj = Oper(user, pwd, host)
        stop_result = obj.command(stop_firewall_cmd)
        disable_result = obj.command(disable_firewall_cmd)
        if int(stop_result.strip().strip('\n')) == 0 and int(disable_result.strip().strip('\n')) == 0:
            result = '系统防火墙关闭和禁用成功！'
            return result
        else:
            result = '系统防火墙关闭和禁用失败！'
            return result

    @staticmethod
    def stop_selinux(user, pwd, host):
        selinux_conf_file = '/etc/selinux/config'
        obj = Oper(user, pwd, host)
        cp_result = obj.command('cp {0} {1}.bak{2};echo $?'.format(selinux_conf_file, selinux_conf_file,
                                                                   datetime.datetime.today().strftime('%Y%m%d%H%M%S')))
        if int(cp_result.strip().strip('\n')) == 0:
            print('{0}文件拷贝成功！'.format(selinux_conf_file))
        else:
            print('{0}文件拷贝失败！'.format(selinux_conf_file))
        modify_result = obj.command(
            "sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' {0};echo $?".format(selinux_conf_file))
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
            return 'selinux关闭和禁用成功！'
        else:
            return 'selinux关闭和禁用失败！'

    @staticmethod
    def rpm_install(user, pwd, host):
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
            return 'yum包安装成功！'
        else:
            print('yum操作失败，请检查yum源！')
            return 'yum包安装失败！'

    @staticmethod
    def user_group_add(user, pwd, host):
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
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
            oracle_pwd = config.get('pre_oracle_oinstall', 'oracle_pwd')
            obj.command(oracle_pwd_cmd.format(oracle_pwd))
            print('oracle用户创建和设置密码成功！')
        if int(oinstall_result.strip().strip('\n')) != 0 and \
                int(asmdba_result.strip().strip('\n')) != 0 and \
                int(asmoper_result.strip().strip('\n')) != 0 and \
                int(dba_result.strip().strip('\n')) != 0 and \
                int(oper_result.strip().strip('\n')) != 0 and \
                int(backupdba_result.strip().strip('\n')) != 0 and \
                int(dgdba_result.strip().strip('\n')) != 0 and \
                int(kmdba_result.strip().strip('\n')) != 0 and \
                int(racdba_result.strip().strip('\n')) != 0 and \
                int(oracle_result.strip().strip('\n')) != 0:
            return '用户和组创建成功！'
        else:
            return '用户和组创建失败！'

    @staticmethod
    def create_dir(user, pwd, host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
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
            return '相关所有目录创建成功！'
        else:
            return '相关目录创建失败'

    @staticmethod
    def modify_oracle_profile(user, pwd, host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
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
echo $?'''.format(oracle_sid, oracle_base, oracle_home, nls_lang, oracle_bash_profile)
        obj = Oper(user, pwd, host)
        is_file = '''if [[ ! -f "{0}" ]]; then echo 0; else echo 1; fi'''
        is_file_result = obj.command(is_file.format(oracle_bash_profile))
        if int(is_file_result.strip().strip('\n')) == 1:
            cp_result = obj.command('cp {0} {1}.bak{2};echo $?'.format(oracle_bash_profile, oracle_bash_profile,
                                                                       datetime.datetime.today().strftime(
                                                                           '%Y%m%d%H%M%S')))
            if int(cp_result.strip().strip('\n')) == 0:
                print('{0}文件备份成功！'.format(oracle_bash_profile))
                modify_result = obj.command(oracle_profile_config)
                if int(modify_result.strip().strip('\n')) == 0:
                    print('{0}文件修改成功！'.format(oracle_bash_profile))
                    return 'bash_profile文件配置成功！'
                else:
                    print('{0}文件修改失败！'.format(oracle_bash_profile))
                    return 'bash_profile文件配置失败！'
            else:
                print('{0}文件备份失败！'.format(oracle_bash_profile))
                return 'bash_profile文件备份失败！'
        else:
            print('oracle用户的{0}文件不存在，cp备份该文件失败！'.format(oracle_bash_profile))
            return 'bash_profile文件不存在！'

    @staticmethod
    def modify_os_parameter_1(user, pwd, host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
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
echo $?'''.format(str(int(round(shmall))), str(int(round(shmmax))), str(int(round(nr_hugepages))), sysctl_file)
        is_file = '''if [[ ! -f "{0}" ]]; then echo 0; else echo 1; fi'''
        is_file_result = obj.command(is_file.format(sysctl_file))
        if int(is_file_result.strip().strip('\n')) == 1:
            cp_result = obj.command('cp {0} {1}.bak{2};echo $?'.format(sysctl_file, sysctl_file,
                                                                       datetime.datetime.today().strftime(
                                                                           '%Y%m%d%H%M%S')))
            if int(cp_result.strip().strip('\n')) == 0:
                print('{0}文件备份成功！'.format(sysctl_file))
                modify_result = obj.command(sysctl_config)
                if int(modify_result.strip().strip('\n')) == 0:
                    print('{0}文件修改成功！'.format(sysctl_file))
                    obj.command('sysctl -p >& /devnull')
                    return 'sysctl.conf文件配置成功！', str(int(round(nr_hugepages)))
                else:
                    print('{0}文件修改失败！'.format(sysctl_file))
                    return 'sysctl.conf文件配置失败！'
            else:
                print('{0}文件备份失败！'.format(sysctl_file))
                return 'sysctl.conf文件备份失败！'
        else:
            print('{0}文件不存在，cp备份该文件失败！'.format(sysctl_file))
            return 'sysctl.conf文件不存在！'

    @staticmethod
    def modify_os_parameter_2(user, pwd, host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
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
echo $?'''.format(str(int(round(memlock))), str(int(round(memlock))), limit_conf_file)
        obj = Oper(user, pwd, host)
        is_file = '''if [[ ! -f "{0}" ]]; then echo 0; else echo 1; fi'''
        is_file_result = obj.command(is_file.format(limit_conf_file))
        if int(is_file_result.strip().strip('\n')) == 1:
            cp_result = obj.command('cp {0} {1}.bak{2};echo $?'.format(limit_conf_file, limit_conf_file,
                                                                       datetime.datetime.today().strftime(
                                                                           '%Y%m%d%H%M%S')))
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
                                                                       datetime.datetime.today().strftime(
                                                                           '%Y%m%d%H%M%S')))
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
            return 'limits.conf文件修改成功！'
        else:
            return 'limits.conf文件修改失败！'

    @staticmethod
    def modify_profile(user, pwd, host):
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
                                                                       datetime.datetime.today().strftime(
                                                                           '%Y%m%d%H%M%S')))
            if int(cp_result.strip().strip('\n')) == 0:
                print('{0}文件备份成功！'.format(profile))
                modify_result = obj.command(profile_str)
                if int(modify_result.strip().strip('\n')) == 0:
                    print('{0}文件修改成功！'.format(profile))
                    obj.command('source /etc/profile')
                    return 'profile文件修改成功！'
                else:
                    print('{0}文件修改失败！'.format(profile))
                    return 'profile文件修改失败！'
            else:
                print('{0}文件备份失败！'.format(profile))
                return 'profile文件备份失败！'
        else:
            print('{0}文件不存在，cp备份该文件失败！'.format(profile))
            return 'profile文件不存在！'

    @staticmethod
    def modify_host(user, pwd, host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
        host_profile = '/etc/hosts'
        ip = config.get('pre_oracle_oinstall', 'ip')
        hostname = config.get('pre_oracle_oinstall', 'hostname')
        host_str = '''
cat >> {2} <<EOF
##############For DB#################
{0} {1}
##############End for DB#############
EOF
echo $?'''.format(ip, hostname, host_profile)
        obj = Oper(user, pwd, host)
        is_file = '''if [[ ! -f "{0}" ]]; then echo 0; else echo 1; fi'''
        is_file_result = obj.command(is_file.format(host_profile))
        if int(is_file_result.strip().strip('\n')) == 1:
            cp_result = obj.command('cp {0} {1}.bak{2};echo $?'.format(host_profile, host_profile,
                                                                       datetime.datetime.today().strftime(
                                                                           '%Y%m%d%H%M%S')))
            if int(cp_result.strip().strip('\n')) == 0:
                print('{0}文件备份成功！'.format(host_profile))
                modify_result = obj.command(host_str)
                if int(modify_result.strip().strip('\n')) == 0:
                    print('{0}文件修改成功！'.format(host_profile))
                    obj.command('hostnamectl set-hostname {}'.format(hostname))
                    return 'hosts文件配置成功！'
                else:
                    print('{0}文件修改失败！'.format(host_profile))
                    return 'hosts文件配置失败！'
            else:
                print('{0}文件备份失败！'.format(host_profile))
                return 'hosts文件备份失败！'
        else:
            print('{0}文件不存在，cp备份该文件失败！'.format(host_profile))
            return 'hosts文件不存在！'

    @staticmethod
    def stop_transparent_hugepage(user, pwd, host, nr_hugepages):
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
            return '透明大页禁用失败！'
        result_2 = obj.command(cmd_2)
        if int(result_2.strip().strip('\n')) == 0:
            print('内核文件中大页参数的配置成功！')
            tag_2 = 1
        else:
            print('内核文件中大页参数的配置失败！')
            return '内核文件中大页参数的配置失败！'
        if tag_1 == 1 and tag_2 == 1:
            return '透明大页禁用成功！'
        else:
            return '透明大页禁用失败！'

    @staticmethod
    def unzip_db_file(user, pwd, host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
        dbsoft_dir = config.get('db_install', 'dbsoft_dir')
        name = config.get('db_install', 'db_zip_file')
        dest_dir = config.get('pre_oracle_oinstall', 'oracle_home')
        db_file_name = dbsoft_dir + '/' + name
        obj = Oper(user, pwd, host)
        is_file = '''if [[ ! -f "{0}" ]]; then echo 0; else echo 1; fi'''
        is_file_result = obj.command(is_file.format(db_file_name))
        if int(is_file_result.strip().strip('\n')) == 1:
            unzip_cmd = 'unzip {0} -d {1} > /dev/null 2>&1;echo $?'.format(db_file_name, dest_dir)
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
    def db_software_install(user, pwd, host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
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
echo $?'''.format(oracle_base, oracle_base, oracle_home, db_resp_file)
        obj = Oper(user, pwd, host)
        gen_rsp_result = obj.command(response_str)
        if int(gen_rsp_result.strip().strip('\n')) == 0:
            print('19c_db_software_install.rsp响应文件制作成功！')
            obj.command('chown oracle:oinstall {0}'.format(db_resp_file))
        else:
            print('19c_db_software_install.rsp响应文件制作失败！')
            return '19c_db_software_install.rsp响应文件制作失败！'
        is_file = '''if [[ ! -f "{0}" ]]; then echo 0; else echo 1; fi'''
        is_file_result = obj.command(is_file.format(db_resp_file))
        if int(is_file_result.strip().strip('\n')) == 1:
            install_cmd = "su - oracle -c 'echo {0} | {1}/runInstaller -silent -force \
                    -noconfig -ignorePrereq -responseFile {2}'".format(root_pwd, oracle_home, db_resp_file)
            install_result = obj.command(install_cmd)
            return install_result
        else:
            print('{0}响应文件不存在！'.format(db_resp_file))
            return '{0}响应文件不存在！'.format(db_resp_file)

    @staticmethod
    def listener_install(user, pwd, host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
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
            return '19c_listener_install.rsp响应文件制作失败！'
        is_file = '''if [[ ! -f "{0}" ]]; then echo 0; else echo 1; fi'''
        is_file_result = obj.command(is_file.format(listener_resp_file))
        if int(is_file_result.strip().strip('\n')) == 1:
            install_cmd = "su - oracle -c 'netca -silent -responsefile {0}'".format(listener_resp_file)
            install_result = obj.command(install_cmd)
            return install_result
        else:
            print('{0}响应文件不存在！'.format(listener_resp_file))
            return '{0}响应文件不存在！'.format(listener_resp_file)

    @staticmethod
    def db_install(user, pwd, host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
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
        template_file = config.get('pre_oracle_oinstall',
                                   'oracle_home') + '/assistants/dbca/templates/General_Purpose.dbc'
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
            return '{0}模板文件不存在！'.format(template_file)

    @staticmethod
    def patch_install(user, pwd, host):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\oracle_install\\setup.conf', encoding='utf-8')
        dbsoft_dir = config.get('db_install', 'dbsoft_dir')
        opatch_name = config.get('patch_install', 'opatch_name')
        patch_name = config.get('patch_install', 'patch_name')
        oracle_home = config.get('pre_oracle_oinstall', 'oracle_home')
        opatch_file = dbsoft_dir + '/' + opatch_name
        patch_file = dbsoft_dir + '/' + patch_name
        obj = Oper(user, pwd, host)
        is_file = '''if [[ ! -f "{0}" ]]; then echo 0; else echo 1; fi'''
        is_file_result = obj.command(is_file.format(opatch_file))
        if int(is_file_result.strip().strip('\n')) == 1:
            unzip_opatch_result = obj.command(
                'unzip {0} -d {1}> /dev/null 2>&1;echo $?'.format(opatch_file, dbsoft_dir))
            if int(unzip_opatch_result.strip().strip('\n')) == 0:
                print('{0}解压成功！'.format(opatch_file))
            else:
                print('{0}解压失败！'.format(opatch_file))
                return '{0}解压失败！'.format(opatch_file)
        else:
            print('{0}文件不存在！'.format(opatch_file))
            return '{0}文件不存在！'.format(opatch_file)
        is_dir = '''if [[ ! -d "{0}" ]]; then echo 0; else echo 1; fi'''
        is_dir_result = obj.command(is_dir.format(dbsoft_dir + '/OPatch'))
        if int(is_dir_result.strip().strip('\n')) == 1:
            obj.command('chown oracle:oinstall -R {0}'.format(dbsoft_dir + '/OPatch'))
            obj.command('mv {0}/OPatch {1}/OPatch.bak'.format(oracle_home, oracle_home))
            obj.command('mv {0} {1}/'.format(dbsoft_dir + '/OPatch', oracle_home))
            print('OPatch目录替换成功！')
        else:
            print('{0}目录不存在！'.format(dbsoft_dir + '/OPatch'))
            return '{0}目录不存在！'.format(dbsoft_dir + '/OPatch')
        is_file_result = obj.command(is_file.format(patch_file))
        if int(is_file_result.strip().strip('\n')) == 1:
            unzip_patch_result = obj.command('unzip {0} -d {1}> /dev/null 2>&1;echo $?'.format(patch_file, dbsoft_dir))
            if int(unzip_patch_result.strip().strip('\n')) == 0:
                print('{0}解压成功！'.format(patch_file))
            else:
                print('{0}解压失败！'.format(patch_file))
                return '{0}解压失败！'.format(patch_file)
        else:
            print('{0}文件不存在！'.format(patch_file))
            return '{0}文件不存在！'.format(patch_file)
        name = patch_name.split('_')[0].strip('p')
        is_dir_result = obj.command(is_dir.format(dbsoft_dir + '/' + name))
        if int(is_dir_result.strip().strip('\n')) == 1:
            obj.command('chown oracle:oinstall -R {0}'.format(dbsoft_dir + '/' + name))
            obj.command("su - oracle -c 'lsnrctl stop'")
            print('监听停止成功！')
            db_shut_cmd = """
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
            db_start_cmd = """
su - oracle -c 'sqlplus -S / as sysdba << EOF
startup
exit
EOF'"""
            obj.command(db_start_cmd)
            print('数据库开启成功！')
            return install_result
        else:
            print('{0}补丁文件不存在！'.format(dbsoft_dir + '/' + name))
            return '{0}补丁文件不存在！'.format(dbsoft_dir + '/' + name)