from django.db import models

# Create your models here.

class LogModel(models.Model):
    user = models.CharField(max_length=20,verbose_name=u"用户名",null=True)
    hosts = models.CharField(max_length=20,verbose_name=u"主机",null=True)
    result = models.CharField(max_length=20,verbose_name=u"执行结果",null=True)
    logs = models.CharField(max_length=500,verbose_name=u"操作日志",null=True)

    class Meta:
        verbose_name = u'操作日志'
        verbose_name_plural = verbose_name
        db_table = 'logs'