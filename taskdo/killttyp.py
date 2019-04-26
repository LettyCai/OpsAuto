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
    #inventory = InventoryManager(loader=loader, sources=[])
    variablemanager = VariableManager(loader=loader, inventory=inventory)

    model = 'shell'
    str = ''
    pc = prpcrypt()
    host_list = []

    if type == 'chuxu':
        str = 'fuser -uk /dev/ptyp'
        groups = HostGroup.objects.get(group_name='储蓄逻辑集中')
        hosts = groups.hostsinfo_set.all()
        for host in hosts:
            password = pc.decrypt(host.ssh_passwd).decode(encoding='UTF-8',errors='strict')
            new_host = inventory.get_host(hostname=host.ip)
            variablemanager.set_host_variable(host=new_host, varname='ansible_ssh_pass', value=password)
            host_list.append(host.ip)
    if type == 'huidui':
        str = 'fuser -uk /dev/ptyp'

    if type == 'baoxian':
        str = 'fuser -uk /dev/ttyp'


    args = str.strip()+ttyp.strip()

    print('*' * 20)
    print(host_list)
    print(model)
    print(args)
    print('*' * 20)
    args = 'touch /root/abcdefg.txt'

    ans = AnsibleRunner()
    result = ans.run_modle(inventory=inventory,loader=loader,host_list=host_list,variable_manager=variablemanager,module_name=model,module_args=args)

    return result