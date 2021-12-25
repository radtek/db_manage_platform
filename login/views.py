# -*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse
from common.libs.Helper import ops_renderErrJSON,ops_renderJSON
from common.libs.UserService import UserService
from common.libs.DataHelper import getCurrentTime
from . import models

# Create your views here.
def index(request):
    return render(request,'login/index.html')

def login(request):
    if request.method == "GET":
        return render(request,'login/login.html')

    if request.method == 'POST':
        login_name = request.POST.get('login_name', None)
        login_pwd = request.POST.get('login_pwd', None)
        if login_name is None or len(login_name) < 1:
            result = ops_renderErrJSON("请输入正确的登录用户名~~")
            return HttpResponse(result)

        if login_pwd is None or len(login_pwd) < 6:
            result = ops_renderErrJSON("请输入正确的登录密码~~")
            return HttpResponse(result)

        user_info = models.User.objects.filter(login_name=login_name)
        if user_info.values()[0]['status'] != 1:
            result = ops_renderErrJSON("账号被禁用，请联系管理员处理~~")
            return HttpResponse(result)

        if not user_info:
            result = ops_renderErrJSON("请输入正确的登录用户名和密码 -1~~")
            return HttpResponse(result)

        if user_info.values()[0]['login_pwd'] != UserService.genePwd(login_pwd, user_info.values()[0]['login_salt']):
            result = ops_renderErrJSON("请输入正确的登录用户名和密码 -2 ~~")
            return HttpResponse(result)

        result = ops_renderJSON( msg="登录成功~~" )
        return HttpResponse(result)

def reg(request):
    if request.method == "GET":
        return render(request, 'login/reg.html')

    nickname = request.POST.get('nickname',None)
    login_name = request.POST.get('login_name',None)
    login_pwd = request.POST.get('login_pwd',None)
    login_pwd2 = request.POST.get('login_pwd2',None)

    if login_name is None or len( login_name ) < 1:
        result = ops_renderErrJSON( msg = "请输入正确的登录用户名~~" )
        return HttpResponse(result)

    if login_pwd is None or len( login_pwd ) < 6:
        result = ops_renderErrJSON( msg ="请输入正确的登录密码，并且不能小于6个字符~~")
        return HttpResponse(result)

    if login_pwd != login_pwd2:
        result = ops_renderErrJSON(msg="请输入正确的确认登录密码~~")
        return HttpResponse(result)

    user_info = models.User.objects.filter(login_name=login_name)
    if user_info:
        result = ops_renderErrJSON( msg="登录用户名已被注册，请换一个~~")
        return HttpResponse(result)

    salt = UserService.geneSalt(8)
    pwd = UserService.genePwd(login_pwd,salt)
    current_user = models.User(login_name=login_name,
                               nickname=nickname,
                               login_salt=salt,
                               login_pwd=pwd,
                               created_time=getCurrentTime(),
                               updated_time=getCurrentTime())
    current_user.save()

    result = ops_renderJSON( msg = "注册成功~~" )
    return HttpResponse(result)