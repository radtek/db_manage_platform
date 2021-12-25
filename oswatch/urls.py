# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('', views.oswatch, name='oswatch'),
    path('mon_pic', views.mon_pic, name='mon_pic'),
    path('log_oper', views.log_oper, name='log_oper')
]