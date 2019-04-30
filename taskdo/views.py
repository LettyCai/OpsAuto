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


        #inventory = MyInventory()
        #ariablemanager = VariableManager(loader=loader, inventory=inventory)

        killttyp.kill_ttyp(type=type,ttyp=ttyp)

        result = killttyp.kill_ttyp(type=type,ttyp=ttyp)

        for key,value in result:
            print('*'*10)
            print(key)
            print(value)


        return render(request,"kill-ttyp.html",{'result':result})

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
        if myfile :
            with open(DIR,'wb+') as destination:
                for chunk in myfile.chunks():
                    destination.write(chunk)
        if not myfile :
            return HttpResponse("no files for upload!")

        gethost = GetHostInfo()

        inventory, variablemanager, host_list,loader = gethost.get_hosts(group_name=host_group)
        args = "src="+DIR+" "+"dest="+updir+"/"+myfile.name
        model = 'copy'

        #指定以user用户上传
        if user != "":
            args = args + " " + "owner="+user

        ans = AnsibleRunner()

        result = ans.run_modle(inventory=inventory, loader=loader,host_list=host_list,
                               variable_manager=variablemanager, module_name=model, module_args=args)



        return render(request, "upload.html",{'result':result,'groups':groups})





