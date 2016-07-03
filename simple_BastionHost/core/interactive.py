# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.


import socket
import os
import sys
import getpass
import pickle

path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )

from db.db_table_init import Audit_log
import os
import sys
import datetime
from paramiko.py3compat import u
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://root:123@192.168.141.137:3306/bastion", max_overflow=5)
Base = declarative_base()
sess = sessionmaker(bind=engine)
se = sess()

with open('info.tmp','r') as f:
    fa=f.read()
    hostname=fa.split(',')[3].split('=')[1].strip()
    host_group=fa.split(',')[5].split('=')[1].strip()
    username=fa.split(',')[0].split("'")[1]


# windows does not have termios...
try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan):
    if has_termios:
        posix_shell(chan)
    else:
        windows_shell(chan)


def posix_shell(chan):
    import select
    
    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)
        cmd =''
        tab_result=''
        whether_tab = False        
        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = u(chan.recv(1024))
                    if len(x) == 0:
                        sys.stdout.write('\r\n*** EOF\r\n')
                        break
                    if whether_tab:
                        cmd += x
                        whether_tab = False
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if x != '\r':
                   cmd += x.strip()
                else:
                   result=cmd.split(']#')[-1]
                   se.add_all([Audit_log(
                                         timestamp=datetime.datetime.today().now(),
                                         username=username,
                                         login_host=hostname,
                                         host_group=host_group,
                                         exec_cmd=result
                     )])        
                   result = cmd = ''
                if x == '\t':
                   whether_tab = True
                if len(x) == 0:
                    break
                chan.send(x)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
        se.commit()

    
# thanks to Mike Looijmans for this code
def windows_shell(chan):
    import threading

    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")
        
    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()
        
    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()
        
    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass
