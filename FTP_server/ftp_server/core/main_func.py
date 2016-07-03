#!/usr/bin/env python
"""
该模块的主要作用是把所有的功能糅合在一块
"""
import socket
import os
import subprocess
import sys

path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )

from conf import settings, templates
from db import db_opration
#from record_log import handler_log
from core import account_caozuo
from core import login_handler
from core import ftp_Server

def main_run():
    lhs=login_handler.login_handler_ser()
    if lhs.recv_userinfo( ):
        while 1:
            fs=ftp_Server.ftp_handler()
            fs.getinfo_from_socket()




'''
main_run()

'''
