from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate,login,logout
from .models import UserProfile

# Create your views here.
class IndexView(View):
    def get(self,request):
        return render(request,'index.html',{})

class LoginView(View):
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
    def get(self,request):
        logout(request)

        return render(request,'login.html',{})

class UsersListView(View):
    def get(self,request):

        users = UserProfile.objects.all()

        return render(request,'users-list.html',{'users':users})