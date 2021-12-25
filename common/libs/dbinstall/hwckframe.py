# -*- coding:utf-8 -*-

# 定义弹框
import wx
from hwcheck import HardwareCheck
from oper import Oper

class HwCkFrame(wx.Frame):
    def __init__(self,oper_type):
        if oper_type == '安装软件上传':
            super().__init__(parent=None,title='{0}'.format(oper_type),size=(600,300))
        else:
            super().__init__(parent=None, title='{0}'.format(oper_type), size=(400, 200))
        self.Center()
        self.oper_type = oper_type
        # 定义面板控件
        panel = wx.Panel(parent=self)

        # 定义静态文本控件
        statictext1 = wx.StaticText(parent=panel, label='目标端用户：')
        statictext2 = wx.StaticText(parent=panel, label='目标端密码：')
        statictext3 = wx.StaticText(parent=panel, label='目标端ip：')
        if self.oper_type != '安装软件上传':
            statictext4 = wx.StaticText(parent=panel, label='检查结果：')
            self.statictext5 = wx.StaticText(parent=panel)
        else:
            statictext4 = wx.StaticText(parent=panel, label='上传结果：')
            self.statictext5 = wx.StaticText(parent=panel)

        # 定义按钮控件
        if self.oper_type == '安装软件上传':
            btn = wx.Button(parent=panel,label='上传安装软件',id=1)
        else:
            btn = wx.Button(parent=panel, label='检查', id=1)
        # 按钮绑定监听方法
        self.Bind(wx.EVT_BUTTON,self.on_click,btn)

        # 定义输入文本控件
        self.tc1 = wx.TextCtrl(parent=panel)
        self.tc2 = wx.TextCtrl(parent=panel)
        self.tc3 = wx.TextCtrl(parent=panel)

        # 定义横向布局器控件
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)

        # 添加静态文本控件
        hbox1.Add(statictext1, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox1.Add(self.tc1, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox2.Add(statictext2, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox2.Add(self.tc2, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox3.Add(statictext3, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox3.Add(self.tc3, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox4.Add(statictext4, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox4.Add(self.statictext5, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox5.Add(btn, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)

        # 定义纵向布局控件
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox1, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox2, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox3, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox4, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox5, proportion=1, flag=wx.CENTER | wx.FIXED_MINSIZE, border=5)
        panel.SetSizer(vbox)

    def on_click(self,event):
        user = self.tc1.GetValue().strip()
        pwd = self.tc2.GetValue().strip()
        host = self.tc3.GetValue().strip()
        if self.oper_type == '系统版本检查':
            result = HardwareCheck.os_release_check(user,pwd,host)
            if result:
                self.statictext5.SetLabelText('检查通过！')
            else:
                self.statictext5.SetLabelText('检查失败！')
        if self.oper_type == '系统内存检查':
            result = HardwareCheck.os_memory_check(user,pwd,host)
            if result:
                self.statictext5.SetLabelText('检查通过！')
            else:
                self.statictext5.SetLabelText('检查失败！')
        if self.oper_type == '系统swap检查':
            result = HardwareCheck.os_swap_check(user,pwd,host)
            if result:
                self.statictext5.SetLabelText('检查通过！')
            else:
                self.statictext5.SetLabelText('检查失败！')
        if self.oper_type == '安装目录检查':
            result = HardwareCheck.oracle_installdir_check(user,pwd,host)
            if result:
                self.statictext5.SetLabelText('检查通过！')
            else:
                self.statictext5.SetLabelText('检查失败！')
        if self.oper_type == '安装软件上传':
            dbsoft_base_dir = 'E:\\project\\dbmanage_v4\\common\\libs\\dbinstall\\dbsoft\\'
            remote_soft_dir = '/dbsoft/'
            dbsoft_file = 'LINUX.X64_193000_db_home.zip'
            opatch_file = 'p6880880_190000_Linux-x86-64.zip'
            patch_file ='p32545013_190000_Linux-x86-64.zip'
            mkdir_cmd = 'mkdir -p {0};echo $?'.format(remote_soft_dir)
            obj = Oper(user,pwd,host)
            mkdir_result = obj.command(mkdir_cmd)
            if int(mkdir_result.strip('\n').strip()) == 0:
                print('{0}远程服务器创建目录{1}成功！'.format(host,remote_soft_dir))
                self.statictext5.SetLabelText('所有安装文件正在上传...')
                print('{0}正在上传！'.format(dbsoft_file))
                db_local_file = dbsoft_base_dir + dbsoft_file
                db_remote_file =  remote_soft_dir + dbsoft_file
                obj.upload(db_local_file,db_remote_file)
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
                self.statictext5.SetLabelText('所有安装文件上传成功！')
            else:
                print('{0}远程服务器创建目录{1}失败！'.format(host, remote_soft_dir))
                self.statictext5.SetLabelText('{0}远程服务器创建目录{1}失败，无法上传文件！'.format(host, remote_soft_dir))
