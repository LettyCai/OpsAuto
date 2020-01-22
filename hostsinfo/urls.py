from django.contrib import admin
from django.conf.urls import include
from django.urls import path,re_path
from hostsinfo.views import DelhostusersView,AddhostusersView,GroupUsersView,DelgroupusersView,AddgroupusersView
app_name = 'hostsinfo'
urlpatterns = [
    re_path(r'delhost_users(?P<user_id>.*)/$',  DelhostusersView.as_view(),name="delhost_users"),
    #path('addhost_users/',AddhostusersView.as_view(),name="addhost_users"),
    path('add_groupusers/',AddgroupusersView.as_view(),name="add_groupusers"),
    re_path(r'group_users(?P<group_id>.*)/$',GroupUsersView.as_view(),name="group_users"),
    re_path(r'del_groupusers/(?P<user_name>.*)/(?P<group_id>.*)/$',DelgroupusersView.as_view(),name="del_groupusers"),
]