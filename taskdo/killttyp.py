# -*- coding: utf-8 -*-
__author__ = 'clj'
__date__ = '2019/3/13 16:18'


from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.inventory.host import Host,Group
from collections import namedtuple
#from ansible_call import AnsibleRunner
from hostsinfo.models import HostsInfo

def kill_ttyp(type="",ttyp=""):
    loader = DataLoader()
    inventory = InventoryManager(loader=loader,sources=['/root/OpsAuto/conf/hostslist'])
    hosts = inventory.get_hosts()
    print('*'*20)
    print(hosts)
    print('*'*20)
    variablemanager = VariableManager(loader=loader, inventory=inventory)
    hosts_info = HostsInfo.objects.filter()
    for host in hosts:
       variablemanager.set_host_variable(host=host.ip,varname='ansible_ssh_pass',value=host.ssh_passwd)

    model = 'shell'
    str = ''

    if type == 'chuxu' or type =='huidu':
        str = 'fuser -uk /dev/ptyp'
    if type == 'baoxian':
        str = 'fuser -uk /dev/ttyp'

    args = str.strip()+ttyp.strip()

    print(args)

    hs = inventory.get_hosts()
    hosts = []
   # for h in hs:
   #     hosts.append(str(host))

    #ans = AnsibleRunner()
    #ans.run_modle(inventory=inventory,host_list=hosts,loader=loader,variable_manager=variablemanager,module_name=model,module_args=args)

    return None