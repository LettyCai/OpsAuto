# Generated by Django 2.0.4 on 2020-02-02 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GroupUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, null=True, verbose_name='用户名')),
                ('passwd', models.CharField(max_length=64, null=True, verbose_name='登陆密码')),
                ('usergroup', models.CharField(max_length=32, null=True, verbose_name='用户组')),
            ],
            options={
                'verbose_name': '主机组登陆用户表',
                'verbose_name_plural': '主机组登陆用户表',
                'db_table': 'groupusers',
            },
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=200, null=True, verbose_name='主机组名')),
                ('group_detail', models.CharField(max_length=200, null=True, verbose_name='分组描述')),
                ('network', models.CharField(max_length=200, null=True, verbose_name='网络')),
                ('hosts_num', models.CharField(max_length=200, null=True, verbose_name='主机数')),
            ],
            options={
                'verbose_name': '主机组',
                'verbose_name_plural': '主机组',
                'db_table': 'hostgroup',
            },
        ),
        migrations.CreateModel(
            name='HostsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=64, verbose_name='主机IP信息')),
                ('ssh_port', models.CharField(max_length=32, null=True, verbose_name='ssh登录的端口')),
                ('ssh_user', models.CharField(max_length=32, null=True, verbose_name='ssh登录的用户')),
                ('ssh_passwd', models.CharField(default='', max_length=64, null=True, verbose_name='ssh登录的用户')),
                ('ssh_rsa', models.CharField(default='', max_length=64, null=True, verbose_name='登录使用的私钥')),
                ('rsa_pass', models.CharField(default='', max_length=64, null=True, verbose_name='私钥的密钥')),
                ('system_ver', models.CharField(default='', max_length=256, null=True, verbose_name='操作系统版本')),
                ('hostname', models.CharField(default='', max_length=256, null=True, verbose_name='操作系统主机名')),
                ('mac_address', models.CharField(default='', max_length=512, null=True, verbose_name='mac地址列表')),
                ('sn', models.CharField(default='', max_length=256, null=True, verbose_name='SN－主机的唯一标示')),
                ('mathine_type', models.CharField(default='', max_length=256, null=True, verbose_name='机器的类型 1=物理服务器,2=虚拟资产,3=网络设备 0=其他类型(未知)')),
                ('sn_key', models.CharField(default='', max_length=256, null=True, verbose_name='唯一设备ID')),
                ('host_type', models.CharField(default='', max_length=256, null=True, verbose_name='虚拟机上宿主机的类型')),
                ('host_group', models.ManyToManyField(to='hostsinfo.HostGroup')),
            ],
            options={
                'verbose_name': '主机信息表',
                'verbose_name_plural': '主机信息表',
                'db_table': 'hostinfo',
            },
        ),
        migrations.AddField(
            model_name='groupusers',
            name='hostgroup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hostsinfo.HostGroup', verbose_name='所属主机组'),
        ),
    ]
