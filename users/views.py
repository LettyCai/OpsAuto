from django.shortcuts import render,HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin  #用户登录验证，用户权限验证
from .models import UserProfile
from hostsinfo.models import HostsInfo,HostGroup
from OpsAuto.settings import LOGIN_URL
# Create your views here.

class IndexView(LoginRequiredMixin,View):
    """
    首页。只允许登陆用户访问
    """

    def get(self, request):
        hosts = HostsInfo.objects.all()
        host_num = hosts.count()
        groups = HostGroup.objects.all()
        group_num = groups.count()
        return render(request, 'index.html', {'host_num': host_num, 'group_num': group_num})



class LoginView(View):
    """
    用户登录
    """
    def get(self,request):
        return render(request,'login.html',{})

    def post(self,request):
        username = request.POST.get('username',"")
        password = request.POST.get('password',"")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, "index.html")
        else:
            return render(request, "login.html", {"msg": "用户名或密码错误"})

class LogoutView(View):
    """
    退出登陆
    """
    def get(self,request):
        logout(request)

        return render(request,'login.html',{})

class UsersListView(UserPassesTestMixin,View):
    """
    系统管理员查看用户列表
    """
    def test_func(self):
        """
        重载父类方法，系统管理员角色的用户才能访问
        :return:
        """
        return self.request.user.role == 0

    def get(self,request):

        users = UserProfile.objects.all()

        return render(request,'users-list.html',{'users':users})

class UserSettingsView(LoginRequiredMixin,View):
    """
    用户修改个人信息
    """
    def get(self,request):

        return render(request,'settings.html')

    def post(self,request):
        username = request.POST.get('username','')
        email = request.POST.get('email','')
        id = request.POST.get('user_id','')
        mobile = request.POST.get('mobile','')

        password1 = request.POST.get('password1','')
        password2 = request.POST.get('password2','')

        #未填写密码项，修改其他信息
        if password1 == '' and password2 == '' :
            user = UserProfile.objects.get(id=int(id))
            user.username = username
            user.email = email
            user.mobile = mobile
            user.save()
            return render(request,"settings.html")
        #填写了密码项且2次密码相同：
        elif password1 == password2:
            user = UserProfile.objects.get(id=int(id))
            user.password = make_password(pwd2)
            user.username = username
            user.email = email
            user.mobile = mobile
            user.save()
            return render(request, "settings.html")
        #2次密码不同：
        else:
            return render(request, "500.html", {"msg": "密码不一致"})



class UserProfileView(UserPassesTestMixin,View):
    """
    系统管理员修改所有用户信息
    """

    def test_func(self):
        """
        重载父类方法，系统管理员角色的用户才能访问
        :return:
        """
        return self.request.user.role == 0

    def get(self,request,user_id):
        user = UserProfile.objects.get(id=user_id)

        return render(request,"userprofile.html",{'user':user})

    def post(self,request,user_id):
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        mobile = request.POST.get('mobile', '')

        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        # 未填写密码项，修改其他信息
        if password1 == '' and password2 == '':
            user = UserProfile.objects.get(id=int(user_id))
            user.username = username
            user.email = email
            user.mobile = mobile
            user.save()
            return render(request, "userprofile.html",{'user':user})
        # 填写了密码项且2次密码相同：
        elif password1 == password2:
            user = UserProfile.objects.get(id=int(user_id))
            user.password = make_password(pwd2)
            user.username = username
            user.email = email
            user.mobile = mobile
            user.save()
            return render(request,"userprofile.html",{'user':user})
        # 2次密码不同：
        else:
            return render(request, "500.html", {"msg": "密码不一致"})


