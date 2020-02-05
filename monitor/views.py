from django.shortcuts import render,redirect
from django.views import View
import re
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin  #用户登录验证，用户权限验证
from django.http import JsonResponse,HttpResponse
from hostsinfo.models import HostsInfo,HostGroup
import  paramiko
from hostsinfo.utils import prpcrypt
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

    def post(self,request):
        hostip = request.POST.get("hostip","")
        host = HostsInfo.objects.get(ip=hostip)
        password = host.ssh_passwd
        pc = prpcrypt()
        password = pc.decrypt(password).decode(encoding='UTF-8', errors='strict')
        result = []


        try:
            a2 = "parted -l  | grep   \"Disk \/dev\/[a-z]d\"  | awk -F\"[ ]\"  '{print $3}' | awk  -F\"GB\"  '{print $1}'"
            s = ssh(ip=hostip,password=password, cmd=a2)
            disk1 = s['data']
            disk2 = disk1.rstrip().split("\n")
            disk = "+".join(map(str, disk2)) #+ "   共计:{} GB".format(round(sum(map(float, disk2))))
            result.append({"total_disk": disk})
        except Exception  as  e:
            result.append({"msg":e})


        try:
            a1 = "top -b -n 1 | grep Cpu | awk -F\"[ ]\"  '{print $3}' "
            s = ssh(ip=hostip,password=password, cmd=a1)
            cpu_use = s['data']
            #cpu_use_data = int(int(cpu_use)*100)
            cpu_use_data = cpu_use
            print(cpu_use_data)
            result.append({"cpu_use":cpu_use_data})
        except Exception as e:
            result.append({"msg2": e})

        try:
            a3 = "free | grep Mem | awk '{print $2}' "
            s = ssh(ip=hostip, password=password, cmd=a3)
            mem_total = s['data']
            a4 = "free | grep Mem | awk '{print $3}' "
            s = ssh(ip=hostip, password=password, cmd=a4)
            mem_use = s['data']
            mem_use_data = int(int(mem_use)/int(mem_total)*100)
            result.append({"mem_use": mem_use_data})


        except Exception as e:
            result.append({"msg2": e})

        return render(request, "monitor.html", {"result": result})

        #return JsonResponse(result, safe=False)



def ssh(ip, password, cmd):
    try:
        ssh = paramiko.SSHClient()  # 创建ssh对象
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, port=22, username="root", password=password, )
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)

        result = stdout.read()
        result1 = result.decode()
        error = stderr.read().decode('utf-8')

        if not error:
            ret = {"ip": ip, "data": result1}
            ssh.close()
            return ret
    except Exception as e:
        error = "账号或密码错误,{}".format(e)
        ret = {"ip": ip, "data": error}
        return ret
