#!/usr/bin/env python
"""
这个模块用来处理ftp服务的上传下载以及切换目录的功能。
"""
import socket
import os
import subprocess
import sys
import re
import socketserver


path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )

from conf import settings, templates
from db import db_opration
from core import login_handler
from core import record_log


class ftp_handler( object):
    """
    这个类用来处理ftp服务的上传下载以及切换目录的功能
    """

    def __init__(self):
        self.ip_port = settings.sets['ip'], settings.sets['port']
        print( self.ip_port )
        #self.ss = socket.socket( )
        #self.ss.bind( self.ip_port )
        #self.ss.listen( 5 )
        #self.conn, self.addr = self.ss.accept( )
        self.lhs=login_handler.login_handler_ser()
        self.conn =socketserver.ThreadingTCPServer((self.ip_port),self.lhs)
        #self._login_user=self.lhs._user
        #print('_login_user:',_login_useru
        self.dbop=db_opration.oprateion_db()
        self.acc_info=self.dbop.db_is_file('init_account.txt','r')
        #下面这步主要是把已经成功登陆的用户提取出来
        with open('suc_login_user.info','r') as slu:
            self.login_user=slu.read()
        self.logger=record_log.handler_log(self.login_user)
        self.home_dir=self.acc_info[self.login_user].get('home_dir')

    def getinfo_from_socket(self):
        """
        这个方法主要用来获取用户输入的命令，然后调用对应的方法
        :return: None
        """
        print( 'client info-->', self.addr )
        print("*"*100)
        cur_dir='/home/%s'%self.login_user
        while True:
            print('wait to recving info....')
            client_data = self.conn.recv( 8192 )
            self.client_data=str(client_data.decode())
            print('self.client_data',self.client_data)
            if str(client_data.decode())=='bye':
                self.ss.close()
                self.logger.info('exit the ftp system')
                exit('system is closeing')
            self.action = str( client_data.decode( ) ).split( )[0]
            if self.action=='put' or self.action=='down':
                file_name = str( client_data.decode( ) ).split( )[1]
                self.logger.info('%s %s'%(self.action,file_name))
                if hasattr( ftp_handler, self.action ):
                    func = getattr( ftp_handler, self.action )
                    func( self, file_name,cur_dir )
            else:
                self.logger.info("%s %s"%(self.action,cur_dir))
                if hasattr( ftp_handler, self.action):
                    func=getattr(ftp_handler, self.action)
                    cur_dir=func(self,cur_dir)


    def check_quota(self,file_size):
        """
        这个用来去判断用户的磁盘配额是否超过了设定值
        用户磁盘配额默认是500M，这个在创建的时候已经创建好累
        :file_size:要上传的文件大小
        :return: True 代表还有空间可以使用
        """
        #这一步用来换算文件大小的
        file_size=int(file_size)/1024/1024
        home_dir=self.acc_info[self.login_user].get('home_dir')
        print('check_quota homedir',home_dir)
        user_quota=self.acc_info[self.login_user].get('quota')
        #统计当前用户的宿主目录有多大
        cur_home_size=subprocess.Popen("du -sh %s |awk '{print $1}'"%home_dir,shell=True,stdout=subprocess.PIPE)
        cur_home_size=str(cur_home_size.stdout.read().decode().split('\n')[0])
        cur_home_size_unit=cur_home_size[-1]
        print('user_quota',user_quota)
        c=re.search('^\d+\.?\d+',cur_home_size)
        if c:
           cur_home_size=c.group()
           print('cur_home_size',cur_home_size)
        if cur_home_size_unit=='M':
            print( user_quota > float(cur_home_size)+float(file_size))
            if user_quota > float(cur_home_size)+float(file_size):
                return True
        #这个user_quota-1的目的在于因为当前宿主目录本身不超过1M，所以减去1后就是当前宿主目录最大能用的容量
        elif cur_home_size_unit=='K' and user_quota-1 >int(file_size): return True
        elif cur_home_size_unit=='G':
            if user_quota <= int(cur_home_siz[0])*1024+file_size:
                return False
        




    def put(self,file_name,cur_dir):
        """
        主要负责对文件上传的操作
        :return:
        """
        print( 'Now Your are put file' )
        os.chdir(cur_dir)
        client_data=self.conn.recv(100)
        print(str(client_data.decode()))
        if str(client_data.decode()).startswith('file size'):
            file_size=str(client_data.decode()).split(':')[1]
            ret=self.check_quota(file_size)
            print('ret',ret)
            if not self.check_quota(file_size):
                self.conn.sendall(bytes('the file size too large,your disk quota can not hold it!!','utf8'))
                self.logger.error('the file size too large,disk quota can not hold it!')
                return False
            self.conn.send(bytes('be ready','utf8'))
            print('file size',file_size)
            print('file name',file_name)
        #这个用来统计当前接受的大小
        jishuqi=0
        f=open(file_name,'wb')
        #判断当前接受的数据是否比要接受的数据大
        while jishuqi < int(file_size):
            file_content=self.conn.recv(8192)
            #print(file_content)
            jishuqi+=len(file_content)
            f.write(file_content)
        f.close()
        print("put finish!!")
        return True


    def down(self, filename , cur_dir):
        """
        主要负责对文件下载的操作
        :return:
        """
        print( 'Now your download file %s'%filename )
        # self.conn.send( bytes( 'down the file', 'utf8' ) )
        f = open( filename, 'rb')
        f.seek( 0, 2 )
        file_size = f.tell( )
        #f.seek( 0, 0 )
        msg_file_siz = "file size : %s" %file_size
        self.conn.send( bytes( msg_file_siz, 'utf8' ) )
        reply_data = self.conn.recv( 50 )
        f=open( filename , 'rb')
        if str( reply_data.decode( ) ) == 'be ready':
            for line in f:
                self.conn.send( line )
        print("download finish!!")
        return True

    def ls(self,cur_dir):
        """
        主要负责对执行用户的命令。
        """
        #读取用户配置信息，然后找到宿主目录
        home_dir=self.acc_info[self.login_user].get('home_dir')
        #读取出用户需要切换或者删除等文件路径
        #创建宿主目录
        if not os.path.exists(home_dir):
            os.mkdir(home_dir)
        print('cur_dir',cur_dir)
        os.chdir(cur_dir)
        #匹配用户输入的哪个命令
        self.conn.send(bytes('be ready','utf8'))
        if str( self.conn.recv( 20 ).decode( ) ) == 'ok':
            print( "exec cmd",self.client_data)   
            if self.action=='cd':
                #提取目标文件或者路径
                direc=self.client_data.split()[1]
                #用来拼接路径，把相对目录拼接成绝对路径
                direc=os.path.join(cur_dir,direc)
                if direc.startswith(home_dir) and os.path.isdir(direc):
                        print('want to change dir:',direc)
                        os.chdir(direc)
                        result_msg="cur_path| %s"%direc
                else:
                   result_msg="you don't have permission change to other's directory!!"
                #这里把切换后的目录存储到一个变量里面，那么在执行下一个命令的时候就是以cur_dir为基准来执行
                cur_dir=os.getcwd()
            else:
                #
                direc=self.client_data.split()[-1]
                print('cur_dir',cur_dir)
                if cur_dir:
                    print('cd',cur_dir)
                    os.chdir(cur_dir)
                direc=os.path.join(home_dir,direc)
                print('directory',direc)
                if direc.startswith(home_dir)==True:
                    cmd=subprocess.Popen(self.client_data,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    result_msg=cmd.stdout.read()
                    print('result_msg',result_msg)
                    if  len(result_msg)<=1:
                        if len(cmd.stderr.read())<=1:
                            result_msg="command execute Sucessfully"
                            print('len(result_msg)<=1',result_msg)
                else:
                    result_msg="You don't have permission access the direcotry(%s)!!"%direc
            print('finally print',result_msg)
            if isinstance(result_msg,str):
                self.conn.sendall(  bytes(result_msg,'utf8') )
            else:
                self.conn.sendall(  result_msg )
          
        return cur_dir

    def cd(self,cur_dir):
        """
        负责处理cd命令，直接调用self.ls方法，在self.ls方法里面去执行对应的操作
        :return:
        """
        return self.ls(cur_dir)



    def rm(self,cur_dir):
        """
        负责处理rm命令，直接调用self.ls方法，在self.ls方法里面去执行对应的操作
        :return:
        """
        return self.ls(cur_dir)

    def mkdir(self,file_name,cur_dir):
        """
        负责处理mkdir命令，直接调用self.ls方法，
        return: True
        """
        return self.ls(cur_dir)



'''
fh = ftp_handler( )
fh.getinfo_from_socket( )
fh.ss.close()
'''
