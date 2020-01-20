from django.contrib import admin
from django.conf.urls import include
from django.urls import path,re_path
from hostsinfo.views import DelhostusersView,AddhostusersView
app_name = 'hostsinfo'
urlpatterns = [
    re_path(r'delhost_users(?P<user_id>.*)/$',  DelhostusersView.as_view(),name="delhost_users"),
    #re_path(r'addhostusers(?P<host_id>.*)/$',  AddUsersView.as_view(),name="addhostusers"),
    path('addhost_users/',AddhostusersView.as_view(),name="addhost_users"),
]