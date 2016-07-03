#/usr/bin/env python
"""
这个模块主要用来负责处理对指定的服务器进行批量执行命令
"""
import paramiko
import sys,os,getopt
path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )
from conf import paramiko_conf
from core import record_log


username=os.popen('echo $USER').read()
username=username.split('\n')[0]
result_log=paramiko_conf.result_log_path

def ssh_cmd(host,port,user,auth_method,passwd=None,cmd=None,pkey_file='/root/.ssh/id_rsa'):
    '''
    这个主要用来处理批量执行命令的
    :cmd : 要执行的命令
    '''
    rrlog=record_log.handler_log(username, result_log)
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.load_system_host_keys()
    #打印debug信息
    #paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)
    if passwd:
        s.connect(host,port,username=user,password=passwd,timeout=3)
    else:
        key = paramiko.RSAKey.from_private_key_file(pkey_file)
        s.connect(host,port,user,key,timeout=3)
    stdin,stdout,stderr = s.exec_command(cmd)
    result = stdout.read().decode(),stderr.read().decode()
    print('\033[32m======================= the result from %s ======================\033[0m'%host)
    #with open(self.result_log,'w') as f:
    #    f.write(result)
    rrlog.info("%s %s"%(host,str(result)))
    for a in result:
        print(a)
    s.close()