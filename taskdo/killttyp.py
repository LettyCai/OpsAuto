# -*- coding: utf-8 -*-
__author__ = 'clj'
__date__ = '2019/3/13 16:18'


from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.inventory.host import Host,Group
from collections import namedtuple
from ansible_call import AnsibleRunner,MyInventory

loader = DataLoader()
inventory = InventoryManager(loader=loader,sources=['/root/OpsAuto/conf/hostslist'])
host = inventory.get_host(hostname='192.168.56.102')
variablemanager = VariableManager(loader=loader, inventory=inventory)
variablemanager.set_host_variable(host=host, varname='ansible_ssh_password', value='123456')
model = 'shell'
args = 'touch /root/abcd.txt'

ans = AnsibleRunner(variablemanager=variablemanager,hosts=hosts)
hosts = inventory.get_hosts()
ans.run_modle(hosts,model,args)
