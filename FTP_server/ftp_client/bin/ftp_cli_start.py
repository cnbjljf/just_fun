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
from core import main_run_cli

if __name__=='__main__':
    mainrun=main_run_cli()
    mainrun.run_main_cli()
