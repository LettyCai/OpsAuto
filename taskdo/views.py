from django.shortcuts import render

from django.views import View
from taskdo.ansible_call import AnsibleRunner,GetHostInfo
from taskdo import killttyp
import os
from django.conf import settings
from hostsinfo.models import HostsInfo,HostGroup
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from hostsinfo.utils import prpcrypt
import json



# Create your views here.
class TaskDoView(View):
    def post(self,request):
        pass

class KillTtypView(View):
    def get(self,request):
        result = {}
        return render(request,"kill-ttyp.html",{'result':result})

    def post(self,request):
        type = request.POST.get('type',"")
        ttyp = request.POST.get('ttyp',"")

        result,success_list,failed_list,unreachable_list,command = killttyp.kill_ttyp(type=type,ttyp=ttyp)

        #执行成功主机数
        success_num = len(success_list)
        #成功主机返回结果
        stdout_success = {}
        for host in success_list:
            stdout_success[host] = result['success'][host]['stdout']

        #z执行成功主机数
        failed_num = len(failed_list)
        #失败主机返回结果
        stdout_failed = {}
        for host in failed_list:
            stdout_failed[host] = result['failed'][host]['msg']

        #无法连接主机数
        unreachable_num = len(unreachable_list)


        return render(request,"kill-ttyp.html",{'result':result,
                                                'success_list':success_list,
                                                'success_num':success_num,
                                                'command':command,
                                                'stdout_success':stdout_success,
                                                'failed_list':failed_list,
                                                'failed_num':failed_num,
                                                'stdout_failed':stdout_failed,
                                                'unreachable_num':unreachable_num,
                                                'unreachable_list':unreachable_list})

class UploadView(View):
    def get(self,request):
        groups = HostGroup.objects.all()
        return render(request,"upload.html",{'groups':groups})

    def post(self,request):
        groups = HostGroup.objects.all()

        host_group = request.POST.get("hostgroup","")
        myfile = request.FILES.get("filename", None)
        user = request.POST.get("username","").strip()
        updir = request.POST.get("uploaddir","").strip()
        DIR = os.path.join(settings.BASE_DIR+"/tmp/",myfile.name)

        #将用户上传的文件保存到服务器
        if myfile :
            with open(DIR,'wb+') as destination:
                for chunk in myfile.chunks():
                    destination.write(chunk)
        if not myfile :
            return HttpResponse("no files for upload!")

        #获取要上传的主机
        gethost = GetHostInfo()
        inventory, variablemanager, host_list,loader = gethost.get_hosts(group_name=host_group)
        #上传文件参数
        args = "src="+DIR+" "+"dest="+updir+"/"+myfile.name +" "+"backup=yes"+" "+"force=yes"
        #上传文件模块
        model = 'copy'

        #指定以user用户上传
        if user != "":
            args = args + " " + "owner="+user

        #调用ansible模块执行命令
        ans = AnsibleRunner()
        result,success_list,failed_list,unreachable_list,command = ans.run_modle(inventory=inventory, loader=loader,host_list=host_list,
                               variable_manager=variablemanager, module_name=model, module_args=args)

        # 执行成功主机数
        success_num = len(success_list)
        # 成功主机返回结果
        stdout_success = {}
        for host in success_list:
            stdout_success[host] =  result['success'][host]


        # z执行成功主机数
        failed_num = len(failed_list)
        # 失败主机返回结果
        stdout_failed = {}
        for host in failed_list:
            stdout_failed[host] = result['failed'][host]['msg']

        # 无法连接主机数
        unreachable_num = len(unreachable_list)

        return render(request, "upload.html",{'result':result,
                                              'groups':groups,
                                              'success_list':success_list,
                                              'success_num':success_num,
                                              'command':command,
                                              'stdout_success':stdout_success,
                                              'failed_list':failed_list,
                                              'failed_num':failed_num,
                                              'unreachable_num':unreachable_num,
                                              'unreachable_list':unreachable_list})





class TaskDoView(View):
    def get(self,request):

        return render(request,"task-do.html")