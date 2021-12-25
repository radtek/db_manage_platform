# -*- coding:utf-8 -*-

# 定义弹框
import wx
from oragridframe import OraGridFrame

class OraSprFrame(wx.Frame):
    def __init__(self,oper_type):
        super().__init__(parent=None,title='{0}'.format(oper_type),size=(400,200))
        self.Center()
        self.oper_type = oper_type
        # 定义面板控件
        panel = wx.Panel(parent=self)

        # 定义静态文本控件
        statictext1 = wx.StaticText(parent=panel,label='请选择ip：')
        statictext2 = wx.StaticText(parent=panel, label='请选择时间：')

        # 定义按钮控件
        btn = wx.Button(parent=panel,label='检查',id=1)
        # 按钮绑定监听方法
        self.Bind(wx.EVT_BUTTON,self.on_click,btn)

        # 定义下拉列表控件
        list1 = ['10.114.130.9','10.114.130.8','10.114.130.85_R','10.114.130.85_A']
        self.ch1 = wx.Choice(parent=panel,id=10,choices=list1)
        list2 = ['1小时','12小时','1天','15天','30天']
        self.ch2 = wx.Choice(parent=panel, id=11, choices=list2)
        # 下拉列表绑定监听
        self.Bind(wx.EVT_CHOICE, self.on_choice, id=10,id2=11)

        # 定义横向布局器控件
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        # 添加静态文本控件
        hbox1.Add(statictext1, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox1.Add(self.ch1, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox2.Add(statictext2, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox2.Add(self.ch2, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox3.Add(btn, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)

        # 定义纵向布局控件
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox1, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox2, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox3, proportion=1, flag=wx.CENTER | wx.FIXED_MINSIZE, border=5)

        panel.SetSizer(vbox)

    def on_choice(self,event):
        event_id = event.GetId()
        if event_id == 10:
            self.ch1_text = event.GetString()
        if event_id == 11:
            self.ch2_text = event.GetString()

    def on_click(self,event):
        ip = self.ch1_text.strip()
        time = self.ch2_text.strip()
        oper_type = self.oper_type.strip()
        app = wx.App()
        frame = OraGridFrame(oper_type,ip,time)
        frame.Show()
        app.MainLoop()