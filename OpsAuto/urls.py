"""OpsAuto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from hostsinfo.views import HostInfoView,AddHostView,CollectHostView,AddGroupView,GroupListView,HostDetailView
from taskdo.views import KillTtypView, UploadView
from users.views import IndexView,LoginView,LogoutView,UsersListView,UserSettingsView

urlpatterns = [
    path('index/',  IndexView.as_view(),name="index"),
    path('admin/', admin.site.urls),
    path('hostinfo/', HostInfoView.as_view(),name="hostinfo"),
    path('killttyp/', KillTtypView.as_view(),name="killttyp"),
    path('addhost/', AddHostView.as_view(),name="addhost"),
    path('collecthost/', CollectHostView.as_view(),name="collecthost"),
    path('addgroup/', AddGroupView.as_view(),name="addgroup"),
    path('grouplist/', GroupListView.as_view(),name="grouplist"),
    path('upload/', UploadView.as_view(), name="upload"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    re_path(r'^hostdetail(?P<host_id>.*)/$',HostDetailView.as_view(),name="hostdetail"),
    path('userlist/',UsersListView.as_view(), name="userlist"),
    path('usersettings/',UserSettingsView.as_view(), name="usersettings"),
]
