# -*- coding: utf-8 -*-
__author__ = 'clj'
__date__ = '2019/3/13 16:18'


from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.inventory.host import Host,Group
from collections import namedtuple
from .ansible_call import AnsibleRunner
from hostsinfo.models import HostsInfo,HostGroup
from hostsinfo.utils import prpcrypt

def kill_ttyp(type="",ttyp=""):
    loader = DataLoader()
    inventory = InventoryManager(loader=loader,sources=['/root/OpsAuto/conf/hostslist'])
    variablemanager = VariableManager(loader=loader, inventory=inventory)

    model = 'shell'
    pc = prpcrypt()
    host_list = []

    #获取主机组及清理进程命令
    if type == '储蓄':
        str = 'fuser -uk /dev/ptyp'
        groups = HostGroup.objects.get(group_name='储蓄逻辑集中')
    elif type == '汇兑':
        str = 'fuser -uk /dev/ptyp'
        groups = HostGroup.objects.get(group_name='电子汇兑')
    else:
        str = 'fuser -uk /dev/ttyp'
        groups = HostGroup.objects.get(group_name='代理保险')

    hosts = groups.hostsinfo_set.all()
    #读取密码
    for host in hosts:
        password = pc.decrypt(host.ssh_passwd).decode(encoding='UTF-8', errors='strict')
        new_host = inventory.get_host(hostname=host.ip)
        variablemanager.set_host_variable(host=new_host, varname='ansible_ssh_pass', value=password)

        #variablemanager.set_host_variable(host=new_host, varname='ansible_ssh_user',value='cpai')
        #variablemanager.set_host_variable(host=new_host, varname='ansible_ssh_pass', value='1245')

        host_list.append(host.ip)


    args = str.strip()+ttyp.strip()
    print(args)
    args = 'whoami'

    ans = AnsibleRunner()
    result,sucess_list,failed_list,unreachable_list,command = ans.run_modle(inventory=inventory,loader=loader,host_list=host_list,variable_manager=variablemanager,module_name=model,module_args=args)

    return result,sucess_list,failed_list,unreachable_list,command