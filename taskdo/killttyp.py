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

class AnsibleRun():
    def run(self):
        loader = DataLoader()
        inventory = InventoryManager(loader=loader,sources=['/root/OpsAuto/conf/hostslist'])
        host = inventory.get_host(hostname='10.0.2.15')
        variablemanager = VariableManager(loader=loader,inventory=inventory)
        variablemanager.get_vars(host=host)
        variablemanager.set_host_variable(host=host, varname='ansible_ssh_password', value='123456')

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

        hosts = inventory.get_hosts()

        play_source = dict(name="Ansible Play",
                           hosts=['10.0.2.15'],
                           gather_facts='no',
                           tasks=[dict(action=dict(module='shell', args='ls -a'))])

        passwords = dict()
        play = Play().load(play_source, variable_manager=variablemanager, loader=loader)
        tqm = TaskQueueManager(inventory=inventory,variable_manager=variablemanager,loader=loader,options=options,passwords=passwords,
                   # stdout_callback="minimal",
                )

        result = tqm.run(play)
        print(result)
        



def main():
    ans = AnsibleRun()
    AnsibleRun.run()

if __name__ == "__main__":
    sys.exit(main())