from django.db import models

# Create your models here.

class OpsLog(models.Model):
    user = models.CharField(max_length=20,verbose_name=u"用户名",null=True)
    cmd = models.CharField(max_length=200,verbose_name=u"操作命令",null=True)
    host = models.TextField(verbose_name=u"操作主机",null=True)
    result = models.CharField(max_length=20,verbose_name=u"执行结果",null=True)
    details = models.TextField(verbose_name=u"操作日志",null=True)
    date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = u'操作日志'
        verbose_name_plural = verbose_name
        db_table = 'opslogs'

class Scripts(models.Model):
    name = models.CharField(max_length=100,verbose_name=u"任务名称",null=True)
    details = models.CharField(max_length=200,verbose_name=u"任务描述",null=True)
    author = models.CharField(max_length=20,verbose_name=u"作者",null=True)
    url = models.CharField(max_length=200,verbose_name=u"文件路径",null=True)

    class Meta:
        verbose_name = u'脚本文件'
        verbose_name_plural = verbose_name
        db_table = 'scripts'