# -*- coding: utf-8 -*-
"""

__author__ = 'clj'
__date__ = '2019/3/12 15:24'
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.inventory.host import Host,Group
from admin.settings.settings import BASE_DIR

class MyInventory():
    def __init__(self,resource,loader,variable_manager):
        self.resource = resource
        self.loader = DataLoader()
        self.inventory = InventoryManager(loader=self.loader,resource=['%s/conf/hostslist'%BASE_DIR])


class AnsibleRunner(object):
    def __init__(self):
        pass

    def __initializeData(self):
        # 初始化ansible
        Options = namedtuple('options',['connection','module_path', 'forks', 'timeout',  'remote_user',
                'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass', 'verbosity',
                'check', 'listhosts', 'listtasks', 'listtags', 'syntax','diff'])

        self.loader = DataLoader()
        self.options = Options(connection='smart', module_path=None, forks=100, timeout=10,
                remote_user='root', ask_pass=False, private_key_file=None, ssh_common_args=None, ssh_extra_args=None,
                sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
                become_user='root', ask_value_pass=False, verbosity=None, check=False, listhosts=False,
                listtasks=False, listtags=False, syntax=False, diff=True)

        self.passwords = dict(sshpass=None, becomepass=None)
        myinvent = MyInventory(self.resource, self.loader, self.variable_manager)
        self.inventory = myinvent.inventory
        self.variable_manager = myinvent.variable_manager
        
        def run_modle(self,host_list,module_name,module_args):
            #
                    run module from andible ad-hoc.
                    module_name: ansible module_name
                    module_args: ansible module args
            #
            play_source = dict( name="Ansible Play",
                hosts=host_list,
                gather_facts='no',
                tasks=[dict(action=dict(module=module_name, args=module_args))])

            play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
            tqm = none
            # if self.redisKey:self.callback = ModelResultsCollectorToSave(self.redisKey,self.logId)
            # else:self.callback = ModelResultsCollector()
            self.callback = ModelResultsCollector()
            import traceback
            try:
                tqm = TaskQueueManager(
                    inventory=self.inventory,
                    variable_manager=self.variable_manager,
                    loader=self.loader,
                    options=self.options,
                    passwords=self.passwords,
                    stdout_callback="minimal",
                )
                tqm._stdout_callback = self.callback
                constants.HOST_KEY_CHECKING = False  # 关闭第一次使用ansible连接客户端是输入命令
                tqm.run(play)
            except Exception as err:
                print(traceback.print_exc())
                # DsRedis.OpsAnsibleModel.lpush(self.redisKey,data=err)
                # if self.logId:AnsibleSaveResult.Model.insert(self.logId, err)
            finally:
                if tqm is not None:
                    tqm.cleanup()

"""