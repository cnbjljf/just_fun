#/usr/bin/env python
"""
这个模块主要用来负责处理对指定的服务器进行批量执行命令，上传下载文件
"""
import paramiko
import sys,os,getopt
path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )
from conf import paramiko_conf
from core import record_log


class Batch_Manage(object):
    def __init__(self,pkey_file):
        self.pkey_file=pkey_file
        username=os.popen('echo $USER').read()
        self.username=username.split('\n')[0]
        self.result_log=paramiko_conf.result_log_path

    def ssh_cmd(self,host,port,user,auth_method,password=None,cmd=None):
        '''
        这个主要用来处理批量执行命令的
        :cmd : 要执行的命令
        '''
        rrlog=record_log.handler_log(self.username, self.result_log)
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.load_system_host_keys()
        #打印debug信息
		#paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)
        if auth_method=='password':
            s.connect(host,port,username=user,password=password,timeout=3)
        else:
            key = paramiko.RSAKey.from_private_key_file(self.pkey_file)
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

    def sftp_put(self,host,port,user,auth_method,lfile,rfile,passwd=None):
        """
        这个方法用来处理上传文件的
        :param host: 要连接的主机
        :param port: 要连接主机的端口号
        :param user: 登陆的用户名
        :param auth_method:
        :param lfile: 本地文件
        :param rfile: 远端文件
        :param passwd: 登陆的密码
        :return: True
        """
        t = paramiko.Transport((host,port))
        print("\033[32m I put %s to %s now,please waite a moment .....\n\n\033[0m"%(lfile,host))
        #如果有密码，那么就走密码登陆的这个方式
        if passwd:
            t.connect(username=user,password=passwd)
        else:
            key=paramiko.RSAKey.from_private_key_file(self.pkey_file)
            t.connect(username=user,pkey=key)
        sftp=paramiko.SFTPClient.from_transport(t)
        sftp.put(lfile,rfile)
        print(sftp.stat(rfile))
        #self.rlog.info(sftp.stat(rfile))
        t.close()
        return True


    def sftp_down(self,host,port,user,auth_method,rfile,lfile,passwd=None):
        """
        这个方法用来处理下载文件的
        :param host: 要连接的主机
        :param port: 要连接主机的端口号
        :param user: 登陆的用户名
        :param auth_method:
        :param lfile: 本地文件
        :param rfile: 远端文件
        :param passwd: 登陆的密码
        :return: True
        """
        print("\033[32m I down %s from %s now,please waite a moment .....\033[0m\n\n"%(rfile,host))
        t = paramiko.Transport((host,port))
        if passwd:
            t.connect(username=user,password=passwd)
        else:
            key=paramiko.RSAKey.from_private_key_file(self.pkey_file)
        sftp=paramiko.SFTPClient.from_transport(t)
        sftp.get(rfile,lfile)
        #这个用来重命名文件的，避免会把原来的文件名覆盖
        os.rename(lfile,lfile+'%s'%host)
        print(sftp.stat(rfile))
        #self.rlog.info(sftp.stat(rfile))
        t.close()
        return True



