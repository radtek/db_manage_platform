# -*- coding:utf-8 -*-

import wx

class InsFrame(wx.Frame):
    def __init__(self,oper_type,result):
        super().__init__(parent=None,title='{0}'.format(oper_type),size=(1000,800))
        self.Center()
        self.oper_type = oper_type
        self.result = result

        # 创建面板
        panel = wx.Panel(parent=self)

        # 定义多行文本控件
        tc = wx.TextCtrl(parent=panel, style=wx.TE_MULTILINE)
        tc.SetValue(self.result)

        # 定义纵向布局器
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(tc,proportion=1,flag=wx.EXPAND)

        panel.SetSizer(vbox)
