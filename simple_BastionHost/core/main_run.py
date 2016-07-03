#!/usr/bin/env python
'''

'''
import os
import sys
import getpass
import pickle

path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )

from db import db_table_init as dti
info_dit=[]

def get_username_passwd():
    """
    判断用户名密码的正确与否
    :return:
    """
    global username
    #username='ljf3'
    #passwd='qwe'
    username = input(" username ==> : ")
    #passwd= getpass.getpass("pwd==>")
    passwd = getpass.getpass('Password for %s ==> :' %username)
    info_dit.append(username)
    info_dit.append(passwd)
    return dti.select_judge_passwd(username,passwd)

def show_host_group():
    """
    这个方法用来提供用户选择哪个设备组
    :return:
    """
    ret=dti.select_user_group(username)
    if ret:
        for i,group in enumerate(ret.split(",")):
            print(i,group)
        chose_group=int(input("input group's serial number ==>"))
        if chose_group <= len(ret)-1:
            return ret.split(',')[chose_group]

def show_host():
    """
    显示主机组
    :return:
    """
    chose_group=show_host_group()
    chose_group=chose_group.split('\n')[0]
    ret=list(dti.select_group_host(chose_group))
    #print(ret)
    if ret:
        for host,i in enumerate(ret):
            i=str(i)
            print(host,"-->",i.split('ssh_port')[0])
        chose_host=int(input("input host's serial number ==>"))
        info_dit.append(ret[chose_host])
        return ret[chose_host]

while 1:
    if get_username_passwd():
        while True:
            show_host()
            with open('info.tmp','w') as f:
                f.write(str(info_dit))
            import demo_simple
    else:
        continue



