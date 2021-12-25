# -*- coding:utf-8 -*-

from dataparse import DataParse

# 定义弹框
import wx

class HisSprFrame(wx.Frame):
    def __init__(self,oper_type):
        super().__init__(parent=None,title='{0}'.format(oper_type),size=(400,200))
        self.Center()
        self.oper_type = oper_type
        # 定义面板控件
        panel = wx.Panel(parent=self)

        # 定义静态文本控件
        statictext1 = wx.StaticText(parent=panel,label='请选择ip：')
        if self.oper_type == '表空间报表':
            statictext2 = wx.StaticText(parent=panel, label='请选择表空间：')
        statictext3 = wx.StaticText(parent=panel, label='请选择时间：')

        # 定义按钮控件
        btn = wx.Button(parent=panel,label='确认',id=1)
        # 按钮绑定监听方法
        self.Bind(wx.EVT_BUTTON,self.on_click,btn)

        # 定义下拉列表控件
        list1 = ['xxx','xxx']
        self.ch1 = wx.Choice(parent=panel,id=10,choices=list1)
        if self.oper_type == '表空间报表':
            list2 = ['TABLESPACESUPPORT','TABLESPACEINDEX','AUDITTBS','TABLESPACEHIST','TABLESPACEMES']
            self.ch2 = wx.Choice(parent=panel, id=11, choices=list2)
        list3 = ['7天','15天','30天']
        self.ch3 = wx.Choice(parent=panel, id=12, choices=list3)
        # 下拉列表绑定监听
        self.Bind(wx.EVT_CHOICE, self.on_choice, id=10,id2=12)

        # 定义横向布局器控件
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        if self.oper_type == '表空间报表':
            hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)

        # 添加静态文本控件
        hbox1.Add(statictext1, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox1.Add(self.ch1, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        if self.oper_type == '表空间报表':
            hbox2.Add(statictext2, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
            hbox2.Add(self.ch2, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox3.Add(statictext3, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hbox3.Add(self.ch3, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)
        hbox4.Add(btn, proportion=1, flag=wx.ALL | wx.FIXED_MINSIZE)

        # 定义纵向布局控件
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox1, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        if self.oper_type == '表空间报表':
            vbox.Add(hbox2, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox3, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox4, proportion=1, flag=wx.CENTER | wx.FIXED_MINSIZE, border=5)

        panel.SetSizer(vbox)

    def on_choice(self,event):
        event_id = event.GetId()
        if event_id == 10:
            self.ch1_text = event.GetString()
        if self.oper_type == '表空间报表':
            if event_id == 11:
                self.ch2_text = event.GetString()
        if event_id == 12:
            self.ch3_text = event.GetString()

    def on_click(self,event):
        ip = self.ch1_text.strip()
        if self.oper_type == '表空间报表':
            tbs = self.ch2_text.strip()
        time = self.ch3_text.strip()
        oper_type = self.oper_type.strip()
        if time == '7天':
            time = '7'
        if time == '15天':
            time = '15'
        if time == '30天':
            time = '30'
        if oper_type == '表空间报表':
            DataParse.tbs_parse(ip,tbs,time)
        if oper_type == 'aas报表':
            DataParse.aas_parse(ip,time)
