from django.urls import path,re_path
from users.views import LoginView,LogoutView,UsersListView,UserSettingsView,UserProfileView,RegisterView,DelUserView
app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/',RegisterView.as_view(), name="register"),
    path('userlist/', UsersListView.as_view(), name="userlist"),
    re_path(r'^usersettings(?P<user_id>.*)/$',UserSettingsView.as_view(), name="usersettings"),
    re_path(r'^userprofile(?P<user_id>.*)/$',UserProfileView.as_view(), name="userprofile"),
    re_path(r'^deluser(?P<user_id>.*)/$', DelUserView.as_view(), name="deluser"),
]