# -*- coding: utf-8 -*-

from django.shortcuts import render
from login import models

# Create your views here.
def db_list(request):
    if request.method == 'GET':
        username = request.GET.get('username', None)
        real_db_info = models.RealDblist.objects.all()
        return render(request,'db/dblist.html',context={'username':username,'real_db_info':real_db_info})
