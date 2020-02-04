from django.shortcuts import render,redirect
from django.views import View
import re
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin  #用户登录验证，用户权限验证
from django.http import JsonResponse,HttpResponse
from hostsinfo.models import HostsInfo,HostGroup
# Create your views here.

class MonitorView(View):
    def test_func(self):
        """
        重载父类方法，实现系统管理员、运维人员角色的用户才能访问
        :return:
        """
        return self.request.user.role != 2

    def get(self,request):
        groups = HostGroup.objects.all()
        return render(request,"monitor.html",{"groups":groups})