#!/usr/bin/env python
'''
借助select IO模型来实现单线程高并发的socket连接，这个服务端
'''
#_*_coding:utf-8_*_
__author__ = 'Alex Li'

import select
import socket
import sys
import queue

# Create a TCP/IP socket
# 下面这一步是创建socket对象(也就是常说的实例化成一个实例)，socket.AF_INET是表示IPV4地址簇，SOCK_STREAM表示是TCP数据流
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 下面这一步表示 把socket设置为不堵塞
server.setblocking(False)

# Bind the socket to the port
server_address = ('localhost', 10000)
# 打印客户端信息，通过错误输出来打印到屏幕上
#print(sys.stderr, 'starting up on %s port %s' % server_address)
server.bind(server_address)

# Listen for incoming connections
# 最大监听客户端连接数量，超过5个以后就不监听，上面设置为不阻塞后，那么表示连接一个处理一个。
server.listen(5)

# Sockets from which we expect to read
# 设置一个列表，用来读取的。
print('server',type(server))
inputs = [ server ]

# Sockets to which we expect to write
# 设置一个用来写的列表
outputs = [ ]

# 设置一个消息队列
message_queues = {}
# 如果inputs这不为空（也就是表示建立了连接），那么开始循环
while inputs:

    # Wait for at least one of the sockets to be ready for processing
    print( '\nwaiting for the next event')
    '''
    调用select模块里的select方法，这里面有3个参数，分别表示读，写，期待某个条件参数（可以看作错误输出。）
    这里的文件描述符可以使socket，也可以是文件对象等等之类的，第四个参数是超时时间，可以使浮点型，分数型，
    如果不存在,那么就不会超时
    返回的值是包含这三个参数的列表，每个子集的内容包含了相对应 已经准备好的文件描述符
    '''
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    # Handle inputs
    # 处理已经准备好的请求，开始遍历准备好的文件描述符
    #print('\033[31m readable\033[0m',readable)
    for s in readable:
        print('\033[31m readable\033[0m',readable)
        # 如果 s 是个 server（socket实例）
        print('-'*100+'begin for loop the readable')
        if s is server:
            # A "readable" server socket is ready to accept a connection
            # 把连接的实例赋值给connection，把连接地址给client_address
            connection, client_address = s.accept()
            #print('s type:',type(s))
            print('new connection from', client_address)
            # 设置当前处理的这个连接为不阻塞类型
            connection.setblocking(False)
            # 把当前这个连接添加到inputs列表里面
            inputs.append(connection)
            print('\033[36m inputs list \033[0m',inputs)

            # Give the connection a queue for data we want to send
            # 把需要发送的消息放入到队列里面
            message_queues[connection] = queue.Queue()
            #print('connectiono type',type(connection),'message_queues type',type(message_queues))
            #print('message_queue',message_queues)
        # 如果不是server（socket类型）
        else:
            # 接收数据
            print('------can recivce data---------')
            data = s.recv(1024)
            # 如果data是有值
            if data:
                # A readable client socket has data
                print('received "%s" from %s' % (data, s.getpeername()),file=sys.stderr )
                message_queues[s].put(data)
                # Add output channel for response
                # 如果s不在outputs里面，那么就把他添加进去,因为这个s此时已经接收到了数据，说明处于活跃状态的连接
                print('outputs',outputs)
                if s not in outputs:
                    outputs.append(s)
            else:
                # Interpret empty result as closed connection
                print('closing', client_address, 'after reading no data')
                # Stop listening for input on the connection
                if s in outputs:
                    outputs.remove(s)  #既然客户端都断开了，我就不用再给它返回数据了，所以这时候如果这个客户端的连接对象还在outputs列表中，就把它删掉
                inputs.remove(s)    #inputs中也删除掉
                print('8888888888888888888  close the connect 88888888888888888888')
                s.close()           #把这个连接关闭掉

                # Remove message queue
                del message_queues[s]
    # Handle outputs
    # 遍历所有可写(也可说是可发送消息)的文件描述符
    print('\033[37m writeable\033[0m', writable)
    for s in writable:
        print('-'*100+'begin for loop the writeable')
        try:
            # 获取消息队列的属于s的信息（get_nowait 表示不等待），并且赋值给next_msg，
            next_msg = message_queues[s].get_nowait()
            print('\033[33m next_msg\033[0m',next_msg)
        except queue.Empty:
            # No messages waiting so stop checking for writability.
            # 如果在队列里面捕获到消息是空的，那么消息发送完了，并且在output删除这个描述符
            print('output queue for', s.getpeername(), 'is empty')
            outputs.remove(s)
        else:
            # 如果获取的消息不是空的，那么就发送消息出去，
            print( 'sending "%s" to %s' % (next_msg, s.getpeername()))
            s.send(next_msg)
    # Handle "exceptional conditions"
    # 遍历有错误的文件描述符
    print("9999999999999999999--exceptional-9999999999999999999")
    for s in exceptional:
        print('-'*100+'begin for loop the exceptional')
        print('handling exceptional condition for', s.getpeername() )
        # Stop listening for input on the connection
        # 在已经就绪的input列表里面删除这个错误对象
        inputs.remove(s)
        # 判断这个错误对象是否在输出列表里面，如果在的话，那么在输出列表里面删除，
        if s in outputs:
            outputs.remove(s)
        # 关闭socket连接00
        s.close()

        # Remove message queue
        # 删除这个消息队列
        del message_queues[s]