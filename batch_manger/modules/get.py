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

def sftp_down(host,port,user,auth_method,rfile,lfile,passwd=None,pkey_file='/root/.ssh/id_rsa'):
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
        key=paramiko.RSAKey.from_private_key_file(pkey_file)
    sftp=paramiko.SFTPClient.from_transport(t)
    sftp.get(rfile,lfile)
    #这个用来重命名文件的，避免会把原来的文件名覆盖
    os.rename(lfile,lfile+'%s'%host)
    print(sftp.stat(rfile))
    #self.rlog.info(sftp.stat(rfile))
    t.close()
    return True