from django.urls import path,re_path
from hostsinfo.views import HostInfoView,AddHostView,CollectHostView,AddGroupView,GroupListView,HostDetailView,DelHostView,ModifyGroupView,DelGroupView,ModifyHostView
from hostsinfo.views import GroupUsersView,DelgroupusersView,AddgroupusersView,updategroupusers
app_name = 'hostsinfo'
urlpatterns = [
    path('add_groupusers/',AddgroupusersView.as_view(),name="add_groupusers"),
    re_path(r'group_users(?P<group_id>.*)/$',GroupUsersView.as_view(),name="group_users"),
    re_path(r'del_groupusers/(?P<user_name>.*)/(?P<group_id>.*)/$',DelgroupusersView.as_view(),name="del_groupusers"),
    path(r'updategroupusers/',updategroupusers,name='updategroupusers'),
    path('hostinfo/', HostInfoView.as_view(), name="hostinfo"),
    path('addhost/', AddHostView.as_view(), name="addhost"),
    path('collecthost/', CollectHostView.as_view(), name="collecthost"),
    path('addgroup/', AddGroupView.as_view(), name="addgroup"),
    path('grouplist/', GroupListView.as_view(), name="grouplist"),
    re_path(r'^hostdetail(?P<host_id>.*)/$', HostDetailView.as_view(), name="hostdetail"),
    re_path(r'^hostdel(?P<host_id>.*)/$', DelHostView.as_view(), name="hostdel"),
    re_path(r'modifygroup(?P<group_id>.*)/$', ModifyGroupView.as_view(), name="modifygroup"),
    re_path(r'delgroup(?P<group_id>.*)/$', DelGroupView.as_view(), name="delgroup"),
    re_path(r'modifyhost(?P<host_id>.*)/$', ModifyHostView.as_view(), name="modifyhost"),
]