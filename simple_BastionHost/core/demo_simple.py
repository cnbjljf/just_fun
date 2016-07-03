#!/usr/bin/env python

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


import base64
import getpass
import os
import socket
import sys
import traceback
from paramiko.py3compat import input
#from main_run import info_dit
import pickle
import paramiko
try:
    import interactive
except ImportError:
    from . import interactive


# setup logging
paramiko.util.log_to_file('demo_simple.log')
# Paramiko client configuration
UseGSSAPI = True             # enable GSS-API / SSPI authentication
DoGSSAPIKeyExchange = True
with open('info.tmp','r') as f:
    fa=f.read()
    hostname=fa.split(',')[3].split('=')[1].strip()
    port=int(fa.split(',')[4].split('=')[1].strip())
    username=fa.split(',')[0].split("'")[1]
    password = fa.split(',')[1].split("'")[1]

print(hostname,port,username,password)


# get hostname


# now, connect and use paramiko Client to negotiate SSH2 across the connection
try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    print('*** Connecting...')
    client.connect(hostname, port, username, password)

    chan = client.invoke_shell()
    print(repr(client.get_transport()))
    print('*** Here we go!\n')
    interactive.interactive_shell(chan)
    chan.close()
    client.close()

except Exception as e:
    print('*** Caught exception: %s: %s' % (e.__class__, e))
    traceback.print_exc()
    try:
        client.close()
    except:
        pass
    sys.exit(1)
