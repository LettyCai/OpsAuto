from django.shortcuts import render

from django.views import View
from taskdo.killttyp import AnsibleRun
# Create your views here.
class TaskDoView(View):
    def post(self,request):
        pass

class KillTtypView(View):
    def get(self,request):
        ans = AnsibleRun()
        result = ans.run()


        return render(request,"kill-ttyp.html",{'result':result})



