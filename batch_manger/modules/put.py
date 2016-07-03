#/usr/bin/env python
"""
这个模块主要用来负责处理对指定的服务器进行批量执行上传 file
"""
import paramiko
import sys,os,getopt
path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )
from conf import paramiko_conf
from core import record_log

def sftp_put(host,port,user,auth_method,lfile,rfile,passwd=None,pkey_file='/root/.ssh/id_rsa'):
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
            key=paramiko.RSAKey.from_private_key_file(pkey_file)
            t.connect(username=user,pkey=key)
        sftp=paramiko.SFTPClient.from_transport(t)
        sftp.put(lfile,rfile)
        print(sftp.stat(rfile))
        #self.rlog.info(sftp.stat(rfile))
        t.close()
        return True
