# Generated by Django 2.0.4 on 2020-07-22 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HostStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=64, verbose_name='主机IP信息')),
                ('sys', models.CharField(max_length=128, verbose_name='所属系统')),
                ('mem_usage', models.CharField(max_length=64, verbose_name='内存使用率')),
                ('cpu_usage', models.CharField(max_length=64, verbose_name='CPU使用率')),
                ('disk_usage', models.CharField(max_length=64, verbose_name='硬盘使用率')),
                ('status', models.CharField(max_length=64, verbose_name='主机运行状态')),
            ],
            options={
                'verbose_name': '主机状态表',
                'verbose_name_plural': '主机状态表',
                'db_table': 'monitorinfo',
            },
        ),
    ]