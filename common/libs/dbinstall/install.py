# -*- coding:utf-8 -*-

import wx
import configparser
from hwckframe import HwCkFrame
from configframe import ConfigFrame
from preinstall import PreOracleInstall
from dbinstall import DBInstall
from insframe import InsFrame
from patchinstall import PatchInstall

config = configparser.ConfigParser()
config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbinstall\\setup.conf',encoding='utf-8')

class Install(wx.Frame):
    def __init__(self):
        super().__init__(parent=None,title='数据库安装工具',size=(800,600))
        self.Center()
        self.nr_hugepages = ''

        # 定义左右分隔窗口
        splitter = wx.SplitterWindow(parent=self, id=-1)
        leftpanel = wx.Panel(parent=splitter)
        rightpanel = wx.Panel(parent=splitter)
        splitter.SplitVertically(leftpanel, rightpanel, 250)
        splitter.SetMinimumPaneSize(100)

        # 定义左窗口树形结构
        self.tree = self.CreateTreeCtrl(leftpanel)
        # 树形结构绑定监听函数
        self.Bind(wx.EVT_TREE_SEL_CHANGING, self.on_tree, self.tree)

        # 左窗口纵向布局器
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(self.tree, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        leftpanel.SetSizer(vbox1)

        # 右窗口纵向布局器
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        self.content = wx.StaticText(parent=rightpanel, label='')
        vbox2.Add(self.content, proportion=1, flag=wx.ALL | wx.EXPAND, border=50)
        rightpanel.SetSizer(vbox2)

    # 树形结构监听函数
    def on_tree(self, event):
        item = event.GetItem()
        oper_type = self.tree.GetItemText(item).strip()
        if oper_type == '系统版本检查':
            self.content.SetLabelText('启动{0}窗口!'.format(oper_type))
            app = wx.App()
            frame = HwCkFrame(oper_type)
            frame.Show()
            app.MainLoop()
        if oper_type == '系统内存检查':
            self.content.SetLabelText('启动{0}窗口!'.format(oper_type))
            app = wx.App()
            frame = HwCkFrame(oper_type)
            frame.Show()
            app.MainLoop()
        if oper_type == '系统swap检查':
            self.content.SetLabelText('启动{0}窗口!'.format(oper_type))
            app = wx.App()
            frame = HwCkFrame(oper_type)
            frame.Show()
            app.MainLoop()
        if oper_type == '安装目录检查':
            self.content.SetLabelText('启动{0}窗口!'.format(oper_type))
            app = wx.App()
            frame = HwCkFrame(oper_type)
            frame.Show()
            app.MainLoop()
        if oper_type == '安装软件上传':
            self.content.SetLabelText('启动{0}窗口!'.format(oper_type))
            app = wx.App()
            frame = HwCkFrame(oper_type)
            frame.Show()
            app.MainLoop()
        if oper_type == '生成安装配置文件':
            self.content.SetLabelText('启动{0}窗口!'.format(oper_type))
            app = wx.App()
            frame = ConfigFrame(oper_type)
            frame.Show()
            app.MainLoop()
        if oper_type == '禁用防火墙':
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            result = PreOracleInstall.stop_firewall('root',sec2['root_pwd'],sec1['ip'])
            if result:
                self.content.SetLabelText('关闭和禁用防火墙成功!')
            else:
                self.content.SetLabelText('关闭和禁用防火墙失败!')
        if oper_type == '禁用selinux':
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            result = PreOracleInstall.stop_selinux('root',sec2['root_pwd'],sec1['ip'])
            if result:
                self.content.SetLabelText('关闭和禁用selinux成功!')
            else:
                self.content.SetLabelText('关闭和禁用selinux失败!')
        if oper_type == 'rpm包安装':
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            result = PreOracleInstall.rpm_install('root',sec2['root_pwd'],sec1['ip'])
            if result:
                self.content.SetLabelText('rpm包安装成功!')
            else:
                self.content.SetLabelText('rpm包安装失败!')
        if oper_type == '添加用户':
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            result = PreOracleInstall.user_group_add('root',sec2['root_pwd'],sec1['ip'])
            if result:
                self.content.SetLabelText('所有用户创建成功!')
            else:
                self.content.SetLabelText('用户创建失败，有的用户已经存在!')
        if oper_type == '创建目录':
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            result = PreOracleInstall.create_dir('root',sec2['root_pwd'],sec1['ip'])
            if result:
                self.content.SetLabelText('所有目录创建成功!')
            else:
                self.content.SetLabelText('目录创建失败，有的目录已经存在!')
        if oper_type == 'bash_profile文件配置':
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            result = PreOracleInstall.modify_oracle_profile('root',sec2['root_pwd'],sec1['ip'])
            if result:
                self.content.SetLabelText('bash_profile文件配置成功!')
            else:
                self.content.SetLabelText('bash_profile文件配置失败!')
        if oper_type == 'sysctl.conf文件配置':
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            result,self.nr_hugepages = PreOracleInstall.modify_os_parameter_1('root',sec2['root_pwd'],sec1['ip'])
            if result:
                self.content.SetLabelText('sysctl.conf文件配置成功!')
            else:
                self.content.SetLabelText('sysctl.conf文件配置失败!')
        if oper_type == 'limits.conf文件配置':
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            result = PreOracleInstall.modify_os_parameter_2('root',sec2['root_pwd'],sec1['ip'])
            if result:
                self.content.SetLabelText('limits.conf文件配置成功!')
            else:
                self.content.SetLabelText('limits.conf文件配置失败!')
        if oper_type == 'profile文件配置':
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            result = PreOracleInstall.modify_profile('root',sec2['root_pwd'],sec1['ip'])
            if result:
                self.content.SetLabelText('profile文件配置成功!')
            else:
                self.content.SetLabelText('profile文件配置失败!')
        if oper_type == 'hosts文件配置':
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            result = PreOracleInstall.modify_host('root',sec2['root_pwd'],sec1['ip'])
            if result:
                self.content.SetLabelText('hosts文件配置成功!')
            else:
                self.content.SetLabelText('hosts文件配置失败!')
        if oper_type == '关闭透明大页':
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            result = PreOracleInstall.stop_transparent_hugepage('root',sec2['root_pwd'],sec1['ip'],self.nr_hugepages)
            if result:
                self.content.SetLabelText('关闭透明大页操作成功！')
            else:
                self.content.SetLabelText('关闭透明大页操作失败！')
        if oper_type == '数据库软件安装':
            self.content.SetLabelText('正在解压数据库安装软件...')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            unzip_result = DBInstall.unzip_db_file('root',sec2['root_pwd'],sec1['ip'])
            if unzip_result:
                self.content.SetLabelText('数据库安装软件解压成功！')
            else:
                self.content.SetLabelText('数据库安装软件解压失败！')
            self.content.SetLabelText('数据库软件正在安装...')
            install_result = DBInstall.db_software_install('root',sec2['root_pwd'],sec1['ip'])
            app = wx.App()
            frame = InsFrame(oper_type,install_result)
            self.content.SetLabelText('数据库软件安装完成！')
            frame.Show()
            app.MainLoop()
        if oper_type == '数据库监听安装':
            self.content.SetLabelText('数据库监听安装中...')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            install_result = DBInstall.listener_install('root',sec2['root_pwd'],sec1['ip'])
            app = wx.App()
            frame = InsFrame(oper_type,install_result)
            self.content.SetLabelText('数据库监听安装完成！')
            frame.Show()
            app.MainLoop()
        if oper_type == '数据库安装':
            self.content.SetLabelText('数据库安装中...')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            install_result = DBInstall.db_install('root',sec2['root_pwd'],sec1['ip'])
            app = wx.App()
            frame = InsFrame(oper_type,install_result)
            self.content.SetLabelText('数据库安装完成！')
            frame.Show()
            app.MainLoop()
        if oper_type == '补丁安装':
            self.content.SetLabelText('补丁安装中...')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            install_result = PatchInstall.patch_install('root',sec2['root_pwd'],sec1['ip'])
            app = wx.App()
            frame = InsFrame(oper_type,install_result)
            self.content.SetLabelText('补丁安装完成！')
            frame.Show()
            app.MainLoop()
        if oper_type == '补丁信息注册':
            self.content.SetLabelText('补丁信息注册中...')
            sec1 = config['pre_oracle_oinstall']
            sec2 = config['db_install']
            patch_result = PatchInstall.patch_registry('root',sec2['root_pwd'],sec1['ip'])
            app = wx.App()
            frame = InsFrame(oper_type,patch_result)
            self.content.SetLabelText('补丁信息注册完成！')
            frame.Show()
            app.MainLoop()

    # 树形结构构造方法
    def CreateTreeCtrl(self, parent):
        tree = wx.TreeCtrl(parent)
        imglist = wx.ImageList(16, 16, True, 2)
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, size=wx.Size(16, 16)))
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, size=wx.Size(16, 16)))
        tree.AssignImageList(imglist)
        root = tree.AddRoot('数据库安装工具', image=0)
        item1 = []
        item1.append(tree.AppendItem(root, 'oracle单实例安装', 0))
        for i in range(len(item1)):
            id = item1[i]
            tree.AppendItem(id, '系统版本检查', 1)
            tree.AppendItem(id, '系统内存检查', 1)
            tree.AppendItem(id, '系统swap检查', 1)
            tree.AppendItem(id, '安装目录检查', 1)
            tree.AppendItem(id, '安装软件上传', 1)
            tree.AppendItem(id, '生成安装配置文件', 1)
            tree.AppendItem(id, '禁用防火墙', 1)
            tree.AppendItem(id, '禁用selinux', 1)
            tree.AppendItem(id, 'rpm包安装', 1)
            tree.AppendItem(id, '添加用户', 1)
            tree.AppendItem(id, '创建目录', 1)
            tree.AppendItem(id, 'bash_profile文件配置', 1)
            tree.AppendItem(id, 'sysctl.conf文件配置',1)
            tree.AppendItem(id, 'limits.conf文件配置', 1)
            tree.AppendItem(id, 'profile文件配置', 1)
            tree.AppendItem(id, 'hosts文件配置', 1)
            tree.AppendItem(id, '关闭透明大页', 1)
            tree.AppendItem(id, '数据库软件安装', 1)
            tree.AppendItem(id, '数据库监听安装', 1)
            tree.AppendItem(id, '数据库安装', 1)
            tree.AppendItem(id, '补丁安装', 1)
            tree.AppendItem(id, '补丁信息注册', 1)
        tree.Expand(root)
        tree.Expand(item1[0])
        tree.SelectItem(root)
        return tree

class InstallApp(wx.App):
    def OnInit(self):
        frame = Install()
        frame.Show()
        return True

    def OnExit(self):
        print('安装工具程序退出！')
        return 0

if __name__ == '__main__':
    app = InstallApp()
    app.MainLoop()
