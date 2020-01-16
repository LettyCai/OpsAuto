from django.contrib import admin
from .models import HostsInfo,HostUsers
# Register your models here.

class HostInfofileAdmin(admin.ModelAdmin):
    pass

admin.site.register(HostsInfo,HostInfofileAdmin)

class HostUsersAdmin(admin.ModelAdmin):
    pass
admin.site.register(HostUsers,HostUsersAdmin)
