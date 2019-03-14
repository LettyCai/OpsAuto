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
#from ansible_call import AnsibleRunner,MyInventory

class MyInventory():
    def __init__(self):
        # self.resource = resource
        self.loader = DataLoader()
        self.inventory = InventoryManager(loader=self.loader, sources=['/root/OpsAuto/conf/hostslist'])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

class ModelResultsCollector(CallbackBase):
    # 改写返回方法
    def __init__(self, *args, **kwargs):
        super(ModelResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class AnsibleRunner(object):
    """
        This is a General object for parallel execute modules.
        """

    def __init__(self, logId=None, *args, **kwargs):
        self.inventory = None
        # self.variable_manager = None
        self.loader = None
        self.options = None
        self.passwords = None
        self.callback = None
        self.__initializeData()
        self.results_raw = {}
        self.redisKey = None
        self.logId = logId

    def __initializeData(self):
        # 初始化ansible
        Options = namedtuple('options', ['connection', 'module_path', 'forks', 'timeout', 'remote_user',
                                         'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args',
                                         'sftp_extra_args',
                                         'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass',
                                         'verbosity',
                                         'check', 'listhosts', 'listtasks', 'listtags', 'syntax', 'diff'])

        self.loader = DataLoader()
        self.options = Options(connection='smart', module_path=None, forks=100, timeout=10,
                               remote_user='root', ask_pass=False, private_key_file=None, ssh_common_args=None,
                               ssh_extra_args=None,
                               sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
                               become_user='root', ask_value_pass=False, verbosity=None, check=False, listhosts=False,
                               listtasks=False, listtags=False, syntax=False, diff=True)

        self.passwords = dict(sshpass=None, becomepass=None)
        myinvent = MyInventory()
        self.inventory = myinvent.inventory
        self.variable_manager = myinvent.variable_manager

    def run_modle(self, host_list, variable_manager, module_name, module_args):
        """
            run module from andible ad-hoc.
            module_name: ansible module_name
            module_args: ansible module args
        """

        play_source = dict(name="Ansible Play",
                           hosts=['192.168.205.10'],
                           gather_facts='no',
                           tasks=[dict(action=dict(module='shell', args='touch /root/aaaaaaaaaa.txt'))])

        play = Play().load(play_source, variable_manager=variable_manager, loader=self.loader)
        # tqm = None
        # if self.redisKey:self.callback = ModelResultsCollectorToSave(self.redisKey,self.logId)
        # else:self.callback = ModelResultsCollector()
        callback = ModelResultsCollector()
        import traceback
        # try:
        tqm = TaskQueueManager(
            inventory=self.inventory,
            variable_manager=variable_manager,
            loader=self.loader,
            options=self.options,
            passwords=self.passwords,
            stdout_callback=callback,
        )
        # constants.HOST_KEY_CHECKING = False  # 关闭第一次使用ansible连接客户端时输入命令
        result = tqm.run(play)


        result_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in callback.host_ok.items():
            result_raw['success'][host] = result._result
        for host, result in callback.host_failed.items():
            result_raw['failed'][host] = result._result

        print(result_raw)

    #  except Exception as err:
    #      print(traceback.print_exc())
    # DsRedis.OpsAnsibleModel.lpush(self.redisKey,data=err)
    # if self.logId:AnsibleSaveResult.Model.insert(self.logId, err)
    #  finally:
    #      if tqm is not None:
    #   tqm.cleanup()






loader = DataLoader()
inventory = InventoryManager(loader=loader,sources=['/root/OpsAuto/conf/hostslist'])
host = inventory.get_host(hostname='192.168.205.10')
variablemanager = VariableManager(loader=loader, inventory=inventory)
variablemanager.set_host_variable(host=host, varname='ansible_ssh_password', value='123456')
model = 'shell'
args = 'touch /root/abcd.txt'

ans = AnsibleRunner()
hosts =['192.168.56.102']
ans.run_modle(hosts,variablemanager,'shell','touch /root/aaaaaaaaaa.txt')



