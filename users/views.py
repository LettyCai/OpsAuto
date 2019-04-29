from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate,login,logout

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
