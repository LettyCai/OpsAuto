from django.shortcuts import render,redirect
from django.views import View
from .models import HostsInfo,HostGroup,HostUsers
from .utils import prpcrypt,NMAPCollection,ListGenerate
from .forms import HostInfoForm
import re
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #分页
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin  #用户登录验证，用户权限验证

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


class AddHostView(UserPassesTestMixin,View):
    def test_func(self):
        """
        重载父类方法，实现系统管理员、运维人员角色的用户才能访问
        :return:
        """
        return self.request.user.role != 2

    def post(self,request):

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
            return render(request,"500.html",{"status":"failed","error":"主机已存在!"})
        else:
            #存储主机信息
            host.save()

            #添加主机所属主机组信息
            for group in groups:
                host = HostsInfo.objects.get(ip=host.ip)
                group = HostGroup.objects.get(group_name=str(group))
                host.host_group.add(group)
                #group.host_num += 1

            # 重新生成hostslist文件
            ge = ListGenerate()
            ge.generate_hostslist()

            return render(request, "add-host.html", {"status": "success"})

    def get(self,request):
        groups = HostGroup.objects.all()
        return render(request,"add-host.html",{'groups':groups})


class CollectHostView(View):

    def post(self,request):
        host_ip = request.POST.get('ip',"")
        host_password = request.POST.get('password',"")

        #检查ip地址格式是否正确：
        if re.match('((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))', host_ip, flags=0):
            #收集主机信息
            nm = NMAPCollection()
            result = nm.collection(host_ip,host_password)

            if result['status']== 'success':
                # 对登陆密码进行加密，并将加密后的密码回传给前端页面
                prp = prpcrypt()
                result['host_pass'] = prp.encrypt(host_password).decode(encoding='UTF-8',errors='strict')
                result['host_ip'] = host_ip

                #查询所有主机组信息，并传给前端添加主机页面显示
                groups = HostGroup.objects.all()
                return render(request,"add-host.html",{'res':result,'groups':groups})
            else:
                groups = HostGroup.objects.all()
                return render(request,"add-host.html",{"msg":"主机信息获取失败",'res':result['res'],'groups':groups})
        #ip地址格式不正确
        else:
            # 查询所有主机组信息，并传给前端添加主机页面显示
            groups = HostGroup.objects.all()
            return render(request,"add-host.html",{'msg':"ip地址格式不正确！",'groups':groups})


class AddGroupView(UserPassesTestMixin,View):
    def test_func(self):
        """
        重载父类方法，实现系统管理员、运维人员角色的用户才能访问
        :return:
        """
        return self.request.user.role != 2

    def get(self,request):
        return render(request,"add-group.html")

    def post(self,request):
        group = HostGroup()

        group.group_name = request.POST.get('group_name',"")
        group.group_detail = request.POST.get('group_detail',"")
        group.network = request.POST.get('group_network',"")

        has_group = HostGroup.objects.filter(group_name =group.group_name)

        if has_group:
            return render(request,"add-group.html",{"status":"failed","msg":"添加失败：主机组已存在！"})
        elif group.group_name == "":
            return render(request,"add-group.html",{"status":"failed","msg":"添加失败：主机组名不能为空！"})
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

            return render(request, "group-list.html", {"status": "success",'groups':groups,"msg":"添加成功！"})


class HostDetailView(View):
    """
    主机详细信息展示View
    """
    def get(self,request,host_id):

        host = HostsInfo.objects.get(id=host_id)

        return render(request, "host-detail.html", {"host": host})


class DelHostView(UserPassesTestMixin,View):
    """
    删除主机
    """
    def test_func(self):
        """
        重载父类方法，实现系统管理员、运维人员角色的用户才能访问
        :return:
        """
        return self.request.user.role != 2

    def get(self,request,host_id):
        #删除主机数据
        HostsInfo.objects.filter(id=host_id).delete()


        # 获取所有主机
        hosts = HostsInfo.objects.all()
        # 获取所有主机组
        groups = HostGroup.objects.all()

        return render(request, "hosts-list.html", {'hosts': hosts, 'groups': groups})


class ModifyHostView(UserPassesTestMixin,View):
    """
    修改主机登陆密码
    """

    def test_func(self):
        """
        重载父类方法，实现系统管理员、运维人员角色的用户才能访问
        :return:
        """
        return self.request.user.role != 2

    def get(self,request,host_id):
        host = HostsInfo.objects.get(id=int(host_id))
        return render(request,"modifyhost.html",{"host":host})

    def post(self,request,host_id):
        host_ip = request.POST.get('ip', "")
        host_password = request.POST.get('password', "")

        print("*"*50)
        print(host_ip)
        print(host_password)

        nm = NMAPCollection()
        result = nm.collection(host_ip, host_password)

        if result['status'] == 'success':
            # 对登陆密码进行加密
            prp = prpcrypt()
            host_pass = prp.encrypt(host_password).decode(encoding='UTF-8', errors='strict')

            #更新主机密码
            host= HostsInfo.objects.get(ip=host_ip)
            host.ssh_passwd = host_pass
            host.save()

            # 返回主机列表页面
            hosts = HostsInfo.objects.all()
            groups = HostGroup.objects.all()

            # 分页
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1

            # Provide Paginator with the request object for complete querystring generation
            p = Paginator(hosts, 10, request=request)
            hosts = p.page(page)

            return render(request, "hosts-list.html", {'msg': "修改成功!",'hosts': hosts, 'groups': groups})

        else:
            groups = HostGroup.objects.all()
            return render(request, "add-host.html", {"msg": "主机信息获取失败", 'res': result['res'], 'groups': groups})


class GroupListView(View):
    def get(self,request):
        groups = HostGroup.objects.all()

        #主机组分页显示
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(groups,10,request=request)
        groups = p.page(page)

        return render(request,"group-list.html",{'groups':groups})


class ModifyGroupView(UserPassesTestMixin,View):
    """
    修改主机组信息
    """
    def test_func(self):
        """
        重载父类方法，实现系统管理员、运维人员角色的用户才能访问
        :return:
        """
        return self.request.user.role != 2

    def get(self,request,group_id):
        group = HostGroup.objects.get(id=int(group_id))
        return render(request,"group-detail.html",{'group':group})

    def post(self,request,group_id):
        group_name = request.POST.get('group_name','')
        group_network = request.POST.get('group_network','')
        group_detail = request.POST.get('group_detail','')

        if group_name =="":
            group = HostGroup.objects.get(id=int(group_id))
            return render(request, "group-detail.html", {'group': group, 'msg':"修改失败：主机组名不能为空！"})
        else:
            HostGroup.objects.filter(id=int(group_id)).update(group_name=group_name,network=group_network,group_detail=group_detail)

        groups = HostGroup.objects.all()

        # 主机组分页显示
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(groups, 10, request=request)
        groups = p.page(page)

        return render(request, "group-list.html", {'groups': groups, 'msg':"修改成功!"})


class DelGroupView(UserPassesTestMixin,View):
    """
    删除主机组
    """
    def test_func(self):
        """
        重载父类方法，实现系统管理员、运维人员角色的用户才能访问
        :return:
        """
        return self.request.user.role != 2

    def get(self,request,group_id):
        HostGroup.objects.filter(id=int(group_id)).delete()

        groups = HostGroup.objects.all()

        # 主机组分页显示
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(groups, 10, request=request)
        groups = p.page(page)

        return render(request, "group-list.html", {'groups': groups, 'msg': "删除成功!"})



class HostUsersView(UserPassesTestMixin,View):
    """
        主机可使用的用户组
        """

    def test_func(self):
        """
        重载父类方法，实现系统管理员、运维人员角色的用户才能访问
        :return:
        """
        return self.request.user.role != 2

    def get(self, request, host_id):
        users = HostUsers.objects.filter(host__id=host_id)

        return render(request, "host-users.html", {'users':users})




