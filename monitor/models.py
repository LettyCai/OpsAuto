from django.db import models

# Create your models here.
class HostStatus(models.Model):
    ip = models.CharField(max_length=64, null=False, verbose_name=u"主机IP信息")
    sys = models.CharField(max_length=128, null=False, verbose_name=u"所属系统")
    mem_usage = models.CharField(max_length=64, null=False, verbose_name=u"内存使用率")
    cpu_usage = models.CharField(max_length=64, null=False, verbose_name=u"CPU使用率")
    disk_usage = models.CharField(max_length=64, null=False, verbose_name=u"硬盘使用率")
    status = models.CharField(max_length=64, null=False, verbose_name=u"主机运行状态")

    class Meta:
        verbose_name = u'主机状态表'
        verbose_name_plural = verbose_name
        db_table = "monitorinfo"