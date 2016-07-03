#!/usr/bin/env python
import socket
import hashlib
import os
import sys
path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )
from conf import settings, templates
from core import login_handler
from core import ftp_Client

def run_main_cli():
    lh=login_handler.login_handler_cli()
    tmp=[]
    if lh.send_user_info():
        ftpcli=ftp_Client.ftpClient()
        ftpcli.ftp_handler()

run_main_cli()
