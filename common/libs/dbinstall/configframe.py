# -*- coding:utf-8 -*-

import wx

class ConfigFrame(wx.Frame):
    def __init__(self,oper_type):
        super().__init__(parent=None, title='{0}'.format(oper_type), size=(600, 900))
        self.Center()
        self.oper_type = oper_type
        # 定义面板控件
        panel = wx.Panel(parent=self)

        # 定义静态文本控件
        statictext1 = wx.StaticText(parent=panel, label='oracle安装目录：')
        statictext2 = wx.StaticText(parent=panel, label='oracle工具目录：')
        statictext3 = wx.StaticText(parent=panel, label='oracle数据目录：')
        statictext4 = wx.StaticText(parent=panel, label='oracle归档目录：')
        statictext5 = wx.StaticText(parent=panel, label='oracle_base目录：')
        statictext6 = wx.StaticText(parent=panel, label='oracle_home目录：')
        statictext7 = wx.StaticText(parent=panel, label='oracle用户密码：')
        statictext8 = wx.StaticText(parent=panel, label='数据库sid：')
        statictext9 = wx.StaticText(parent=panel, label='客户端字符集：')
        statictext10 = wx.StaticText(parent=panel, label='SGA大小：')
        statictext11 = wx.StaticText(parent=panel, label='ip地址：')
        statictext12 = wx.StaticText(parent=panel, label='主机名：')
        statictext13 = wx.StaticText(parent=panel, label='安装软件目录：')
        statictext14 = wx.StaticText(parent=panel, label='root用户密码：')
        statictext15 = wx.StaticText(parent=panel, label='db安装软件：')
        statictext16 = wx.StaticText(parent=panel, label='sys用户密码：')
        statictext17 = wx.StaticText(parent=panel, label='system用户密码：')
        statictext18 = wx.StaticText(parent=panel, label='数据库总内存：')
        statictext19 = wx.StaticText(parent=panel, label='数据库字符集：')
        statictext20 = wx.StaticText(parent=panel, label='opatch文件：')
        statictext21 = wx.StaticText(parent=panel, label='补丁文件：')
        statictext22 = wx.StaticText(parent=panel, label='结果：')
        self.statictext23 = wx.StaticText(parent=panel, label='')

        # 定义按钮控件
        btn = wx.Button(parent=panel, label='生成安装配置文件', id=1)
        # 按钮绑定监听方法
        self.Bind(wx.EVT_BUTTON,self.on_click,btn)

        # 定义输入文本控件
        self.tc1 = wx.TextCtrl(parent=panel)
        self.tc2 = wx.TextCtrl(parent=panel)
        self.tc3 = wx.TextCtrl(parent=panel)
        self.tc4 = wx.TextCtrl(parent=panel)
        self.tc5 = wx.TextCtrl(parent=panel)
        self.tc6 = wx.TextCtrl(parent=panel)
        self.tc7 = wx.TextCtrl(parent=panel)
        self.tc8 = wx.TextCtrl(parent=panel)
        self.tc9 = wx.TextCtrl(parent=panel)
        self.tc10 = wx.TextCtrl(parent=panel)
        self.tc11 = wx.TextCtrl(parent=panel)
        self.tc12 = wx.TextCtrl(parent=panel)
        self.tc13 = wx.TextCtrl(parent=panel)
        self.tc14 = wx.TextCtrl(parent=panel)
        self.tc15 = wx.TextCtrl(parent=panel)
        self.tc16 = wx.TextCtrl(parent=panel)
        self.tc17 = wx.TextCtrl(parent=panel)
        self.tc18 = wx.TextCtrl(parent=panel)
        self.tc19 = wx.TextCtrl(parent=panel)
        self.tc20 = wx.TextCtrl(parent=panel)
        self.tc21 = wx.TextCtrl(parent=panel)

        # 定义横向布局器控件
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        hbox7 = wx.BoxSizer(wx.HORIZONTAL)
        hbox8 = wx.BoxSizer(wx.HORIZONTAL)
        hbox9 = wx.BoxSizer(wx.HORIZONTAL)
        hbox10 = wx.BoxSizer(wx.HORIZONTAL)
        hbox11 = wx.BoxSizer(wx.HORIZONTAL)
        hbox12 = wx.BoxSizer(wx.HORIZONTAL)
        hbox13 = wx.BoxSizer(wx.HORIZONTAL)
        hbox14 = wx.BoxSizer(wx.HORIZONTAL)
        hbox15 = wx.BoxSizer(wx.HORIZONTAL)
        hbox16 = wx.BoxSizer(wx.HORIZONTAL)
        hbox17 = wx.BoxSizer(wx.HORIZONTAL)
        hbox18 = wx.BoxSizer(wx.HORIZONTAL)
        hbox19 = wx.BoxSizer(wx.HORIZONTAL)
        hbox20 = wx.BoxSizer(wx.HORIZONTAL)
        hbox21 = wx.BoxSizer(wx.HORIZONTAL)
        hbox22 = wx.BoxSizer(wx.HORIZONTAL)
        hbox23 = wx.BoxSizer(wx.HORIZONTAL)

        # 添加静态文本控件
        hbox1.Add(statictext1, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox1.Add(self.tc1, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox2.Add(statictext2, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox2.Add(self.tc2, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox3.Add(statictext3, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox3.Add(self.tc3, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox4.Add(statictext4, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox4.Add(self.tc4, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox5.Add(statictext5, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox5.Add(self.tc5, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox6.Add(statictext6, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox6.Add(self.tc6, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox7.Add(statictext7, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox7.Add(self.tc7, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox8.Add(statictext8, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox8.Add(self.tc8, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox9.Add(statictext9, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox9.Add(self.tc9, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox10.Add(statictext10, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox10.Add(self.tc10, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox11.Add(statictext11, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox11.Add(self.tc11, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox12.Add(statictext12, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox12.Add(self.tc12, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox13.Add(statictext13, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox13.Add(self.tc13, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox14.Add(statictext14, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox14.Add(self.tc14, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox15.Add(statictext15, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox15.Add(self.tc15, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox16.Add(statictext16, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox16.Add(self.tc16, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox17.Add(statictext17, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox17.Add(self.tc17, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox18.Add(statictext18, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox18.Add(self.tc18, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox19.Add(statictext19, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox19.Add(self.tc19, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox20.Add(statictext20, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox20.Add(self.tc20, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox21.Add(statictext21, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox21.Add(self.tc21, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox22.Add(statictext22, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox22.Add(self.statictext23, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox23.Add(btn, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)

        # 定义纵向布局控件
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox1, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox2, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox3, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox4, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox5, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox6, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox7, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox8, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox9, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox10, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox11, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox12, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox13, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox14, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox15, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox16, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox17, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox18, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox19, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox20, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox21, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox22, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox23, proportion=1, flag=wx.CENTER | wx.FIXED_MINSIZE, border=5)
        panel.SetSizer(vbox)

    def on_click(self,event):
        oracle_dir = 'oracle_dir = ' + self.tc1.GetValue().strip() + '\n'
        oracle_tool = 'oracle_tool = ' + self.tc2.GetValue().strip() + '\n'
        data_dir = 'data_dir = ' + self.tc3.GetValue().strip() + '\n'
        archive_dir = 'archive_dir = ' + self.tc4.GetValue().strip() + '\n'
        oracle_base = 'oracle_base = ' + self.tc5.GetValue().strip() + '\n'
        oracle_home = 'oracle_home = ' + self.tc6.GetValue().strip() + '\n'
        oracle_pwd = 'oracle_pwd = ' + self.tc7.GetValue().strip() + '\n'
        oracle_sid = 'oracle_sid = ' + self.tc8.GetValue().strip() + '\n'
        nls_lang = 'nls_lang = ' + self.tc9.GetValue().strip() + '\n'
        sga_size = 'sga_size = ' + self.tc10.GetValue().strip() + '\n'
        ip = 'ip = ' + self.tc11.GetValue().strip() + '\n'
        hostname = 'hostname = ' + self.tc12.GetValue().strip() + '\n'
        dbsoft_dir = 'dbsoft_dir = ' + self.tc13.GetValue().strip() + '\n'
        root_pwd = 'root_pwd = ' + self.tc14.GetValue().strip() + '\n'
        db_zip_file = 'db_zip_file = ' + self.tc15.GetValue().strip() + '\n'
        sys_pwd = 'sys_pwd = ' + self.tc16.GetValue().strip() + '\n'
        system_pwd = 'system_pwd = ' + self.tc17.GetValue().strip() + '\n'
        db_total_mem = 'db_total_mem = ' + self.tc18.GetValue().strip() + '\n'
        lang = 'lang = ' + self.tc19.GetValue().strip() + '\n'
        opatch_name = 'opatch_name = ' + self.tc20.GetValue().strip() + '\n'
        patch_name = 'patch_name = ' + self.tc21.GetValue().strip() + '\n'
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
        base_dir = 'E:\\project\\dbmanage_v4\\common\\libs\\dbinstall\\'
        config_file = base_dir + 'setup.conf'
        try:
            with open(file=config_file,mode='w',encoding='utf-8') as f:
                f.writelines(config_list)
            self.statictext23.SetLabelText('配置文件生成成功！')
        except Exception as e:
            print('配置文件写入失败！')
            print('错误信息：{0}'.format(e))
