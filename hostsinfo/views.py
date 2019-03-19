from django.shortcuts import render
from django.views import View
from .models import HostsInfo
from .utils import prpcrypt,NMAPCollection

# Create your views here.
class HostInfoView(View):
    def get(self,request):
        hosts = HostsInfo.objects.all()
        return render(request,"hosts-list.html",{'hosts':hosts})


class AddHostView(View):
    def post(self,request):
        host = HostsInfo()

        password = request.POST.get('password',"")
        prp = prpcrypt()
        host.password = prp.encrypt(password)

        return render(request,"")

    def get(self,request):

        return render(request,"add-host.html")

class CollectHostView(View):
    def post(self,request):
        host_ip = request.POST.get('ip',"")
        host_password = request.POST.get('password',"")
        nm = NMAPCollection()
        result = nm.collection(host_ip,host_password)
        print(result)
        return render(request,"add-host.html",{'res':result})

