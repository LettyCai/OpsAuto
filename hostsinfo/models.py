# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
#主机信息表
class HostsInfo(models.Model):
    ip = models.CharField(max_length=64, null=False, verbose_name=u"主机IP信息")
    ssh_port = models.CharField(max_length=32, null=True, verbose_name=u"ssh登录的端口")
    ssh_user = models.CharField(max_length=32, null=True, verbose_name=u"ssh登录的用户")
    ssh_passwd = models.CharField(max_length=64, null=True, verbose_name=u"ssh登录的用户", default="")
    ssh_rsa = models.CharField(max_length=64, null=True, verbose_name=u"登录使用的私钥", default="")
    rsa_pass = models.CharField(max_length=64, null=True, verbose_name=u"私钥的密钥", default="")
    system_ver = models.CharField(max_length=256, null=True, verbose_name=u"操作系统版本", default="")
    hostname = models.CharField(max_length=256, null=True, verbose_name=u"操作系统主机名", default="")
    mac_address = models.CharField(max_length=512, null=True,verbose_name=u"mac地址列表", default="")
    sn = models.CharField(max_length=256,null=True, verbose_name=u"SN－主机的唯一标示", default="")
    mathine_type = models.CharField(max_length=256, null=True,verbose_name=u"机器的类型 1=物理服务器,2=虚拟资产,3=网络设备 0=其他类型(未知)", default="")
    sn_key = models.CharField(max_length=256, null=True,verbose_name=u"唯一设备ID", default="")
    host_type = models.CharField(max_length=256, verbose_name=u"虚拟机上宿主机的类型", default="", null=True)


    class Meta:
        verbose_name = u'主机信息表'
        verbose_name_plural = verbose_name
        db_table = "hostinfo"

class HostGroup(models.Model):
    group_name = models.CharField(max_length=20,verbose_name=u"主机组名")
    group_detail = models.CharField(max_length=200,verbose_name=u"分组描述")

    class Meta:
        verbose_name = u'主机组'
        verbose_name_plural = verbose_name
        db_table = 'hostgroup'

class HostInGroup(models.Model):
    host_id = models.ForeignKey(HostsInfo,on_delete=models.CASCADE, verbose_name=u"主机Id", null=True, blank=True)
    group_id = models.ForeignKey(HostGroup,on_delete=models.CASCADE, verbose_name=u"所属主机组", null=True, blank=True)

    class Meta:
        verbose_name = u'主机分组表'
        verbose_name_plural = verbose_name
        db_table = 'hostingroup'