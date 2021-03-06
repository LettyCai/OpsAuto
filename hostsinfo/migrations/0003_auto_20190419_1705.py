# Generated by Django 2.0.4 on 2019-04-19 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostsinfo', '0002_auto_20190320_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostgroup',
            name='host_num',
            field=models.CharField(max_length=200, null=True, verbose_name='主机数'),
        ),
        migrations.AddField(
            model_name='hostgroup',
            name='network',
            field=models.CharField(max_length=200, null=True, verbose_name='网络'),
        ),
        migrations.AlterField(
            model_name='hostgroup',
            name='group_detail',
            field=models.CharField(max_length=200, null=True, verbose_name='分组描述'),
        ),
        migrations.AlterField(
            model_name='hostgroup',
            name='group_name',
            field=models.CharField(max_length=20, null=True, verbose_name='主机组名'),
        ),
    ]
