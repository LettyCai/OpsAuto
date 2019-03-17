from django.shortcuts import render

from django.views import View
from taskdo.ansible_call import AnsibleRunner
# Create your views here.
class TaskDoView(View):
    def post(self,request):
        pass

class KillTtypView(View):
    def get(self,request):
        return render(request,"kill-ttyp.html",{'result':result})

    def post(self,request):
        type = request.POST.get('type',"")
        ttyp = request.POST.get('ttyp',"")


        inventory = MyInventory()
        variablemanager = VariableManager(loader=loader, inventory=inventory)

        if type == "chuxu" :
            hosts = inventory.get_hosts(group='chuxu')
            args = ''
            passwords = ''
            variablemanager.set_host_variable(host=host, varname='ansible_ssh_password', value='')
        if type == "baoxian":
            hosts = inventory.get_hosts(group='baoxian')
            args = ''
            passwords = ''
        if type == "huidui":
            hosts = inventory.get_hosts(group='huidui')
            args = ''
            passwords = ''
        #if hosts :
         #   ans = AnsibleRun(variablemanager=variablemanager)
        #    result = ans.run_modle(self,hosts,'shell',args+ttyp)

        return render(request,"kill-ttyp.html",{'result':result})



