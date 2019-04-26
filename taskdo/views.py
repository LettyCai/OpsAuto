from django.shortcuts import render

from django.views import View
from taskdo.ansible_call import AnsibleRunner
from taskdo import killttyp
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

        return render(request,"kill-ttyp.html",{'result':result})



