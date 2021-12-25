# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('',views.dbcheck,name='dbcheck'),
    path('sqlservercheck',views.sqlserver_check,name='sqlservercheck')
]