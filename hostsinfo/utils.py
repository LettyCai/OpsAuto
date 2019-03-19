from Crypto.Cipher import AES
import  paramiko
import logging
import yaml
logger = logging.getLogger("django")

class prpcrypt():
    def __init__(self):
        self.key = "okeqwnk2987#$%ql"
        # 这里密钥key 长度必须为16（AES-128）,
        # 24（AES-192）,或者32 （AES-256）Bytes 长度
        # 目前AES-128 足够目前使用
        self.mode = AES.MODE_CBC

        # 加密函数，如果text不足18位就用空格补足为18位，
        # 如果大于16当时不是18的倍数，那就补足为18的倍数。
        def encrypt(self, text):
            cryptor = AES.new(bytes(self.key, "utf8"), self.mode, b'0000000000000000')

            length = 16
            count = len(text)
            if count < length:
                add = (length - count)
                # \0 backspace
                text = text + ('\0' * add)
            elif count > length:
                add = (length - (count % length))
                text = text + ('\0' * add)
            self.ciphertext = cryptor.encrypt(bytes(text, "utf8"))
            # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
            # 所以这里统一把加密后的字符串转化为16进制字符串
            return b2a_hex(self.ciphertext)

        # 解密后，去掉补足的空格用strip() 去掉
        def decrypt(self, text):
            cryptor = AES.new(bytes(self.key, encoding="utf8"), self.mode, b'0000000000000000')
            plain_text = cryptor.decrypt(a2b_hex(text))
            return plain_text

class J_do(object):

    def __init__(self):
        self.result = {"info": info}

    def pass_do(self,login_info,cmd_list=""):
        '''
        用户密码方式登录
        :param login_info:登录的信息，如：('192.168.6.11', 22, 'root', '123')
        :param cmd_list:登录机器后，需要执行的命令
        :return:
        '''
        try:
            ssh = paramiko.SSHClient()
            #允许连接不在Knowhosts文件中的主机
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #连接服务器
            ssh.connect(hostname=login_info[0],port=login_info[1],username=login_info[2],password=login_info[3],timeout=3)
            self.result["status"] = "success"
            for cmd in cmd_list:
                stdin,stdout,stderr = ssh.exec_command(cmd,timeout=10)
                std_res = stdout.read()
                self.result[cmd] = std_res
        except Exception as e:
            print(logger.exception("Use passwd ssh login exception:%s,%s" % (e, login_info)))
            self.result["status"] = "failed"
            self.result["res"] = str(e)
        return self.result


class NmapDev(object):
    '''
    扫描类：扫描获取指定网段主机等对象信息
    '''

    def try_login(self, sship_list, password_list, syscmd_list):
        '''
        尝试ssh用户密码登录，获取机器基本信息
        :param sship_list:
        :param password_list:
        :param syscmd_list:
        :return:
        '''
        password_list = password_list
        syscmd_list = syscmd_list
        if isinstance(sship_list, dict):
            ssh_tuple_list = [(ip, port) for ip, port in sship_list.items()]
        elif isinstance(sship_list, list):
            ssh_tuple_list = sship_list
        for ip, port in ssh_tuple_list:
            system_info = ""
            for password in password_list:
                if ip not in self.can_login_lst.keys():
                    login_info = (ip, int(port), 'root', password)
                    doobj = J_ssh_do(login_info)
                    res = doobj.pass_do(login_info, syscmd_list)
                    if res["status"] == "success":
                        if ip in self.not_login_lst:
                            self.not_login_lst.pop(ip)
                        sys_hostname = res["hostname"]
                        sys_mac = mac_trans(
                            res["cat /sys/class/net/[^vtlsb]*/address||esxcfg-vmknic -l|awk '{print $8}'|grep ':'"])
                        sys_sn = sn_trans(res["dmidecode -s system-serial-number"])
                        system_info = getsysversion([res["cat /etc/issue"], res["cat /etc/redhat-release"]])
                        machine_type = machine_type_trans(
                            res["dmidecode -s system-manufacturer"] + res["dmidecode -s system-product-name"])
                        print("ssh login and exec command:%s", res)
                        logger.info("ssh login and exec command:%s", res)
                        self.can_login_lst[ip] = (
                        port, password, 'root', system_info, sys_hostname, sys_mac, sys_sn, machine_type)
                    elif res["status"] == "failed" and re.search(r"reading SSH protocol banner", res["res"]):
                        # print "res res..........................",res['res']
                        print("IP:%s Connection closed by remote host,Sleep 60 (s).................. " % ip, res)
                        time.sleep(60)
                    else:
                        if ip not in self.not_login_lst.keys() and ip not in self.can_login_lst.keys():
                            self.not_login_lst[ip] = port
                        # print ip,port,password,traceback.print_exc()
        return self.can_login_lst, self.not_login_lst

class NMAPCollection():

    def collection(self,ip,password):
        # 实例化paramiko类
        jssh = paramiko.SSHClient()
        #s_conf = yaml.load(open('hostsinfo.yaml'))
        #s_cmds = s_conf['hostsinfo']['syscmd_list']
        #print(s_cmds)
        # 默认添加至knowhosts文件
        jssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 配置连接
        jssh.connect(hostname=ip, port=22, username='root', password=password)
        result = {}
        """
        for cmd in s_cmds:
            stdin, stdout, stderr = jssh.exec_command(cmd, timeout=10)
            std_res = stdout.read()
            print(std_res)
            result[cmd] = std_res
        print(result)
        """

        #获取操作系统版本号
        stdin, stdout, stderr = jssh.exec_command('cat /etc/issue', timeout=10)
        result['sys_version'] = stdout.read()
        #获取主机名
        stdin, stdout, stderr = jssh.exec_command('hostname', timeout=10)
        result['host_name'] = stdout.read()
        #获取mac地址
        stdin, stdout, stderr = jssh.exec_command('cat /sys/class/net/[^vtlsb]*/address', timeout=10)
        result['host_mac'] = stdout.read()
        # 获取序列号
        stdin, stdout, stderr = jssh.exec_command('dmidecode -s system-serial-number', timeout=10)
        result['serial_number'] = stdout.read()
        # 获取产品类型
        stdin, stdout, stderr = jssh.exec_command('dmidecode -s system-product-name', timeout=10)
        result['product-name'] = stdout.read()

        print(result)

        return result