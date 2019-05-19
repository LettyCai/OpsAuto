# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
import  paramiko
import logging
import yaml
import re
from binascii import b2a_hex, a2b_hex
logger = logging.getLogger("django")

class prpcrypt():
    '''
    用于通过密钥进行重要数据的加密解密
    '''
    def __init__(self):
        self.key = "okeqwnk2987#$%ql"
        #这里密钥key 长度必须为16（AES-128）,
        #24（AES-192）,或者32 （AES-256）Bytes 长度
        #目前AES-128 足够目前使用
        self.mode = AES.MODE_CBC

    #加密函数，如果text不足18位就用空格补足为18位，
    #如果大于16当时不是18的倍数，那就补足为18的倍数。
    def encrypt(self,text):
        cryptor = AES.new(bytes(self.key,"utf8"),self.mode,b'0000000000000000')

        length = 16
        count = len(text)
        if count < length:
            add = (length-count)
            #\0 backspace
            text = text + ('\0' * add)
        elif count > length:
            add = (length-(count % length))
            text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(bytes(text,"utf8"))
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        #所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    #解密后，去掉补足的空格用strip() 去掉
    def decrypt(self,text):
        cryptor = AES.new(bytes(self.key,encoding="utf8"),self.mode,b'0000000000000000')
        plain_text  = cryptor.decrypt(a2b_hex(text))
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


class NMAPCollection():

    def collection(self,ip,password):
        # 实例化paramiko类
        jssh = paramiko.SSHClient()
        #s_conf = yaml.load(open('/hostsinfo/hostsinfo.yaml'))
        #s_cmds = s_conf['hostsinfo']['syscmd_list']
        #print(s_cmds)
        # 默认添加至knowhosts文件
        jssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        result = {}
        # 配置连接
        try:
            jssh.connect(hostname=ip, port=22, username='root', password=password,timeout=5)

            #获取操作系统版本号
            #centos,redhat,redflag
            stdin, stdout, stderr = jssh.exec_command('cat /etc/redhat-release', timeout=10)
            sys_version = str(stdout.read()).strip("b'").strip(r'\n')
            #ubuntu
            if sys_version == "":
                stdin, stdout, stderr = jssh.exec_command('cat /etc/issue', timeout=10)
                sys_version = str(stdout.read())
                print(sys_version)
                sys_version=sys_version.strip("b'").strip(r'\n').strip(r'\\l').strip(r'\n')

            result['sys_version'] = sys_version

            #获取主机名
            stdin, stdout, stderr = jssh.exec_command('hostname', timeout=10)
            host_name = str(stdout.read())
            result['host_name'] = self.trans(host_name)

            #获取mac地址
            stdin, stdout, stderr = jssh.exec_command('cat /sys/class/net/[^vtlsb]*/address', timeout=10)
            mac = str(stdout.read())
            mac = self.trans(mac)
            result['host_mac'] = mac

            # 获取序列号
            stdin, stdout, stderr = jssh.exec_command('dmidecode -s system-serial-number', timeout=10)
            result['serial_number'] = self.trans(str(stdout.read()))

            # 获取产品类型
            stdin, stdout, stderr = jssh.exec_command('dmidecode -s system-product-name', timeout=10)
            result['product_name'] = self.trans(str(stdout.read()))

            result['status'] = 'success'
        except Exception as e:
            result["status"] = "failed"
            result["res"] = str(e)

        return result

    def mac_trans(self,mac):
        '''
            转化mac地址，将传递到mac进行数据格式的转换
            :param mac:
            :return:
            '''
        if mac:
            mac_lst = mac.split("\n")
            for item in mac_lst:
                item.replace(b":",b'').replace(b"000000000000", b'').replace(b"00000000", b'')
                mac_res.append(item)
            mac_string = b"_".join(mac_res)
            return mac_string
        else:
            return ""

    def trans(self,str):
        str = str.strip("b'")
        str = str.strip(r'\n')
        return str

    def getsysversion(version_list):
        '''
        提取系统版本
        :param version_list:
        :return:
        '''
        for version_data in version_list:
            v_data_lst = re.findall(b"vmware|centos|linux|ubuntu|redhat|\d{1,}\.\d{1,}", version_data, re.IGNORECASE)
            if v_data_lst:
                if len(v_data_lst) > 1:
                    v_data = b" ".join(v_data_lst)
                    break
            else:
                v_data = ""
        return v_data

class ListGenerate():
    def generate_hostslist(self):
        """
        生成ansible hostslist文件
        :return:None
        """
        #获取所有主机组
        groups = HostGroup.objects.all()

        contents = ""

        #写入主机组信息
        for group in groups:
            contents = contents + "[" + group.group_name + "]" + "\n"
            hosts = group.host_set.all()
            #写入该组所有主机信息
            for host in hosts:
                contents = contents + host.ip + "\n"

        #将所有信息写入hostslist文件
        with open("/root/OpsAuto/conf/hostslist_test", 'w') as f:
            f.write(contents)


if __name__ == '__main__':
    password = '123456'
    print("password============")
    prp = prpcrypt()
    password = prp.encrypt(password)
    print(password)
    password = prp.decrypt(password)
    print("password============")
    print(password)