# -*- coding: utf-8 -*-

# Create your views here.
from django.shortcuts import render,HttpResponse
from login import models
from common.libs.GetData import get_startuptime_data,get_tbs_used_data,get_update_obj_data,get_scheduler_job_data,get_dbbackup_data,get_archlog_data,get_db_perform_data
from common.libs.oswatch import gen_sqlserver_img
from common.libs.Helper import ops_renderJSON,ops_renderErrJSON

def dbcheck(request):
    if request.method == 'GET':
        username = request.GET.get('username', None)
        db_info = models.Dblist.objects.all()
        type = request.GET.get('type', None)
        tag = 0
        if type == 'startup_time':
            tag = 1
        if type == 'tbs_used':
            tag = 2
        if type == 'update_object':
            tag = 3
        if type == 'job_scheduler':
            tag = 4
        if type == 'db_backup':
            tag = 5
        if type == 'db_archive':
            tag = 6
        if type == 'param_info':
            tag = 7
        return render(request,'dbcheck/dbcheck.html',context={'username': username,'db_info':db_info,'tag':tag})
    if request.method == 'POST':
        # 查看数据库监控指标
        username = request.GET.get('username', None)
        type = request.GET.get('type', None)
        db_info = models.Dblist.objects.all()
        ip = request.POST.get('ip',None)
        time = request.POST.get('time',None)
        if ip is not None and type is not None and time is not None:
            time = time.strip('天')
            result = []
            if type == 'startup_time':
                result = get_startuptime_data(ip,time)
            if type == 'tbs_used':
                result = get_tbs_used_data(ip, time)
            if type == 'update_object':
                result = get_update_obj_data(ip, time)
            if type == 'job_scheduler':
                result = get_scheduler_job_data(ip, time)
            if type == 'db_backup':
                result = get_dbbackup_data(ip, time)
            if type == 'db_archive':
                result = get_archlog_data(ip, time)
            if type == 'param_info':
                result = get_db_perform_data(ip, time)
            return render(request, 'dbcheck/dbcheck.html', context={'username': username, 'result': result, 'type': type,'db_info': db_info})
        else:
            return render(request, 'dbcheck/dbcheck.html',context={'username': username,'db_info': db_info})

def sqlserver_check(request):
    if request.method == 'GET':
        username = request.GET.get('username',None)
        return render(request,'dbcheck/sqlservercheck.html',context={'username':username})
    if request.method == 'POST':
        gen_sqlserver_img()
        result = ops_renderJSON(msg='操作成功！')
        return HttpResponse(result)

