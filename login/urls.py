# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='/'),
    path('login/', views.login, name='login'),
    path('reg/', views.reg, name='reg'),
]