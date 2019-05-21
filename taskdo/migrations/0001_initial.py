# Generated by Django 2.0.4 on 2019-05-21 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OpsLogModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20, null=True, verbose_name='用户名')),
                ('group', models.CharField(max_length=200, null=True, verbose_name='操作主机组')),
                ('hosts', models.TextField(null=True, verbose_name='操作主机')),
                ('result', models.CharField(max_length=20, null=True, verbose_name='执行结果')),
                ('details', models.TextField(null=True, verbose_name='操作日志')),
            ],
            options={
                'verbose_name': '操作日志',
                'verbose_name_plural': '操作日志',
                'db_table': 'opslogs',
            },
        ),
    ]
