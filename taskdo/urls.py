from django.urls import path,re_path
from taskdo.views import KillTtypView,UploadView,TaskDoView,FindLogView,LogDetailsView,gethost,getajaxtask,getusers,getajaxupload,AddscriptsView,PlaybookdoView,getplaybooktask,DelscriptsView,UpdatescriptsView,ScriptdetailView
app_name = 'taskdo'

urlpatterns = [
    path('killttyp/',KillTtypView.as_view(),name="killttyp"),
    path('upload/', UploadView.as_view(), name="upload"),
    path('findlog/', FindLogView.as_view(), name="findlog"),
    re_path(r'logdetails(?P<log_id>.*)/$', LogDetailsView.as_view(), name="logdetails"),
    path(r'gethost/',gethost,name='gethost'),
    path(r'getusers/',getusers,name='getusers'),
    path(r'ajaxtask/',getajaxtask,name='ajaxtask'),
    path(r'getajaxupload/',getajaxupload,name='getajaxupload'),
    path('taskdo/', TaskDoView.as_view(), name="taskdo"),
    path('addscripts/', AddscriptsView.as_view(), name="addscripts"),
    path('playbookdo/',PlaybookdoView.as_view(), name="playbookdo"),
    path(r'ajaxplaybook/', getplaybooktask, name='ajaxplaybook'),
    re_path(r'delscript(?P<script_id>.*)/$', DelscriptsView.as_view(), name="delscript"),
    re_path(r'updatescript(?P<script_id>.*)/$', UpdatescriptsView.as_view(), name="updatescript"),
    re_path(r'scriptdetail(?P<script_id>.*)/$', ScriptdetailView.as_view(), name="scriptdetail"),
]