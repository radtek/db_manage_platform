# -*- coding:utf-8 -*-

import wx
import os
import configparser

class ImgFrame(wx.Frame):
    def __init__(self,oper_type):
        super().__init__(parent=None,title='启动{0}窗口！'.format(oper_type),size=(1400,800))
        self.Center()

        # 创建面板
        panel = wx.Panel(parent=self)

        # 创建静态图片空间
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbcheck\\Setup.ini', encoding='utf-8')
        sec2 = config['base']
        if not os.path.exists(sec2['base_dir'] + 'sqlserver_img\\sqlserver.img'):
            bmps = [
                wx.Bitmap('sqlserver_img//sqlserver.jpg',wx.BITMAP_TYPE_ANY)
            ]
            image = wx.StaticBitmap(parent=panel,id=-1,bitmap=bmps[0])

            # 创建纵向布局器
            vbox = wx.BoxSizer(wx.VERTICAL)
            vbox.Add(image,proportion=1,flag=wx.Center| wx.FIXED_MINSIZE,border=20)

            panel.SetSizer(vbox)
