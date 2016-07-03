#!/usr/bin/env python
"""
这个模块用来实现ftp客户端上传下载文件的功能
"""
import socket
import os
import sys
import random
import json
import pickle

path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )
from conf import settings, templates


class ftpClient( object ):
    def __init__(self):
        self.ip_port = settings.sets['ip'], settings.sets['port']
        self.ss = socket.socket( )
        self.ss.connect( self.ip_port )

    def ftp_handler(self):
        """
        判断用户输入的信息来使用哪个方法
        :return:
        """
        cur_dir='~'
        pwd_dir=cur_dir
        while True:
            #这个用来显示当前目录的，做的还有bug，时间关系在后面修改了。
            self.user_input = input( "[%s(q:exit)]==>"%pwd_dir ).strip( )
            if self.user_input == 'q':
                self.ss.sendall(bytes('bye','utf8'))
                self.ss.close()
                exit('Now you close quit the system!!')
            elif not self.user_input:
                continue
            action = self.user_input.split( )[0]
            file_name = self.user_input.split( )[-1]
            ret={'type':'exec','action':action,'filename':file_name,}
            self.user_input=json.dumps(ret)
            self.ss.sendall( bytes( self.user_input, 'utf8' ) )
            print('user_input already send to perr')
            if hasattr( ftpClient, action ):
                func = getattr( ftpClient, action )
                cur_dir=func( self , file_name )
                    
    def schedule(self,file_name):
        if os.path.exists('schdule.txt'):
            print('do you want to recover last put/or down')
            yn=input('==>')
            if yn=="Y" or yn=='y':
                with open('schdule.txt','r') as sch_f:
                    schedule_info=json.load(sch_f)
                file_name=schedule_info.get('filename')
                action=schedule_info.get('action')
                user_input='%s %s'%(action,file_name)
                self.ss.send(bytes(user_input,'utf8'))
                self.ss.send(bytes('recover'))
                reply_data=self.ss.recv(8192)
                if str(reply_data.decode())=='ok':
                    self.ss.send(bytes(schedule_info,'utf8'))
                os.remove('schdule.txt')
        else:
            self.ss.send(bytes('no recover','utf8'))  
            self.ss.recv(8192)




    def get(self, file_name ):
        """
        处理下载文件的模块
        :param file_name: 要下载的文件名
        :return: True
        """
        self.schedule(file_name)
        reply_data = self.ss.recv( 8192 )
        if reply_data.decode( ).startswith( "file size" ):
            self.ss.sendall( bytes( "be ready", 'utf8' ) )
            #print( 'reply_data:', reply_data.decode( ) )
            msg_size =int( str( reply_data.decode( ) ).split( ":" )[-1])
            print( "msg_size", msg_size )
        #这个用来判断当前是否有文件存在了
        if os.path.exists(file_name):
            os.remove(file_name)
        file_name=file_name+'.tmp'
        f=open( file_name, 'ab')
        jishuqi = 0
        while 1:
            try:
                reply_data = self.ss.recv( 8192 )
                jishuqi = jishuqi+len( reply_data )
                transfer_percent=int(jishuqi/msg_size*100)
                #print(transfer_percent)
                self.show_speed(transfer_percent)
                f.write(reply_data)
                if int(jishuqi) >=  int(msg_size) :
                    print('\033[32m\n\tfile had download !!\033[0m')
                    break
            except (KeyboardInterrupt,BrokenPipeError,ConnectionResetError) as e:
                with open('schdule.txt','w') as sch_f:
                    schdule_status={'action':'get','jishuqi':jishuqi,'filename':file_name,'file_size':msg_size,}
                    json.dump(schdule_status,sch_f)
                    return False
        new_filename=file_name.split('.tmp')[0]
        os.rename(file_name,new_filename)
        print('')
        f.close()
        return True

    def put(self, file_name ):
        """
        是用来执行上传文件的功能
        :param file_name: 要上传的文件名
        :return: true
        """
        #f.seek( 0, 2 )
        #获取文件大小的
        #file_size = f.tell( )
        #f.seek( 0, 0 )

        if not os.path.exists(file_name):
            print("the file not exist %s"%file_name)
            return False
        self.schedule(file_name)
        file_size=os.path.getsize(file_name)
        jishuqi=0
        msg_file_size="file size : %s"%file_size
        self.ss.send( bytes( msg_file_size, 'utf8' ) )
        recv_data= self.ss.recv(100)
        print('wether ready :',str(recv_data.decode()))
        if str(recv_data.decode()) ==  'be ready':
            f = open( file_name, 'rb' )
            #这里读一行发送一行的速度有点慢，需要改进的地方
            print('---begin send file')
            try:
                for line in f:
                    jishuqi=jishuqi+len(line)
                    transfer_percent=int(jishuqi/file_size*100)
                    self.show_speed(transfer_percent)
                    self.ss.send(line)
                f.close()
            except (KeyboardInterrupt,BrokenPipeError) as e:
                with open('schdule.txt','w') as sch_f:
                    schdule_status={'action':'get','jishuqi':jishuqi,'filename':file_name,'file_size':file_size,}
                    json.dump(schdule_status,sch_f)
                    return False
        elif str(recv_data.decode()).startswith('the file'):
           print('\033[31m the file size too large,disk quota can not hold it  \033[0m')
           return False
        print('\033[32m\n\tfile had Put !!\033[0m')
        return True

    def show_speed(self,percent):
        """
        用来打印下载进度条的信息
        :param percent: 已经传输内容占总内容的百分比
        :return:
        """
        #定义一个初试值，用来做进度条宽度的
        bar_length=40
        #计算需要打印多少个#号
        hashes = '#' * int(percent/100.0 * bar_length)
        #计算需要打印多少个空格
        spaces = ' ' * (bar_length - len(hashes))
        #屏幕输出，通过\r参数能够原有的内容（既上一次的输出内容）进行覆盖
        sys.stdout.write("\rPercent: [%s] %d%%"%(hashes + spaces, percent))
        #下面这个flush的话，会把进度条在下一行重新打印出来,又好像不对，我也忘了这个参数了
        sys.stdout.flush()


    def ls(self,file_name):
        """
        这个用来执行ls参数的
        :file_name: means None
        :return:
        """
        print()
        server_data=self.ss.recv(8192)
        if str(server_data.decode())=='be ready':
            self.ss.sendall(bytes('ok','utf8'))
        server_data=self.ss.recv(8192)
        if str(server_data.decode())=="Sucessfully":
            return file_name
        else:print('\033[33m',str(server_data.decode()),'\033[0m')
        return True


    def rm(self,file_name):
        """
        用来执行rm命令参数的
        :param file_name: 要切换到的目录下面
        :return: True
        """
        print('Your are execute rm command ,rm filename %s'%file_name)
        if self.ls(file_name):
            return True

    def cd(self,file_name):
        """
        用来执行cd命令的
        :param file_name: 要切换到的目录下面
        :return:
        """
        print('Your are execute Cd command ,cd filename %s'%file_name)
        return self.ls(file_name)

    def mkdir(self,file_name):
        """
        用来执行mkdir命令
        :param file_name: 要切换的目录下面
        :return : True
        """
        print('Your are execute mkdir command ,mkdir filename %s'%file_name)
        if self.ls(file_name):
            return True
        



'''
sc = ftpClient( )
sc.ftp_handler( )
sc.ss.close( )
'''
