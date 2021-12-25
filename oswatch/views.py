# -*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse
from common.libs.oswatch import create_all_osw_zip_file,get_remote_osw_zip_file,unzip_local_osw_file,osw_snapshot,gen_osw_img
from login import models
from common.libs.Helper import ops_renderJSON,ops_renderErrJSON
from common.libs.log import DownLoad,Checklog
from django.db.models import Q
from common.libs.drawpicture import DataParse

log_path = r"E:\daily_data\log"

# Create your views here.
def oswatch(request):
    if request.method == 'GET':
        username = request.GET.get('username', None)
        real_db_info = models.RealDblist.objects.filter(~Q(ip="xxx"))
        return render(request, 'oswatch/oswatch.html', context={'username': username,'real_db_info':real_db_info})
    if request.method == 'POST':
        ip1 = request.POST.get('ip',None)
        btn_name = request.POST.get('btn_name')
        if ip1 is not None:
            if btn_name == 'btn_name_1':
                out_name = create_all_osw_zip_file(username='xxx', password='xxx', hostname='xxx',ip=ip1)
                get_remote_osw_zip_file(host_ip='xxx', username='xxx', password='xxx', out_name=out_name,ip=ip1)
                unzip_local_osw_file(ip1)
                result = ops_renderJSON(msg='下载成功！',data=ip1)
                return HttpResponse(result)
            if btn_name == 'btn_name_8':
                gen_osw_img(ip1)
                result = ops_renderJSON(msg='查看成功！',data=ip1)
                return HttpResponse(result)
        result = ops_renderErrJSON(msg='请选择IP地址！')
        return HttpResponse(result)

def mon_pic(request):
    if request.method == 'GET':
        username = request.GET.get('username', None)
        db_info = models.Dblist.objects.all()
        return render(request, 'oswatch/mon_pic.html', context={'username': username, 'db_info': db_info})
    if request.method == 'POST':
        ip3 = request.POST.get('ip3', None)
        type = request.POST.get('type3', None)
        time = request.POST.get('time3', None)
        if time is not None:
            time = time.strip('天')
        if ip3 is not None and type is not None and time is not None:
            DataParse.tbs_parse(ip3, type, time)
            result = ops_renderJSON(msg='表空间报表生成！')
            return HttpResponse(result)
        ip4 = request.POST.get('ip4', None)
        time = request.POST.get('time4', None)
        if time is not None:
            time = time.strip('天')
        if ip4 is not None and time is not None:
            DataParse.aas_parse(ip4, time)
            result = ops_renderJSON(msg='AAS报表生成！')
            return HttpResponse(result)
        result = ops_renderErrJSON(msg='请把选项都选全！')
        return HttpResponse(result)

def log_oper(request):
    if request.method == 'GET':
        username = request.GET.get('username', None)
        real_db_info = models.RealDblist.objects.filter(~Q(ip="xxx"))
        return render(request, 'oswatch/log_oper.html', context={'username': username, 'real_db_info': real_db_info})
    if request.method == 'POST':
        ip2 = request.POST.get('ip2', None)
        btn_name2 = request.POST.get('btn_name2')
        if ip2 is not None:
            if btn_name2 == 'btn_name_2':
                obj = DownLoad('oracle', 'oracle', 'xxx')
                name = obj.get_all_remote_log_filename(ip2, 'alter')
                obj.get_all_remote_log_file(name)
                result = ops_renderJSON(msg='alert日志下载成功！')
                return HttpResponse(result)
            if btn_name2 == 'btn_name_3':
                alterlog_list, _ = Checklog.logclassify(log_path)
                content_list = Checklog.dberror(alterlog_list, ip2)
                result = ops_renderJSON(msg='alert日志查看成功！', data=content_list)
                return HttpResponse(result)
            if btn_name2 == 'btn_name_4':
                obj = DownLoad('oracle', 'oracle', 'xxx')
                name = obj.get_all_remote_log_filename(ip2, 'oslog')
                obj.get_all_remote_log_file(name)
                result = ops_renderJSON(msg='os日志下载成功！')
                return HttpResponse(result)
            if btn_name2 == 'btn_name_5':
                _, oslog_list = Checklog.logclassify(log_path)
                content_list = Checklog.oserror(oslog_list, ip2)
                result = ops_renderJSON(msg='os日志查看成功！', data=content_list)
                return HttpResponse(result)
        result = ops_renderErrJSON(msg='请选择IP地址！')
        return HttpResponse(result)
