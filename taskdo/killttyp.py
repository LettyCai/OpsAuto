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


class AnsibleRunner(object):
    """
        This is a General object for parallel execute modules.
        """

    def __init__(self, logId=None, *args, **kwargs):
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
        #self.loader = DataLoader()


        self.options = Options(connection='smart', module_path=None, forks=100, timeout=10,
                               remote_user='root', ask_pass=False, private_key_file=None, ssh_common_args=None,
                               ssh_extra_args=None,
                               sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
                               become_user='root', ask_value_pass=False, verbosity=None, check=False, listhosts=False,
                               listtasks=False, listtags=False, syntax=False, diff=True)

        self.passwords = dict(sshpass=None, becomepass=None)


    def run_modle(self,inventory,variable_manager,loader,host_list,module_name,module_args):
        """
            run module from andible ad-hoc.
            module_name: ansible module_name
            module_args: ansible module args
        """

        play_source = dict(name="Ansible Play",
                           hosts=host_list,
                           gather_facts='no',
                           tasks=[dict(action=dict(module=module_name, args=module_args))])

        play = Play().load(play_source,variable_manager=variable_manager,loader=loader)
        # tqm = None
        # if self.redisKey:self.callback = ModelResultsCollectorToSave(self.redisKey,self.logId)
        # else:self.callback = ModelResultsCollector()
        callback = ModelResultsCollector()
        import traceback
        # try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
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
        for host, result in callback.host_unreachable.items():
            result_raw['unreachable'][host] = result._result

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
variablemanager.set_host_variable(host=host,varname='ansible_ssh_pass',value='123456')
model = 'shell'
args = 'touch /root/abcdppppppppppp.txt'

hs = inventory.get_hosts()
print(hs)
hosts = []
for host in hs:
    hosts.append(host)
print(hosts)

#hosts = ['192.168.205.10','192.168.205.11']

ans = AnsibleRunner()
ans.run_modle(inventory=inventory,host_list=hosts,loader=loader,variable_manager=variablemanager,module_name=model,module_args=args)
