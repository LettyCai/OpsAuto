from django.shortcuts import render,redirect
from django.views import View
from .models import HostsInfo,HostGroup
from .utils import prpcrypt,NMAPCollection
from .forms import HostInfoForm
#分页
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
class HostInfoView(View):
    def get(self,request):
        #获取所有主机
        hosts = HostsInfo.objects.all()
        #获取所有主机组
        groups = HostGroup.objects.all()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(hosts, 10, request=request)
        hosts = p.page(page)
        
        return render(request,"hosts-list.html",{'hosts':hosts,'groups':groups})

    def post(self,request):
        group = request.POST.get('host_group',"")
        ip = request.POST.get('host_ip',"")

        #获取指定主机组里的主机
        if group.strip() != '':
            groups = HostGroup.objects.get(group_name=group)
            hosts = groups.hostsinfo_set.all()
            #筛选ip地址
            if ip.strip() != '':
                hosts = hosts.filter(ip=ip.strip())
        #获取所有主机组里的主机
        else:
            hosts = HostsInfo.objects.all()
            ##筛选ip地址
            if ip.strip() != '':
                hosts = hosts.filter(ip=ip.strip())
        #返回所有主机组列表
        groups = HostGroup.objects.all()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(hosts, 10, request=request)
        hosts = p.page(page)

        print('*'*20)
        print(hosts)


        return render(request,"hosts-list.html",{'hosts':hosts,'groups':groups})


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

        groups = request.POST.getlist("group")

        has_host = HostsInfo.objects.filter(ip=host.ip)

        if has_host:
            return render(request,"500.html",{"status":"failed","error":"the host has added!"})
        else:
            host.save()

            for group in groups:
                host = HostsInfo.objects.get(ip=host.ip)
                group = HostGroup.objects.get(group_name=str(group))
                host.host_group.add(group)
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
        groups = HostGroup.objects.all()
        return render(request,"add-host.html",{'groups':groups})


class CollectHostView(View):

    def post(self,request):
        host_ip = request.POST.get('ip',"")
        host_password = request.POST.get('password',"")
        nm = NMAPCollection()
        result = nm.collection(host_ip,host_password)
        prp = prpcrypt()
        result['host_pass'] = prp.encrypt(host_password).decode(encoding='UTF-8',errors='strict')
        result['host_ip'] = host_ip

        groups = HostGroup.objects.all()

        return render(request,"add-host.html",{'res':result,'groups':groups})

class GroupListView(View):
    def get(self,request):
        groups = HostGroup.objects.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(groups,10,request=request)
        groups = p.page(page)

        return render(request,"group-list.html",{'groups':groups})

class AddGroupView(View):
    def get(self,request):
        return render(request,"add-group.html")

    def post(self,request):
        group = HostGroup()

        group.group_name = request.POST.get('group_name',"")
        group.group_detail = request.POST.get('group_detail',"")
        group.network = request.POST.get('group_network',"")

        print(group.group_name)

        has_group = HostGroup.objects.filter(group_name =group.group_name)

        if has_group:
            return render(request,"500.html",{"status":"failed","error":"the group has added!"})
        else:
            group.save()
            groups = HostGroup.objects.all()

            #分页
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1

            # Provide Paginator with the request object for complete querystring generation
            p = Paginator(groups, 10, request=request)
            groups = p.page(page)

            return render(request, "group-list.html", {"status": "success",'groups':groups})

class HostDetailView(View):
    def get(self,request,host_id):

        host = HostsInfo.objects.get(id=host_id)

        return render(request, "host-detail.html", {"host": host})

class DelHostView(View):
    def get(self,request,host_id):
        #删除主机数据
        HostsInfo.objects.filter(id=host_id).delete()

        # 获取所有主机
        hosts = HostsInfo.objects.all()
        # 获取所有主机组
        groups = HostGroup.objects.all()

        return render(request, "hosts-list.html", {'hosts': hosts, 'groups': groups})

class ModifyGroupView(View):
    def get(self,request,group_id):
        group = HostGroup.objects.get(id=int(group_id))
        return render(request,"group-detail.html",{'group':group})

    def post(self,request,group_id):
        group_name = request.POST.get('group_name','')
        group_network = request.POST.get('group_network','')
        group_detail = request.POST.get('group_detail','')

        group_id = request.POST.get('group_id','')

        HostGroup.objects.filter(id=int(group_id)).update(group_name=group_name,network=group_network,group_detail=group_detail)

        return redirect("grouplist")

class DelGroupView(View):
    def get(self,request,group_id):
        HostGroup.objects.filter(id=int(group_id)).delete()

        return redirect("grouplist")



