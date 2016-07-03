#!/usr/bin/env python
'''
这个select模型的客户端。
'''
__author__ = 'jieli'
import socket
import sys

# 定义一个消息列表
messages = [ 'This is the message. ',
             'It will be sent ',
             'in parts.',
             ]
server_address = ('localhost', 10000)

# Create a TCP/IP socket
# 创建一个socket实例的列表
socks = [ socket.socket(socket.AF_INET, socket.SOCK_STREAM),
          socket.socket(socket.AF_INET, socket.SOCK_STREAM),
          ]

# Connect the socket to the port where the server is listening

print('connecting to %s port %s' % server_address,file=sys.stderr)
# 遍历socks列表里的对象，然后去连接服务器
for s in socks:
    s.connect(server_address)

# 遍历消息列表，
for message in messages:

    # Send messages on both sockets
    # 遍历socks列表里面的值，在两个socket上面发生消息到服务器
    for s in socks:
        #print >>sys.stderr, '%s: sending "%s"' % (s.getsockname(), message)
        print('%s: sending "%s"' % (s.getsockname(), message),file=sys.stderr)
        s.send(bytes(message,'utf8'))

    # Read responses on both sockets
    # 遍历socks列表，开始接受新的数据，
    for s in socks:
        data = s.recv(1024)
        #print >>sys.stderr, '%s: received "%s"' % (s.getsockname(), data)
        print('%s: received "%s"' % (s.getsockname(), data),file=sys.stderr)
        if not data:
            #print >>sys.stderr, 'closing socket', s.getsockname()
            print('closing socket', s.getsockname(),file=sys.stderr)
            s.close()