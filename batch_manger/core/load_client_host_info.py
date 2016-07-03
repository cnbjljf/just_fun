#!/usr/bin/env python
'''
这个模块主要用来读取要连接的客户端信息
'''

import os
import sys
import yaml
path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )
from conf import paramiko_conf
import collections

class load_info(object):
    def __init__(self):
        pass

    def Read_from_file(self,file_name):
        """
        这个模块主要用来读取要连接的主机信息
        :param file_name:
        :return:
        """
        if  not os.path.exists(file_name):
            exit("\033[31m The file %s is not exists!!\033[0m"%file_name)

        with open(file_name,'r') as f:
            info=f.read()
        return info

    def code_yaml_file(self,filename):
        """
        the function was use decode yaml format of file
        :param filename:  need decode file name
        :return: file content
        """

        with open(filename,'r') as f:
            info=yaml.load(f)
        return info



'''
a=load_info()
c=a.Read_from_file('ssh_login.txt')
for i in c.split('\n'):
    print(i)
'''
