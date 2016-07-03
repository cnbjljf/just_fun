#!/usr/bin/env python

import os
import subprocess
import sys
import re
import socketserver
import json


path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )

from conf import settings
from conf import login_user
from core import login_handler
from core import record_log
from core import account_caozuo


#
class ftpserver(socketserver.BaseRequestHandler):
#class ftpserver(object):
    """
    用来处理ftp服务用的以及接受网络数据的
    """
    def begin(self,username,passwd):
        self.ac=account_caozuo.login_check(username)
        return self.ac.judge_passwd(username,passwd)

    def recv_alldata(self):
        """
        用户接受数据的
        :return:
        """
        recv_data=self.request.recv(8192)
        if len(recv_data) > 0 :
            return recv_data
        else:
            return None

    def send_alldata(self,data_content):
        """
        用来发送数据的
        :return:
        """
        return self.request.send(bytes(data_content,'utf8'))

    def handle(self):
        #def judge_action(self):
        """
        这个用来判断用户动作的
        :return:
        """
        global password,username
        cur_dir=None
        while True:
            ret=self.recv_alldata()
            if ret:ret=json.loads(str(ret.decode()))
            if ret.get('type')=='auth':
                password=ret.get('passwd')
                username=ret.get('username')
                if self.begin(username,password):
                    print()
                    if not os.path.exists('/home/%s'%username):
                        os.mkdir('/home/%s'%username)
                    #self.logger=record_log.handler_log(self.username)
                    print('login the ftp system!!')
                    self.send_alldata('true')
                else:
                    self.send_alldata('Flase')
                   
            else:
                if not cur_dir:
                    cur_dir="/home/%s"%username
                self.action=ret.get('action')
                self.file_name=ret.get('filename')
                if self.action:
                    if self.action=='put' or self.action=='get':
                        #self.logger.info('%s %s'%(self.action,self.file_name))
                        if hasattr( ftpserver, self.action ):
                            func = getattr( ftpserver, self.action )
                            func( self, self.file_name,cur_dir )
                    else:
                        #self.logger.info("%s %s"%(self.action,cur_dir))
                        if hasattr( ftpserver, self.action):
                            func=getattr(ftpserver, self.action)
                            cur_dir=func(self,cur_dir)



    def check_quota(self,username,file_size):
        """
        这个用来去判断用户的磁盘配额是否超过了设定值
        用户磁盘配额默认是500M，这个在创建的时候已经创建好累
        :file_size:要上传的文件大小
        :return: True 代表还有空间可以使用
        """
        file_size=int(file_size)/1024/1024
        home_dir='/home/%s'%username
        user_quota=int(login_user.user_info[username].get('quota'))
        #统计当前用户的宿主目录有多大
        cur_home_size=subprocess.Popen("du -sh %s |awk '{print $1}'"%home_dir,shell=True,stdout=subprocess.PIPE)
        cur_home_size=str(cur_home_size.stdout.read().decode().split('\n')[0])
        print('user_quota M',user_quota)
        #if int(cur_home_size)+int(file_size) < int(user_quota):
        #    return True
        #else:
        #    return False
        cur_home_size_unit=cur_home_size[-1]
        c=re.search('^\d+\.?\d+',cur_home_size)
        if c:
           cur_home_size=c.group()
           print('cur_home_size',cur_home_size)
        if cur_home_size_unit=='M':
            if user_quota > float(cur_home_size)+float(file_size):
                return True
        #这个user_quota-1的目的在于因为当前宿主目录本身不超过1M，所以减去1后就是当前宿主目录最大能用的容量
        elif cur_home_size_unit=='K' and user_quota-1 >int(file_size): return True
        elif cur_home_size_unit=='G':
            if user_quota <= int(cur_home_size)*1024+file_size:
                return False



    def recover_schedule(self):
        '''
        这个主要用来处理断点续传的功能
        :return:
        '''
        ret=self.recv_alldata()
        print(str(ret.decode()))
        if str(ret.decode())=='recover':
            self.send_alldata('ok')
            reply_data=self.recv_alldata()
            reply_data=json.loads(reply_data)
            return reply_data
        else:
            ret={'action':'xxx'}
            self.send_alldata('no ok')
            return ret


    def put(self,file_name,cur_dir):
        """
        主要负责对文件上传的操作
        :return:
        """
        print( 'Now Your are put file' )
        os.chdir(cur_dir)
        ret=self.recover_schedule()
        if ret.get('action')=='put':
            file_name=ret.get('filename')
            jishuqi=ret.get('jishuqi')
            file_size=ret.get('file_size')
            file_name=file_name+'.tmp'
            f=open(file_name,'wb')
            with jishuqi<int(file_size):
                file_content=self.recv_alldata()
                jishuqi+=len(file_content)
                f.write(file_content)
            new_filename=file_name.split('.tmp')[0]
            #把tmp文件名改回原来正常的文件名
            os.rename(file_name,new_filename)
            f.close()
            #self.logger.info('file had puted!!')
            print("put finish!!")
            return True

        client_data=self.recv_alldata()
        print(str(client_data.decode()))
        if str(client_data.decode()).startswith('file size'):
            file_size=str(client_data.decode()).split(':')[1]
            if not self.check_quota(username,file_size):
                self.send_alldata('the file size too large,your disk quota can not hold it!!')
                #self.logger.error('the file size too large,disk quota can not hold it!')
                print('the file size too large,disk quota can not hold it!')
                return False
            self.send_alldata('be ready')
            print('\\\\\\\\\\')
            print('file size',file_size)
            print('file name',file_name)
        #这个用来统计当前接受的大小
        jishuqi=0
        #定义一个临时文件名
        file_name=file_name+'.tmp'
        f=open(file_name,'wb')
        print('---begin recv file---')
        #判断当前接受的数据是否比要接受的数据大
        while jishuqi < int(file_size):
            file_content=self.recv_alldata()
            jishuqi+=len(file_content)
            f.write(file_content)
        new_filename=file_name.split('.tmp')[0]
        #把tmp文件名改回原来正常的文件名
        os.rename(file_name,new_filename)
        f.close()
        #self.logger.info('file had puted!!')
        print("put finish!!")
        return True


    def get(self, filename , cur_dir):
        """
        主要负责对文件下载的操作
        :return:
        """
        print( 'Now your download file %s'%filename )
        os.chdir(cur_dir)
        ret=self.recover_schedule()
        if ret.get('action')=='get':
            file_name=ret.get('filename')
            jishuqi=ret.get('jishuqi')
            file_size=ret.get('file_size')
            f=open(file_name,'rb')
            f.seek(jishuqi,0)
            for line in f:
                self.request.send(line)
            print("\t\ndownload finish!!")
            return True

        # self.conn.send( bytes( 'down the file', 'utf8' ) )
        f = open( filename, 'rb')
        #seek()方法呢，后面的是表示从末端开始取值，值的大小为第一个数字，目前为0
        #f.seek( 0, 2 )
        #file_size = f.tell( )
        #f.seek( 0, 0 )
        file_size=os.path.getsize(filename)
        msg_file_siz = "file size : %s" %file_size
        self.send_alldata(msg_file_siz)
        reply_data = self.recv_alldata()
        f=open( filename , 'rb')
        if str( reply_data.decode( ) ) == 'be ready':
            for line in f:
                self.request.send( line )
        #self.logger.info('file had down!!')
        print("download finish!!")
        return True

    def ls(self,cur_dir):
        """
        主要负责对执行用户的命令。
        """
        #读取用户配置信息，然后找到宿主目录
        home_dir="/home/%s"%username
        #读取出用户需要切换或者删除等文件路径
        #创建宿主目录
        if not os.path.exists(home_dir):
            os.mkdir(home_dir)
        print('cur_dir',cur_dir)
        os.chdir(cur_dir)
        #匹配用户输入的哪个命令
        self.send_alldata('be ready')
        reply_data=self.recv_alldata()
        if str( reply_data.decode( ) ) == 'ok':
            print("%s %s"%(self.action,self.file_name))
            if self.action=='cd':
                #提取目标文件或者路径
                direc=self.file_name
                #用来拼接路径，把相对目录拼接成绝对路径
                direc=os.path.join(cur_dir,direc)
                if direc.startswith(home_dir) and os.path.isdir(direc):
                        os.chdir(direc)
                        result_msg='Sucessfully'
                else:
                   result_msg="you don't have permission change to other's directory!!"
                #这里把切换后的目录存储到一个变量里面，那么在执行下一个命令的时候就是以cur_dir为基准来执行
                cur_dir=os.getcwd()
            else:
                #这个用来定义命令的别名
                option_dict={
                    'ls':'ls -l',
                    'mkdir':'mkdir -p',
                    'rm':'rm -rf',
                } 
                self.action=option_dict.get(self.action)
                direc=self.file_name
                print('---cur_dir',cur_dir)
                if cur_dir:
                    os.chdir(cur_dir)
                #把要进入的目录和宿主目录拼接起来
                direc=os.path.join(home_dir,direc)
                print('directory',direc)
                #如果以宿主目录开头的路径，那么就说明是在宿主目录下
                if direc.startswith(home_dir)==True:
                    cmd=subprocess.Popen("%s %s"%(self.action,self.file_name),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    result_msg=cmd.stdout.read()
                    if  len(result_msg)<=1:
                        print(len(cmd.stderr.read()))
                        if len(cmd.stderr.read())<=1:
                            result_msg="command execute Sucessfully"
                else:
                    result_msg="You don't have permission access the direcotry(%s)!!"%direc
            print('\033[34m result_msg\033[0m',result_msg)
            if isinstance(result_msg,str):
                self.send_alldata( result_msg )
            else:
                self.request.send(  result_msg )

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

    def mkdir(self,cur_dir):
        """
        负责处理mkdir命令，直接调用self.ls方法，
        return: True
        """
        return self.ls(cur_dir)





def main():
    c=socketserver.ThreadingTCPServer(('127.0.0.1',9999),ftpserver)
    c.serve_forever()

main()
