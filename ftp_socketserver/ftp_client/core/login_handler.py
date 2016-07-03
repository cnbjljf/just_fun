#!/usr/bin/env python
"""
这个模块用来处理用户登陆的，ftp 客户端
"""
import socket
import hashlib
import os
import sys
import json
path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )
from conf import settings, templates
from core import record_log 


class login_handler_cli( object ):
    def __init__(self):
        self.ip_port = settings.sets['ip'], settings.sets['port']
        self.ss = socket.socket( )
        self.ss.connect( self.ip_port )
        self.encry=settings.sets['encryption']

    def send_user_info(self,):
        """
        这个用来提供用户登陆的，与服务器进行交互。
        :param username:
        :param passwd:
        :return:
        """
        jiami_dict={
        'md5':hashlib.md5,
        'sha512':hashlib.sha512,
        }
        i=0
        while i<3:
            print("Input your username:")
            username=input('==>')
            #username='yq'
            print("Input your password:")
            passwd=input("==>")
            #passwd='123'
            logger=record_log.handler_log(username)
            encry=jiami_dict.get(self.encry)()
            encry.update(passwd.encode('utf8'))
            user_info={'type':'auth','username':username,'passwd':encry.hexdigest(),}
            user_info=json.dumps(user_info)
            self.ss.send(bytes(user_info,'utf8'))
            sever_response=self.ss.recv(100)
            print(str(sever_response.decode()))
            if str(sever_response.decode())=='true':
                print("login in ftp system  is sucessfully!!")
                logger.info("login in ftp system  is sucessfully!!")
                return True
            else:
                print("error username or password!!")
                logger.error("error username or password!!")
                i+=1
        return False

'''
lhc=login_handler_cli()
lhc.send_user_info('ljf','123')
'''
