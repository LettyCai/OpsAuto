from django.contrib import admin
from django.conf.urls import include
from django.urls import path,re_path
from hostsinfo.views import DelhostusersView,AddhostusersView
app_name = 'hostsinfo'
urlpatterns = [
    re_path(r'delhostusers(?P<user_id>.*)/$',  DelhostusersView.as_view(),name="delhostusers"),
    #re_path(r'addhostusers(?P<host_id>.*)/$',  AddUsersView.as_view(),name="addhostusers"),
    path('addhostusers/',AddhostusersView.as_view(),name="addhostusers"),
]