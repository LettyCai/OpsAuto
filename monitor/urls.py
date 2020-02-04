from django.urls import path,re_path
from monitor.views import MonitorView

app_name = 'monitor'
urlpatterns = [
    path('monitor/',MonitorView.as_view(),name="monitor"),
    #re_path(r'group_users(?P<group_id>.*)/$',GroupUsersView.as_view(),name="group_users"),
]