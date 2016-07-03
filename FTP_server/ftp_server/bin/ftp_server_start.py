#!/usr/bin/env python
"""
这个是ftpserver启动的脚本
"""
import socket
import os
import subprocess
import sys

path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )

from conf import settings, templates
from db import db_opration
from core import record_log
from core import account_caozuo
from core import login_handler
from core import ftp_Server
from core import main_func

if __name__=="__main__":
    mainrun=main_func.main_run()
    #mainrun.main_run()