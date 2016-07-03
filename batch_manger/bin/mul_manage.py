#!/usr/bin/env python
'''
这个模块主要是用来是启动主程序的。
'''
import os
import sys
import getopt
from  multiprocessing import Pool
from  multiprocessing import TimeoutError

path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )
from modules import command,get,pkg,put
from conf import paramiko_conf
from core import load_client_host_info
from core import record_log
from core import main_run

if __name__ == "__main__":
    main_run.Run_main()


