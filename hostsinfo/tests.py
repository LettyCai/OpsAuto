from django.test import TestCase

# Create your tests here.
import paramiko
import yaml


#实例化paramiko类
jssh = paramiko.SSHClient()
s_conf = yaml.load(open('hostsinfo.yaml'))
s_cmds = s_conf['hostsinfo']['syscmd_list']
print(s_cmds)
#默认添加至knowhosts文件
jssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#配置连接
jssh.connect(hostname='192.168.56.102',port=22,username='root',password='123456')
result = {}
for cmd in s_cmds:
    stdin, stdout, stderr = jssh.exec_command(cmd, timeout=10)
    std_res = stdout.read()
    print(std_res)
    result[cmd] = std_res
print(result)