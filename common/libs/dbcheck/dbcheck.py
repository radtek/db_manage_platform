# -*- coding:utf-8 -*-

# 数据库巡检功能窗口
import wx
from orasprframe import OraSprFrame
from dowload import DownLoad
import configparser
from logoper import Checklog
from logframe import LogFrame
from sqlserverimg import SqlserverImg
from imgframe import ImgFrame
from oswoper import OswOper
from genoswfile import GenOswFile
from hissprframe import HisSprFrame

class DbCheck(wx.Frame):
    def __init__(self):
        super().__init__(parent=None,title='数据库巡检工具',size=(800,600))
        self.Center()

        # 定义左右分隔窗口
        splitter = wx.SplitterWindow(parent=self,id=-1)
        leftpanel = wx.Panel(parent=splitter)
        rightpanel = wx.Panel(parent=splitter)
        splitter.SplitVertically(leftpanel,rightpanel,250)
        splitter.SetMinimumPaneSize(100)

        # 定义左窗口树形结构
        self.tree = self.CreateTreeCtrl(leftpanel)
        # 树形结构绑定监听函数
        self.Bind(wx.EVT_TREE_SEL_CHANGING,self.on_tree,self.tree)

        # 左窗口纵向布局器
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(self.tree,proportion=1,flag=wx.ALL | wx.EXPAND,border=5)
        leftpanel.SetSizer(vbox1)

        # 右窗口纵向布局器
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        self.content = wx.StaticText(parent=rightpanel, label='')
        vbox2.Add(self.content, proportion=1, flag=wx.ALL | wx.EXPAND, border=50)
        rightpanel.SetSizer(vbox2)


    # 树形结构监听函数
    def on_tree(self,event):
        item = event.GetItem()
        oper_type = self.tree.GetItemText(item).strip()
        oper_type_list = ['实例启动时间',
                          '表空间检查',
                          '更新对象检查',
                          '作业调度检查',
                          '备份检查',
                          '归档检查',
                          '性能检查'
                          ]
        if oper_type in oper_type_list:
            self.content.SetLabelText('启动{0}巡检窗口!'.format(oper_type))
            app = wx.App()
            frame = OraSprFrame(oper_type)
            frame.Show()
            app.MainLoop()
        if oper_type == '日志下载':
            self.content.SetLabelText('日志开始下载，请等待!')
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbcheck\\Setup.ini', encoding='utf-8')
            sec1 = config['monitor']
            obj = DownLoad(sec1['system_user'], sec1['system_pwd'], sec1['host'])
            result_list = obj.get_all_remote_log_filename()
            obj.get_all_remote_log_file(result_list)
            self.content.SetLabelText('日志下载完成!')
        if oper_type == '查看数据库日志报错':
            self.content.SetLabelText('启动{0}巡检窗口!'.format(oper_type))
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbcheck\\Setup.ini', encoding='utf-8')
            sec2 = config['base']
            alterlog_list, oslog_list = Checklog.logclassify(sec2['local_log_dir'])
            Checklog.dberror(alterlog_list)
            with open(file=sec2['local_db_log'], mode='r', encoding='gbk') as f:
                result = f.read()
            app = wx.App()
            frame = LogFrame(oper_type,result)
            frame.Show()
            app.MainLoop()
        if oper_type == '查看系统日志报错':
            self.content.SetLabelText('启动{0}巡检窗口!'.format(oper_type))
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbcheck\\Setup.ini', encoding='utf-8')
            sec2 = config['base']
            alterlog_list, oslog_list = Checklog.logclassify(sec2['local_log_dir'])
            Checklog.oserror(oslog_list)
            with open(file=sec2['local_os_log'], mode='r', encoding='gbk') as f:
                result = f.read()
            app = wx.App()
            frame = LogFrame(oper_type, result)
            frame.Show()
            app.MainLoop()
        if oper_type == '巡检结果':
            self.content.SetLabelText('正在生成sqlserver巡检图片...')
            SqlserverImg.gen_sqlserver_img()
            self.content.SetLabelText('启动{0}巡检窗口!'.format(oper_type))
            app = wx.App()
            frame = ImgFrame(oper_type)
            frame.Show()
            app.MainLoop()
        if oper_type == 'osw压缩下载':
            config = configparser.ConfigParser()
            config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbcheck\\Setup.ini', encoding='utf-8')
            sec2 = config['monitor']
            self.content.SetLabelText('正在压缩和下载oswatch文件...')
            out_name = OswOper.create_all_osw_zip_file(username=sec2['system_user'], password=sec2['system_pwd'], hostname=sec2['host'])
            OswOper.get_remote_osw_zip_file(host_ip=sec2['host'], username=sec2['system_user'], password=sec2['system_pwd'],out_name=out_name)
            self.content.SetLabelText('oswatch文件已经压缩和下载！')
        if oper_type == 'osw解压':
            self.content.SetLabelText('正在解压oswatch文件...')
            ip_list = ['xxx', 'xxx', 'xxx','xxx']
            OswOper.unzip_local_osw_file(ip_list)
            self.content.SetLabelText(r'oswatch压缩文件已经解压完成！')
        if oper_type == 'osw文件生成':
            self.content.SetLabelText('正在远程生成oswatch文件...')
            ip_list = ['xxx', 'xxx', 'xxx', 'xxx']
            for i in ip_list:
                GenOswFile.gen_osw_file(i)
                print('{0}节点oswatch文件已经生成！'.format(i))
            self.content.SetLabelText('oswatch文件已经生成！')
        if oper_type == '表空间报表':
            self.content.SetLabelText('启动{0}巡检窗口!'.format(oper_type))
            app = wx.App()
            frame = HisSprFrame(oper_type)
            frame.Show()
            app.MainLoop()
        if oper_type == 'aas报表':
            self.content.SetLabelText('启动{0}巡检窗口!'.format(oper_type))
            app = wx.App()
            frame = HisSprFrame(oper_type)
            frame.Show()
            app.MainLoop()

    # 树形结构构造方法
    def CreateTreeCtrl(self,parent):
        tree = wx.TreeCtrl(parent)
        imglist = wx.ImageList(16,16,True,2)
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,size=wx.Size(16,16)))
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, size=wx.Size(16, 16)))
        tree.AssignImageList(imglist)
        root = tree.AddRoot('数据库巡检工具',image=0)
        item1 = []
        item1.append(tree.AppendItem(root,'oracle巡检',0))
        for i in range(len(item1)):
            id = item1[i]
            tree.AppendItem(id,'实例启动时间',1)
            tree.AppendItem(id, '表空间检查', 1)
            tree.AppendItem(id, '更新对象检查', 1)
            tree.AppendItem(id, '作业调度检查', 1)
            tree.AppendItem(id, '备份检查', 1)
            tree.AppendItem(id, '归档检查', 1)
            tree.AppendItem(id, '性能检查', 1)
        item2 = []
        item2.append(tree.AppendItem(root, 'sqlserver巡检', 0))
        for i in range(len(item2)):
            id = item2[i]
            tree.AppendItem(id,'巡检结果',1)
        item3 = []
        item3.append(tree.AppendItem(root, '告警日志巡检', 0))
        for i in range(len(item3)):
            id = item3[i]
            tree.AppendItem(id, '日志下载', 1)
            tree.AppendItem(id, '查看数据库日志报错', 1)
            tree.AppendItem(id, '查看系统日志报错', 1)
        item4 = []
        item4.append(tree.AppendItem(root, 'oswatch巡检', 0))
        for i in range(len(item4)):
            id = item4[i]
            tree.AppendItem(id, 'osw文件生成', 1)
            tree.AppendItem(id, 'osw压缩下载', 1)
            tree.AppendItem(id, 'osw解压', 1)
        item5 = []
        item5.append(tree.AppendItem(root, '历史数据报表', 0))
        for i in range(len(item5)):
            id = item5[i]
            tree.AppendItem(id, '表空间报表', 1)
            tree.AppendItem(id, 'aas报表', 1)
        tree.Expand(root)
        tree.Expand(item1[0])
        tree.Expand(item2[0])
        tree.Expand(item3[0])
        tree.Expand(item4[0])
        tree.Expand(item5[0])
        tree.SelectItem(root)
        return tree

# 数据库巡检功能程序
class DbCheckApp(wx.App):
    def OnInit(self):
        frame = DbCheck()
        frame.Show()
        return True

    def OnExit(self):
        print('数据库巡检程序退出')
        return 0

if __name__ == '__main__':
    app = DbCheckApp()
    app.MainLoop()
