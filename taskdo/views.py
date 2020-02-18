from django.shortcuts import render
from django.views import View
from taskdo.ansible_call import AnsibleRunner,GetHostInfo
from taskdo import killttyp
import os
from django.conf import settings
from hostsinfo.models import HostsInfo,HostGroup,GroupUsers
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from hostsinfo.utils import prpcrypt
import json
from .models import OpsLog,Scripts
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin  #用户登录验证，用户权限验证
from django.http import JsonResponse,HttpResponse
#from django.core import serializers
from .utils import savelog
from OpsAuto.settings import BASE_DIR


# Create your views here.


class KillTtypView(LoginRequiredMixin,View):
    """
    清理终端号
    """
    def get(self,request):
        result = {}
        return render(request,"kill-ttyp.html",{'result':result})

    def post(self,request):
        type = request.POST.get('type',"")
        ttyp = request.POST.get('ttyp',"")
        user = request.user.username

        result,success_list,failed_list,unreachable_list,command = killttyp.kill_ttyp(type=type,ttyp=ttyp)

        #执行成功主机数
        success_num = len(success_list)
        #成功主机返回结果
        stdout_success = {}
        for host in success_list:
            savelog(user, command, host, 'success', result['success'][host])
            stdout_success[host] = result['success'][host]['stdout']

        #z执行成功主机数
        failed_num = len(failed_list)
        #失败主机返回结果
        stdout_failed = {}
        for host in failed_list:
            # 保存操作日志
            savelog(user, command, host, 'failed', result['failed'][host])
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


class UploadView(UserPassesTestMixin,View):
    """
    上传文件
    """
    def test_func(self):
        """
        重载父类方法，实现系统管理员、运维人员角色的用户才能访问
        :return:
        """
        return self.request.user.role != 2

    def get(self,request):
        groups = HostGroup.objects.all()
        return render(request,"upload.html",{'groups':groups})

    def post(self,request):
        groups = HostGroup.objects.all()

        host_group = request.POST.get("group","")
        myfile = request.FILES.get("filename", None)
        username = request.POST.get("users","").strip()
        updir = request.POST.get("uploaddir","").strip()
        DIR = os.path.join(settings.BASE_DIR+"/tmp/",myfile.name)

        user = HostUsers.objects.filter(username=username).first()

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

        #指定文件所属用户及用户组
        if user != "":
            args = args + " " + "owner=" + user.username + " " + "group=" + user.usergroup

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


        # 执行成功主机数
        failed_num = len(failed_list)
        # 失败主机返回结果
        stdout_failed = {}
        for host in failed_list:
            stdout_failed[host] = result['failed'][host]['msg']

        # 无法连接主机数
        unreachable_num = len(unreachable_list)

        print(stdout_failed)

        return render(request, "upload.html",{'result':result,
                                              'groups':groups,
                                              'success_list':success_list,
                                              'success_num':success_num,
                                              'command':command,
                                              'stdout_success':stdout_success,
                                              'failed_list':failed_list,
                                              'failed_num':failed_num,
                                              'unreachable_num':unreachable_num,
                                              'unreachable_list':unreachable_list,
                                              'stdout_failed':stdout_failed})


class TaskDoView(UserPassesTestMixin,View):
    """
    执行ad-hoc命令
    """
    def test_func(self):
        """
        重载父类方法，实现系统管理员、运维人员角色的用户才能访问
        :return:
        """
        return self.request.user.role != 2

    def get(self,request):
        groups = HostGroup.objects.all()
        #return render(request,"task-do.html",{'groups':groups})
        return render(request, "task-do-ajax.html", {'groups': groups})


class FindLogView(LoginRequiredMixin,View):
    """
    查看日志列表
    """
    def get(self,request):

        logs = OpsLog.objects.all().order_by('-date')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(logs, 10, request=request)
        logs = p.page(page)

        return render(request,"logs.html",{'logs':logs})

class LogDetailsView(LoginRequiredMixin,View):
    """
    查看日志详细信息
    """
    def get(self,request,log_id):
        log = OpsLog.objects.get(id=int(log_id)).details

        return render(request,"logdetails.html",{'log':log})

def gethost(request):
    """
    执行ad-hoc命令页面，获取主机组所有主机
    :param request:
    :return:
    """
    if request.method == "GET":
        sendgroupname = request.GET.get("sendgroupname")
        if sendgroupname:
            groups = HostGroup.objects.get(group_name=str(sendgroupname))
            hosts = groups.hostsinfo_set.all().values("ip")
            data=list(hosts)
            return JsonResponse(data, safe=False)

def getusers(request):
    """
        获取主机组的所有用户
        :param request:
        :return:
        """
    if request.method == "GET":
        sendgroupname = request.GET.get("sendgroupname")
        if sendgroupname:
            group = HostGroup.objects.get(group_name=sendgroupname)
            users = GroupUsers.objects.filter(hostgroup__id=group.id).values("username")
            data = list(users)
            return JsonResponse(data, safe=False)


def getajaxtask(request):
    """
    AJAX执行ad-hoc命令
    :param request:
    :return:
    """
    if request.method == "POST":
        group = request.POST.get("sendgroupname", "")
        hosts = request.POST.getlist("ip", "")
        model = request.POST.get("model", "")
        task = request.POST.get("task", "")
        remoteuser = request.POST.get("user","")
        chdir = request.POST.get("chdir","")

        if chdir != "":
            args = "chdir="+chdir+" "+task
        else :
            args = task

        gethost = GetHostInfo()
        inventory, variablemanager, host_list,loader = gethost.get_hosts(group_name=group,remoteuser=remoteuser)

        host_list = []
        for host in hosts:
            host_list.append(host)

        # 调用ansible模块执行命令
        ans = AnsibleRunner()
        result, success_list, failed_list, unreachable_list, command = ans.run_modle(inventory=inventory, loader=loader,
                                                                                     host_list=host_list,
                                                                                     variable_manager=variablemanager,
                                                                                     module_name=model,
                                                                                     module_args=args)

        # 执行成功主机数
        success_num = len(success_list)
        # 成功主机返回结果
        stdout_success = {}
        for host in success_list:
            savelog(request.user, command, host, 'success', result['success'][host])
            stdout_success[host] = result['success'][host]['stdout']

        # 执行成功主机数
        failed_num = len(failed_list)
        # 失败主机返回结果
        stdout_failed = {}
        for host in failed_list:
            # 保存操作日志
            savelog(request.user, command, host, 'failed', result['failed'][host])
            stdout_failed[host] = result['failed'][host]['msg']

        # 无法连接主机数
        unreachable_num = len(unreachable_list)

        data = {'success_list': success_list,
                'success_num': success_num,
                'command': command,
                'stdout_success': stdout_success,
                'failed_list': failed_list,
                'failed_num': failed_num,
                'stdout_failed': stdout_failed,
                'unreachable_num': unreachable_num,
                'unreachable_list': unreachable_list}


        return JsonResponse(data,safe=False)

def getajaxupload(request):
    """
        AJAX执行upload命令
        :param request:
        :return:
        """
    if request.method == "POST":

        host_group = request.POST.get("group", "")
        myfile = request.FILES.get("filename", None)
        username = request.POST.get("users", "").strip()
        updir = request.POST.get("uploaddir", "").strip()
        DIR = os.path.join(settings.BASE_DIR + "/tmp/", myfile.name)

        user = GroupUsers.objects.get(username=username)

        # 将用户上传的文件保存到服务器
        if myfile:
            with open(DIR, 'wb+') as destination:
                for chunk in myfile.chunks():
                    destination.write(chunk)
        if not myfile:
            return HttpResponse("no files for upload!")

        # 获取要上传的主机
        gethost = GetHostInfo()

        inventory, variablemanager, host_list, loader = gethost.get_hosts(group_name=host_group)
        # 上传文件参数
        args = "src=" + DIR + " " + "dest=" + updir + "/" + myfile.name + " " + "backup=yes" + " " + "force=yes"
        # 上传文件模块
        model = 'copy'

        # 指定文件所属用户及用户组
        if user != "":
            args = args + " " + "owner=" + user.username + " " + "group=" + user.usergroup

        # 调用ansible模块执行命令
        ans = AnsibleRunner()
        result, success_list, failed_list, unreachable_list, command = ans.run_modle(inventory=inventory, loader=loader,
                                                                                     host_list=host_list,
                                                                                     variable_manager=variablemanager,
                                                                                     module_name=model,
                                                                                     module_args=args)

        # 执行成功主机数
        success_num = len(success_list)
        # 成功主机返回结果
        stdout_success = {}
        for host in success_list:
            savelog(request.user,command,host,'success',result['success'][host])
            stdout_success[host] = result['success'][host]

        # 执行失败主机数
        failed_num = len(failed_list)
        # 失败主机返回结果
        stdout_failed = {}
        for host in failed_list:
            savelog(request.user, command, host,'failed', result['failed'][host])
            stdout_failed[host] = result['failed'][host]['msg']

        # 无法连接主机数
        unreachable_num = len(unreachable_list)

        data = {'success_list': success_list,
                   'success_num': success_num,
                   'command': command,
                   'stdout_success': stdout_success,
                   'failed_list': failed_list,
                   'failed_num': failed_num,
                   'unreachable_num': unreachable_num,
                   'unreachable_list': unreachable_list,
                   'stdout_failed': stdout_failed}

        os.remove(DIR)  #删除服务器上的临时文件

    return JsonResponse(data, safe=False)


class AddscriptsView(UserPassesTestMixin,View):
    """
    新建脚本
    """
    def test_func(self):
        """
        重载父类方法，实现系统管理员、运维人员角色的用户才能访问
        :return:
        """
        return self.request.user.role != 2

    def get(self,request):
        scripts = Scripts.objects.all()

        return render(request,"add-scripts.html",{"scripts":scripts})

    def post(self,request):
        name = request.POST.get("name","")
        text = request.POST.get("text","")
        details = request.POST.get("details","")

        path = BASE_DIR + "/scripts/"+ name +".yaml"

        with open(path,'w') as f:
            f.write(text)

        script = Scripts()
        script.name = name
        script.author = request.user.username
        script.url = path
        script.details = details
        script.save()

        return render(request,"add-scripts.html")


class DelscriptsView(UserPassesTestMixin,View):
    """
        删除脚本
            """

    def test_func(self):
        """
        重载父类方法，实现系统管理员、运维人员角色的用户才能访问
        :return:
        """
        return self.request.user.role != 2


    def get(self, request,script_id):
        script = Scripts.objects.get(id=script_id)
        path = script.url
        os.remove(path)
        script.delete()

        scripts = Scripts.objects.all()
        return render(request, "add-scripts.html", {"scripts": scripts})

class UpdatescriptsView(UserPassesTestMixin,View):
    """
        删除脚本
            """

    def test_func(self):
        """
        重载父类方法，实现系统管理员、运维人员角色的用户才能访问
        :return:
        """
        return self.request.user.role != 2


    def get(self, request,script_id):
        script = Scripts.objects.get(id=script_id)
        path = script.url

        with open(path,'r') as f:
            text = f.read()

        return render(request, "script-detail.html", {"script": script,"text":text})

    def post(self,request,script_id):
        script = Scripts.objects.get(id=script_id)

        name = request.POST.get("name","")
        details = request.POST.get("details","")
        text = request.POST.get("text","")

        script.name = name
        script.details = details

        with open(script.url, 'w') as f:
            f.write(text)

        script.save()

        groups = HostGroup.objects.all()
        scripts = Scripts.objects.all()

        return render(request,"playbook-do.html",{"groups":groups,"scripts":scripts})




class PlaybookdoView(UserPassesTestMixin,View):
    """
    新建脚本
    """
    def test_func(self):
        """
        重载父类方法，实现系统管理员、运维人员角色的用户才能访问
        :return:
        """
        return self.request.user.role != 2

    def get(self,request):
        groups = HostGroup.objects.all()
        scripts = Scripts.objects.all()

        return render(request,"playbook-do.html",{"groups":groups,"scripts":scripts})



def getplaybooktask(request):
    """
        AJAX执行playbook命令
        :param request:
        :return:
        """
    if request.method == "POST":
        group = request.POST.get("sendgroupname", "")
        hosts = request.POST.getlist("ip", "")
        scriptname = request.POST.get("scriptname", "")

        gethost = GetHostInfo()
        inventory, variablemanager, host_list, loader = gethost.get_hosts(group_name=group, remoteuser="root")

        host_list = []
        for host in hosts:
            host_list.append(host)

        inventory.subset(host_list)     #限制指定主机执行
        script = Scripts.objects.get(name=scriptname)
        playbook_path = script.url

        # 调用ansible模块执行命令
        ans = AnsibleRunner()

        result, success_list, failed_list, unreachable_list = ans.run_playbook(playbook_path=playbook_path,inventory=inventory, loader=loader,
                                                                                     variable_manager=variablemanager)


        # 执行成功主机数
        success_num = len(success_list)
        # 成功主机返回结果
        stdout_success = {}

        for host in success_list:
            savelog(request.user,playbook_path, host, 'success', result['success'][host])
            stdout_success[host] = result['success'][host]['msg']

        # 执行成功主机数
        failed_num = len(failed_list)
        # 失败主机返回结果
        stdout_failed = {}
        for host in failed_list:
            # 保存操作日志
            savelog(request.user,playbook_path, host, 'failed', result['failed'][host])
            stdout_failed[host] = result['failed'][host]['msg']

        # 无法连接主机数
        unreachable_num = len(unreachable_list)

        data = {'success_list': success_list,
                'success_num': success_num,
                'script':script.name,
                'stdout_success': stdout_success,
                'failed_list': failed_list,
                'failed_num': failed_num,
                'stdout_failed': stdout_failed,
                'unreachable_num': unreachable_num,
                'unreachable_list': unreachable_list}

        return JsonResponse(data, safe=False)