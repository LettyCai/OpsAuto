from django.shortcuts import render,redirect
from django.views import View
import re
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin  #用户登录验证，用户权限验证
from django.http import JsonResponse,HttpResponse
from hostsinfo.models import HostsInfo,HostGroup
import  paramiko
from hostsinfo.utils import prpcrypt
from monitor.utils import ssh,getmsg
from monitor.models import HostStatus
# Create your views here.

class MonitorView(View):
    def test_func(self):
        """
        重载父类方法，实现系统管理员、运维人员角色的用户才能访问
        :return:
        """
        return self.request.user.role != 2

    def get(self,request,host_ip):
        hoststatus = HostStatus.objects.get(ip=host_ip)
        data = {"mem_use_data": hoststatus.mem_usage, "cpu_use_data": hoststatus.cpu_usage, "disk_use_data": hoststatus.disk_usage}
        data = getmsg(host_ip)
        return render(request,"monitor.html",{"data":data})

    def post(self,request):
        hostip = request.POST.get("hostip","")
        host = HostsInfo.objects.get(ip=hostip)
        has_host = HostStatus.objects.filter(ip=hostip)

        if has_host:
            hoststatus = HostStatus.objects.get(ip=hostip)
        else:
            hoststatus = HostStatus()

        data = getmsg(hostip)

        hoststatus.ip = hostip
        hoststatus.sys = host.mathine_type
        hoststatus.mem_usage = data["mem_use_data"]
        hoststatus.cpu_usage = data["cpu_use_data"]
        hoststatus.disk_usage = data["disk_use_data"]
        hoststatus.status = "正常"

        hoststatus.save()

        return JsonResponse(data, safe=False)


class MonitorListView(View):
    def test_func(self):
        """
        重载父类方法，实现系统管理员、运维人员角色的用户才能访问
        :return:
        """
        return self.request.user.role != 2

    def get(self,request):

        host_status = HostStatus.objects.all()
        return render(request,"monitor-list.html",{"host_status":host_status})


