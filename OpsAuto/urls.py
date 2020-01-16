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
from hostsinfo.views import HostInfoView,AddHostView,CollectHostView,AddGroupView,GroupListView,HostDetailView,DelHostView,ModifyGroupView,DelGroupView,ModifyHostView,HostUsersView
from taskdo.views import KillTtypView, UploadView,TaskDoView,FindLogView,LogDetailsView,gethost,getajaxtask
from users.views import IndexView,LoginView,LogoutView,UsersListView,UserSettingsView,UserProfileView,RegisterView

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
    path('register/',RegisterView.as_view(), name="register"),
    re_path(r'^hostdetail(?P<host_id>.*)/$',HostDetailView.as_view(),name="hostdetail"),
    path('userlist/',UsersListView.as_view(), name="userlist"),
    path('usersettings/',UserSettingsView.as_view(), name="usersettings"),
    re_path(r'^hostdel(?P<host_id>.*)/$', DelHostView.as_view(), name="hostdel"),
    re_path(r'^userprofile(?P<user_id>.*)/$', UserProfileView.as_view(), name="userprofile"),
    re_path(r'modifygroup(?P<group_id>.*)/$', ModifyGroupView.as_view(), name="modifygroup"),
    re_path(r'delgroup(?P<group_id>.*)/$', DelGroupView.as_view(), name="delgroup"),
    path('taskdo/', TaskDoView.as_view(), name="taskdo"),
    path('findlog/', FindLogView.as_view(), name="findlog"),
    re_path(r'logdetails(?P<log_id>.*)/$', LogDetailsView.as_view(), name="logdetails"),
    re_path(r'modifyhost(?P<host_id>.*)/$', ModifyHostView.as_view(), name="modifyhost"),
    re_path(r'hostusers(?P<host_id>.*)/$', HostUsersView.as_view(), name="hostusers"),
    path(r'gethost/',gethost,name='gethost'),
    path(r'ajaxtask/',getajaxtask,name='ajaxtask')
]
