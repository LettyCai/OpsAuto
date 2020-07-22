from hostsinfo.utils import prpcrypt
from hostsinfo.models import HostsInfo,HostGroup
import  paramiko

def getmsg(hostip):
    host = HostsInfo.objects.get(ip=hostip)
    password = host.ssh_passwd
    pc = prpcrypt()
    password = pc.decrypt(password).decode(encoding='UTF-8', errors='strict')
    result = []

    try:
        a2 = "parted -l  | grep   \"Disk \/dev\/[a-z]d\"  | awk -F\"[ ]\"  '{print $3}' | awk  -F\"GB\"  '{print $1}'"
        s = ssh(ip=hostip, password=password, cmd=a2)
        disk1 = s['data']
        disk2 = disk1.rstrip().split("\n")
        disk = "+".join(map(str, disk2))  # + "   共计:{} GB".format(round(sum(map(float, disk2))))
        result.append({"total_disk": disk})
    except Exception  as  e:
        result.append({"msg": e})

    try:
        a1 = "top -b -n 1 | grep Cpu | awk -F\"[ ]\"  '{print $3}' "
        s = ssh(ip=hostip, password=password, cmd=a1)
        cpu_use = s['data']
        cpu_use_data = int(float(cpu_use))
        result.append({"cpu_use_data": cpu_use_data})
    except Exception as e:
        result.append({"msg2": e})
        cpu_use_data = e

    try:
        a3 = "free | grep Mem | awk '{print $2}' "
        s = ssh(ip=hostip, password=password, cmd=a3)
        mem_total = s['data']
        a4 = "free | grep Mem | awk '{print $3}' "
        s = ssh(ip=hostip, password=password, cmd=a4)
        mem_use = s['data']
        mem_use_data = int(int(mem_use) / int(mem_total) * 100)
        result.append({"mem_use_data": mem_use_data})


    except Exception as e:
        result.append({"msg2": e})
        mem_use_data = e

    try:
        a4 = "df -P | grep /$ | awk '{print $5}' | sed 's/%//g'"
        s = ssh(ip=hostip, password=password, cmd=a4)
        disk_use = int(s['data'])
    except Exception as e:
        result.append({"msg3": e})
        disk_use = e

    data = {"mem_use_data": mem_use_data, "cpu_use_data": cpu_use_data, "disk_use_data": disk_use}
    return data



def ssh(ip, password, cmd):
    try:
        ssh = paramiko.SSHClient()  # 创建ssh对象
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, port=22, username="root", password=password, )
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)

        result = stdout.read()
        result1 = result.decode()
        error = stderr.read().decode('utf-8')

        if not error:
            ret = {"ip": ip, "data": result1}
            ssh.close()
            return ret
    except Exception as e:
        error = "账号或密码错误,{}".format(e)
        ret = {"ip": ip, "data": error}
        return ret
