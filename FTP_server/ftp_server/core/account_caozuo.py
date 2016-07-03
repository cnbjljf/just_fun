#!/usr/bin/env python

import pickle
import sys
import os

path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )
from conf import settings
from conf import templates
from db import db_opration
from core import record_log
import hashlib
import re


class login_check( object ):
    def __init__(self):
        '''
        open account info's file
        :return: None
        '''
        self.dbop = db_opration.oprateion_db( )
        if settings.sets['storage_engine'] == 'file':
            self.account_info = self.dbop.db_is_file( "init_account.txt", 'r' )
        elif settings.sets['storage_engine'] == 'mysql':
            self.account_info = self.dbop.db_is_mysql( )
        #print( self.account_info )

    def check_account_exist(self, username,filename='init_account.txt'):
        '''
        Testing a user name exists
        username: 要判断的用户名
        filename: 用户信息文件
        :return True or False
        '''
        self.dbop = db_opration.oprateion_db( )
        self.account_info = self.dbop.db_is_file( filename, 'r' )
        if username in self.account_info.keys( ):
            print( "the account Exist" )
            return True
        else:
            return False

    def check_account_status(self, username):
        '''
        Testing the user whether lock
        :param username:input username
        :return: True or False
        '''
        if self.account_info[username].get( 'lock' ) == 'no':
            print( 'The account does not lock' )
            return True
        else:
            print( 'The account had lock' )
            return False

    def judge_passwd(self, username, passwd,filename='init_account.txt'):
        '''
        验证密码是否正确
        :param username:输入的用户名
        :param passwd: 输入的密码
        :param filename: 用户信息文件
        :return: True or False
        '''
        self.dbop = db_opration.oprateion_db( )
        self.account_info = self.dbop.db_is_file( filename, 'r' )
        print(self.account_info[username].get( 'pwd' ),passwd)
        if self.account_info[username].get( 'pwd' ) == passwd:
            print( "Password  is True" )
            return True
        else:
            print( "Password  is False" )
            return False

    def lock_account(self, username, F):
        '''
        lock the username if F is True,else  not lock
        :param username: input username
        :param F:  Flags,if F is Ture ,then the username will be lock,else unlock
        :return:
        '''
        if F:
            self.account_info[username]['lock'] = 'yes'
            print( 'the %s had lock!!' % username )
        else:
            self.account_info[username]['lock'] = 'no'
            print( "the %s had unlock!!" % username )

        return self.dbop.db_is_file( 'init_account.txt', 'w', self.account_info )

    def find_passwd(self,username):
        """
        find account's password!!
        :param username: input username
        :return:
        """
        print(self.account_info[username]['email'])
        email=input("Input your email address ==>")

        if email==self.account_info[username]['email']:
            print("Your Password is %s"%self.account_info[username]['pwd'])
        else:
            print("Email address is Error!!")
            return False

    def change_passwd(self,username):
        """
        change your password!!
        :param username: input username
        :return:
        """
        old_passwd=input("Old Passwd ==>")
        if self.judge_passwd(username,old_passwd):
            new_passwd1=input("New Passwd ==>")
            new_passwd2=input("New Passwd ==>")
            if new_passwd1==new_passwd2:
                self.account_info[username]['pwd']=new_passwd2
                if self.dbop.db_is_file('init_account.txt','w',self.account_info):
                    print("Change Password has Sucessfully")
            else:
                print("Password not the Same!!")
                return False


    def amin_system(self):
        """
        提供管理员登陆的方法
        :return:
        """
        admin_name=input("Input admin's name ==>").strip()
        if self.check_account_exist(admin_name,filename='admin_account.txt'):
            admin_passwd=input("Input admin's Password ==>").strip()
            if self.judge_passwd(admin_name,admin_passwd,filename='admin_account.txt'):
                rlog=record_log.handler_log(admin_name)
                rlog.info("login the combat admin system")
                msg="""\033[36m
                \t1 : lock account
                \t2 : unlock account
                \t3 : del account
                \t4 ：exit
                \033[0m
                """
                print(msg)
                op_dic={
                    '1':'lock',
                    '2':'unlock',
                    '3':'del',
                    '4':exit
                }

                op=input("input opration's serial number ==>").strip()
                if op=='4':exit()
                username=input("input need opration account's name ==>").strip()
                if op in op_dic.keys() and self.check_account_exist(username):
                    rlog.info("%s the account %s"%(op_dic[op],username))
                    return  self.admin_manger(username,op_dic[op])




    def register_account(self):
        """
        这个体用普通用户注册信息用的方法
        :return: True
        """
        print('\t\t\033[44m This is Register Function\033[0m')
        F=1
        while F:
            username=input('Input Register Account Name (q:quit)==>')
            account_info = self.dbop.db_is_file( "init_account.txt", 'r' )
            if self.check_account_exist(username):
                print("Sorry,the username is exist !\nplease input another name!")
                continue
            elif username=='q' or username=='Q':
                break
            while True:
                newpasswd1=input("Input Register Account Password (First)  (q:quit)==>").strip()
                newpasswd2=input("Input Register Account Password (Second)  (q:quit)==>").strip()
                if newpasswd2=='q' or newpasswd1=='q':
                    break
                elif newpasswd1==newpasswd2:
                    hmd5=hashlib.md5()
                    hmd5.update(newpasswd1.encode('utf8'))
                elif newpasswd1!=newpasswd2:
                    print("\033[41m\tsorry,password not the same !!please try again\33[0m")
                    continue

                while True:
                    el=input("Input Register Account Email Address (q:quit)==>")
                    if el=='q' or el=='Q':
                        break
                    email=re.search("[0-9.a-z]{0,26}@[0-9.a-z]{0,20}.[0-9a-z]{0,8}",el)
                    if email:
                        email=email.group()
                        print("\033[32m Email address is ok!!\033[0m")
                    else:
                        print("\033[31m Sorry .the email format is error!!\033[0m")
                        continue
                    lc=login_check()
                    account_info=self.dbop.db_is_file('init_account.txt','r')
                    #print('Register --',account_info)
                    info={'pwd':hmd5.hexdigest(),'email':email,'lock':'no','money':''}
                    #info={'pwd':newpasswd1,'email':email,'lock':'no','money':''}
                    account_info[username]=info
                    if self.dbop.db_is_file('init_account.txt','w',account_info):
                        print("\n\t\033[32mCongratulation , Register Sucessfull!!\033[0m")
                    return True


    def admin_manger(self,username,opration):
        """
        给管理用户解锁或者锁定，删除普通用户的功能
        :param username: 普通用户名字
        :param opration: 管理员要操作的动作，解锁或者锁定，删除普通用户
        :return:
        """
        if opration=="lock":
            self.account_info[username]['lock'] = 'yes'
            print( 'the %s had lock!!' % username )
        elif opration=='unlock':
            self.account_info[username]['lock'] = 'no'
            print( "the %s had unlock!!" % username )
        elif opration=='del':
            self.account_info.pop(username)
            print("Delete the account %s"%username)
        return self.dbop.db_is_file( 'init_account.txt', 'w', self.account_info )


'''
ac = login_check( )
ac.check_account_exist( 'ljf' )
ac.check_account_status( 'ljf' )
ac.lock_account( 'ljf', 'True' )
#xxxx = {'name': 'ljf', 'pwd': '1234', 'email': '198402913@qq.com',}
#print(xxxx)
#ac.register( name='ljdf',pwd='1234',email='19845402913@qq.com' )
ac.change_passwd('ljf')
'''