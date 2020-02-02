from django.contrib import admin
from .models import HostsInfo
# Register your models here.

class HostInfofileAdmin(admin.ModelAdmin):
    pass

admin.site.register(HostsInfo,HostInfofileAdmin)
