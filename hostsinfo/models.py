# -*- coding: utf-8 -*-
from django.db import models

class HostGroup(models.Model):
    group_name = models.CharField(max_length=200,verbose_name=u"主机组名",null=True)
    group_detail = models.CharField(max_length=200,verbose_name=u"分组描述",null=True)
    network = models.CharField(max_length=200,verbose_name=u"网络",null=True)
    #hosts_num = models.CharField(max_length=200,verbose_name=u"主机数",null=True)

    class Meta:
        verbose_name = u'主机组'
        verbose_name_plural = verbose_name
        db_table = 'hostgroup'

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
    host_group = models.ManyToManyField(HostGroup)

    class Meta:
        verbose_name = u'主机信息表'
        verbose_name_plural = verbose_name
        db_table = "hostinfo"

class GroupUsers(models.Model):
    username = models.CharField(max_length=32, null=True, verbose_name=u"用户名")
    passwd = models.CharField(max_length=64, null=True, verbose_name=u"登陆密码")
    usergroup = models.CharField(max_length=32, null=True, verbose_name=u"用户组")
    hostgroup = models.ForeignKey(HostGroup,on_delete=models.SET_NULL,null=True,verbose_name=u"所属主机组")

    class Meta:
        verbose_name = u'主机组登陆用户表'
        verbose_name_plural = verbose_name
        db_table = "groupusers"