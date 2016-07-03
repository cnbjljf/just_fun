#!/usr/bin/env python
"""
这个模块用来处理用户登陆认证的，ftp服务端
"""
import socketserver
import os
import subprocess
import sys

path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )

from core import  record_log
from conf import settings
from core import account_caozuo


class login_handler_ser( socketserver.BaseRequestHandler ):
    """
    这个类用来处理ftp服务的登陆的功能
    """

    def __init__(self):
        pass
        '''
        self.ip,self.port= settings.sets['ip'], settings.sets['port']
        self.conn=socketserver.ThreadingTCPServer((self.ip,self.port),login_handler_ser)
        self.conn.serve_forever()
        #print( self.ip_port )
        #self.ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM )
        #下面这个参数表示地址重用(socket.SOL_SOCKET,socket.SO_REUSEADDR,1),这样做了以后就不会出现地址被占用了
        #self.ss.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.ss.bind( self.ip_port )
        self.ss.listen( 5 )
        self.conn, self.addr = self.ss.accept( )
       '''

    def recv_userinfo(self):
        """
        用户接受客户端发送过来的用户登陆数据，然后去检测这些信息是否正确
        :return:
        """
        tmp = []
        ac = account_caozuo.login_check( )
        while True:

            user_info = self.request.recv( 200 )
            user_info = str( user_info.decode( ) )
            print( user_info )

            username = user_info.split( ',' )[0].split( ":" )[1]
            passwd = user_info.split( ',' )[1].split( ":" )[1]
            logger = record_log.handler_log( username )


            if ac.check_account_exist( username ):
                if ac.check_account_status( username ):
                    if ac.judge_passwd( username, passwd ):
                        print( "welcome to login the ftp system!!" )
                        logger.info( 'login system sucessfully' )
                        # 把当前登陆成功的用户写入一个文件里面，这样的话方便其他功能去调用
                        with open( 'suc_login_user.info', 'w' ) as fi:
                            fi.write( username )
                        #self.__user=username
                        self.request.send( bytes( 'true', 'utf8' ) )
                        #print(" the connection is close at authcation")
                        return True
                    else:
                        logger.info( 'password is error when login the system' )
                        print('password is error when login the system')
                        tmp.append( username )
                        print(tmp.count(username))
                        if tmp.count( username ) > 2:
                            ac.lock_account( username, 1 )
                            self.request.send( bytes( 'the account had locked', 'utf8' ) )
                            return False
                        self.request.send( bytes( 'false', 'utf8' ) )
                        continue



                else:
                    logger.info( 'the account had locked' )
                    self.request.send( bytes( 'false', 'utf8' ) )
                    return False
            else:
                logger.info( 'the account not exist!!' )
                self.request.send( bytes( 'false', 'utf8' ) )
            return False



'''
ip,port= settings.sets['ip'], settings.sets['port']
conn=socketserver.ThreadingTCPServer((ip,port),login_handler_ser)
conn.serve_forever()

lh = login_handler_ser( )
lh.recv_userinfo( )
'''