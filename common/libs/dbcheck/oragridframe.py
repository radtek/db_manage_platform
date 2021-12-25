# -*- coding:utf-8 -*-

import wx
import wx.grid
from dboper import DbOper
import configparser

class OraGridFrame(wx.Frame):
    def __init__(self,oper_type,ip,time):
        super().__init__(parent=None,title='{0}节点{1}'.format(ip,oper_type),size=(1000,600))
        self.Center()
        self.oper_type = oper_type
        self.ip = ip
        self.time = time

        # 定义网格控件
        self.grid = self.CreateGrid(self)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick, self.grid)

    # 定义网格控件出发函数
    def OnLabelLeftClick(self, event):
        print('RowIdx：{0}'.format(event.GetRow()))
        print('ColIdx：{0}'.format(event.GetCol()))
        # 确保能继续处理其他的事件
        event.Skip()

    def CreateGrid(self,parent):
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbcheck\\Setup.ini', encoding='utf-8')
        sec1 = config['monitor']
        obj = DbOper(sec1['user'], sec1['pwd'], sec1['host'], sec1['port'], sec1['sid'])
        if self.time.strip() == '1小时':
            self.time = '1/24'
        if self.time.strip() == '12小时':
            self.time = '1/2'
        if self.time.strip() == '1天':
            self.time = '1'
        if self.time.strip() == '15天':
            self.time = '15'
        if self.time.strip() == '30天':
            self.time = '30'

        # 定义列
        starttime_column = ['IP','INSTANCE_NAME','STARTTUP_TIME','GETTIME']
        tbs_column = ['IP','TABLESPACE_NAME','TOTAL_MB','FREE_MB','USED_MB','FREE_RATIO','USED_RATIO','GETTIME']
        upobj_column = ['IP','更新对象个数']
        job_column = ['IP','LOG_DATE','OWNER','JOB_NAME','STATUS','ERROR#','RUN_DURATION','CPU_USED','ADDITIONAL_INFO','GETTIME']
        bak_column = ['IP','STARTTIME','ENDTIME','STATUS']
        arch_column = ['IP','归档信息','GETTIME']
        perform_column = ['IP','HIT','GETTIME']

        # 数据库实例启动时间sql
        starttime_sql = '''
        select a.* from table_startup a,server_order b 
        where a.gettime>=sysdate-%s 
        and a.ip=b.ip 
        and a.ip = '%s'
        ''' % (self.time,self.ip)

        # 数据库表空间使用率sql
        tbs_sql = '''
         select a.* 
         from tablespace_size_new a,server_order b 
         where a.gettime>=sysdate-%s
         and a.ip=b.ip 
         and a.ip = '%s'
         order by a.used_ratio
        ''' % (self.time,self.ip)

        # 数据库更新对象sql
        upobj_sql = '''
        select a.ip,'更新'||a.count_tab||'个对象' 
        from count_tab a,server_order b 
        where a.ip=b.ip and a.gettime>=sysdate-%s 
        and a.ip = '%s'
        ''' % (self.time,self.ip)

        # 数据库job检查sql
        job_sql = '''
                select a.* from 
                mon_scheduler_job a,server_order b 
                where a.ip=b.ip and a.gettime>=sysdate-%s
                and a.ip='%s'
               ''' % (self.time, self.ip)

        # 数据库备份检查sql
        bak_sql = '''
                SELECT a.ip,a.START_TIME,to_char(a.END_TIME,'yyyy-mm-dd hh24:mi:ss'),a.STATUS 
                FROM backup_status a,server_order b 
                WHERE a.ip=b.ip and a.gettime>sysdate-%s 
                and to_char(start_time,'YYYY-MM-DD HH24:MI:SS')>= to_char(sysdate-15/24,'YYYY-MM-DD HH24:MI:SS')
                and a.ip='%s'
        ''' % (self.time, self.ip)

        # 数据库归档查询sql
        arch_sql = '''
            SELECT a.* 
            FROM archive_log a,server_order b 
            WHERE  a.ip=b.ip and a.gettime>sysdate-%s 
            and A like '最近一次归档%s' and a.ip='%s'
        ''' % (self.time,'%',self.ip)

        # 数据库性能查询sql
        perform_sql = '''
        select a.* from hit_table a ,server_order b ,hit_order c 
        WHERE  a.ip=b.ip and a.gettime>sysdate-%s and substr(a.hit,1,7)=substr(c.name,1,7) 
        and a.ip = '%s'
        ''' % (self.time,self.ip)

        # 构建grid网格
        grid = wx.grid.Grid(parent)
        if self.oper_type == '实例启动时间':
            data = obj.dboper(starttime_sql)
            if len(data) != 0:
                grid.CreateGrid(len(data),len(data[0]))
                for row in range(len(data)):
                    for col in range(len(data[row])):
                        grid.SetColLabelValue(col,starttime_column[col])
                        grid.SetCellValue(row,col,str(data[row][col]))
        if self.oper_type == '表空间检查':
            data = obj.dboper(tbs_sql)
            if len(data) != 0:
                grid.CreateGrid(len(data),len(data[0]))
                for row in range(len(data)):
                    for col in range(len(data[row])):
                        grid.SetColLabelValue(col,tbs_column[col])
                        grid.SetCellValue(row,col,str(data[row][col]))
        if self.oper_type == '更新对象检查':
            data = obj.dboper(upobj_sql)
            if len(data) != 0:
                grid.CreateGrid(len(data),len(data[0]))
                for row in range(len(data)):
                    for col in range(len(data[row])):
                        grid.SetColLabelValue(col,upobj_column[col])
                        grid.SetCellValue(row,col,str(data[row][col]))
        if self.oper_type == '作业调度检查':
            data = obj.dboper(job_sql)
            if len(data) != 0:
                grid.CreateGrid(len(data),len(data[0]))
                for row in range(len(data)):
                    for col in range(len(data[row])):
                        grid.SetColLabelValue(col,job_column[col])
                        grid.SetCellValue(row,col,str(data[row][col]))
        if self.oper_type == '备份检查':
            data = obj.dboper(bak_sql)
            if len(data) != 0:
                grid.CreateGrid(len(data),len(data[0]))
                for row in range(len(data)):
                    for col in range(len(data[row])):
                        grid.SetColLabelValue(col,bak_column[col])
                        grid.SetCellValue(row,col,str(data[row][col]))
        if self.oper_type == '归档检查':
            data = obj.dboper(arch_sql)
            if len(data) != 0:
                grid.CreateGrid(len(data),len(data[0]))
                for row in range(len(data)):
                    for col in range(len(data[row])):
                        grid.SetColLabelValue(col,arch_column[col])
                        grid.SetCellValue(row,col,str(data[row][col]))
        if self.oper_type == '性能检查':
            data = obj.dboper(perform_sql)
            if len(data) != 0:
                grid.CreateGrid(len(data),len(data[0]))
                for row in range(len(data)):
                    for col in range(len(data[row])):
                        grid.SetColLabelValue(col,perform_column[col])
                        grid.SetCellValue(row,col,str(data[row][col]))
        grid.AutoSize()
        return grid

