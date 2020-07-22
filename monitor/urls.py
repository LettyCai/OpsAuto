from django.urls import path,re_path
from monitor.views import MonitorView,MonitorListView

app_name = 'monitor'
urlpatterns = [
    #path('monitor/',MonitorView.as_view(),name="monitor"),
    path('monitorlist/',MonitorListView.as_view(),name="monitorlist"),
    #re_path(r'group_users(?P<group_id>.*)/$',GroupUsersView.as_view(),name="group_users"),
    re_path(r'monitor(?P<host_ip>.*)/$',MonitorView.as_view(),name="monitor"),
]