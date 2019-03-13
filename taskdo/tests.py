from django.test import TestCase

# Create your tests here.


from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.inventory.host import Host,Group
from collections import namedtuple

loader = DataLoader()
inventory = InventoryManager(loader=loader,sources=['/root/OpsAuto/conf/hostslist'])
host = inventory.get_host(hostname='192.168.205.10')
variablemanager = VariableManager(loader=loader,inventory=inventory)
#variablemanager.get_vars(host=host)
#variablemanager.set_host_variable(host=host, varname='ansible_ssh_pass', value='123456')

Options = namedtuple('options', ['connection', 'module_path', 'forks', 'timeout', 'remote_user',
                                 'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args',
                                 'sftp_extra_args',
                                 'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass',
                                 'verbosity',
                                 'check', 'listhosts', 'listtasks', 'listtags', 'syntax', 'diff'])


options = Options(connection='smart', module_path=None, forks=5, timeout=10,
                       remote_user='root', ask_pass=False, private_key_file=None, ssh_common_args=None,
                       ssh_extra_args=None,
                       sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
                       become_user='root', ask_value_pass=False, verbosity=None, check=False, listhosts=False,
                       listtasks=False, listtags=False, syntax=False, diff=True)

#hosts = inventory.get_hosts()

play_source = dict(name="Ansible Play",
                   hosts=['192.168.205.10'],
                   gather_facts='no',
                   tasks=[dict(action=dict(module='shell', args='touch /root/aaaaaaaaaa.txt')),
                          ]
                   )

passwords = dict()
play = Play().load(play_source, variable_manager=variablemanager, loader=loader)

class ModelResultsCollector(CallbackBase):
    """
    重写callbackBase类的部分方法
    """
    def __init__(self, *args, **kwargs):
        super(ModelResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}
    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result
    def v2_runner_on_ok(self, result):
        self.host_ok[result._host.get_name()] = result
    def v2_runner_on_failed(self, result):
        self.host_failed[result._host.get_name()] = result

callback = ModelResultsCollector()


tqm = TaskQueueManager(inventory=inventory,variable_manager=variablemanager,loader=loader,options=options,passwords=passwords,stdout_callback=callback,
        )

result = tqm.run(play)

result_raw = {'success':{},'failed':{},'unreachable':{}}
for host,result in callback.host_ok.items():
    result_raw['success'][host] = result._result
for host,result in callback.host_failed.items():
    result_raw['failed'][host] = result._result

print(result_raw)
