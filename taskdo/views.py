from django.shortcuts import render

from django.views import View
# Create your views here.
class TaskDoView(View):
    def post(self,request):
        pass

class KillTtypView(View):
    def get(self,request):
        return render(request,"kill-ttyp.html")



