from django.shortcuts import render
from django.views import View
from .models import HostsInfo
from .utils import prpcrypt,NMAPCollection
from .forms import HostInfoForm

# Create your views here.
class HostInfoView(View):
    def get(self,request):
        hosts = HostsInfo.objects.all()
        return render(request,"hosts-list.html",{'hosts':hosts})


class AddHostView(View):
    def post(self,request):
        host_form = HostInfoForm(request.POST)

        host = HostsInfo()

        host.ip = request.POST.get('ip',"")
        host.ssh_passwd =request.POST.get('ssh_passwd',"")
        host.host_type = request.POST.get('host_type',"")
        host.system_ver = request.POST.get('system_ver',"")
        host.hostname = request.POST.get('hostname',"")
        host.mac_address = request.POST.get('mac_address',"")
        host.sn_key = request.POST.get('sn_key',"")

        print(host)

        has_host = HostsInfo.objects.filter(ip=host.ip)

        print(has_host)

        if has_host:
            return render(request,"500.html",{"status":"failed","error":"the host has added!"})
        else:
            host.save()
            return render(request, "add-host.html", {"status": "success"})

        """
        if host_form.is_valid():
            host_form.save()
        else:
            return render(request, "500.html", {"status": "fail"}) 
        """
        #prp = prpcrypt()
        #host.password = prp.encrypt(password)



    def get(self,request):

        return render(request,"add-host.html")

class CollectHostView(View):

    def post(self,request):
        host_ip = request.POST.get('ip',"")
        host_password = request.POST.get('password',"")
        nm = NMAPCollection()
        result = nm.collection(host_ip,host_password)
        prp = prpcrypt()
        result['host_pass'] = prp.encrypt(host_password)
        result['host_ip'] = host_ip
        print(result)

        return render(request,"add-host.html",{'res':result})

