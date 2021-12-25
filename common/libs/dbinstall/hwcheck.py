# -*- coding:utf-8 -*-

from oper import Oper

class HardwareCheck(object):
    @staticmethod
    def os_release_check(user,pwd,host):
        obj = Oper(user, pwd, host)
        cmd = 'cat /etc/oracle-release'
        str = obj.command(cmd)
        result = str.split(' ')[-1].strip('\n')
        if float(result) >= 7.4:
            print('当前系统版本为：{0}，检查通过！'.format(result))
            return True
        else:
            print('当前系统版本为：{0}，检查失败！'.format(result))
            return False

    @staticmethod
    def os_memory_check(user,pwd,host):
        obj = Oper(user, pwd, host)
        cmd = 'cat /proc/meminfo | head -1'
        str = obj.command(cmd)
        result = str.split(':')[-1].strip().strip('\n').split(' ')[0]
        if float(result) / 1024 / 1024 > 16:
            print('当前系统内存为：{0}G，检查通过！'.format(float(result) / 1024 / 1024))
            return True
        else:
            print('当前系统内存为：{0}G，检查失败！'.format(float(result) / 1024 / 1024))
            return False

    @staticmethod
    def os_swap_check(user,pwd,host):
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
                print('当前系统swap大小为：{0}G，检查通过！'.format(swap_size))
                return True
            else:
                print('当前系统swap大小为：{0}G，检查失败！'.format(swap_size))
                return False
        if memory_size > 2 and memory_size < 16:
            if swap_size == 16:
                print('当前系统swap大小为：{0}G，检查通过！'.format(swap_size))
                return True
            else:
                print('当前系统swap大小为：{0}G，检查失败！'.format(swap_size))
                return False
        if memory_size > 16:
            if swap_size >= 16:
                print('当前系统swap大小为：{0}G，检查通过！'.format(swap_size))
                return True
            else:
                print('当前系统swap大小为：{0}G，检查失败！'.format(swap_size))
                return False

    @staticmethod
    def oracle_installdir_check(user,pwd,host):
        obj = Oper(user, pwd, host)
        oracle_install_dir = '/oracle'
        cmd = "df -h | grep '%s$' | awk '{print $1}'" % (oracle_install_dir)
        str = obj.command(cmd)
        result = str.strip('\n')
        if result.endswith('G'):
            if float(result.strip('G')) >= 100:
                print('当前系统oracle安装目录为：{0}，大小：{1}，检查通过！'.format(oracle_install_dir, result))
                return True
            else:
                print('当前系统oracle安装目录为：{0}，大小：{1}，检查失败！'.format(oracle_install_dir, result))
                return False
        if result.endswith('T'):
            print('当前系统oracle安装目录为：{0}，大小为：{1}，检查通过！'.format(oracle_install_dir, result))
            return True
        if result.endswith('M'):
            print('当前系统oracle安装目录为：{0}，大小为：{1}，检查失败！'.format(oracle_install_dir, result))
            return False
