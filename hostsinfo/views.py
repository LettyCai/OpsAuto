from django.shortcuts import render
from django.views import View
from .models import HostsInfo

# Create your views here.
class HostInfoView(View):
    def get(self,request):
        hosts = HostsInfo.objects.all()
        return render(request,"hosts-list.html",{'hosts':hosts})


class AddHostView(View):
    def post(self,request):
        host = HostsInfo()
