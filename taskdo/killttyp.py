# -*- coding: utf-8 -*-
__author__ = 'clj'
__date__ = '2019/3/13 16:18'


from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.inventory.host import Host,Group
from collections import namedtuple
from ansible_call import AnsibleRunner


loader = DataLoader()
inventory = InventoryManager(loader=loader,sources=['/root/OpsAuto/conf/hostslist'])
host = inventory.get_host(hostname='192.168.205.10')
variablemanager = VariableManager(loader=loader, inventory=inventory)
variablemanager.set_host_variable(host=host,varname='ansible_ssh_pass',value='123456')
model = 'shell'
args = 'touch /root/abcdppppppppppp.txt'

hs = inventory.get_hosts()
hosts = []
for h in hs:
    hosts.append(str(host))

ans = AnsibleRunner()
ans.run_modle(inventory=inventory,host_list=hosts,loader=loader,variable_manager=variablemanager,module_name=model,module_args=args)
