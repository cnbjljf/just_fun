#!/usr/bin/env python
from twisted.internet import protocol
from twisted.internet import reactor

'''
class Echo(protocol.Protocol):
    def dataReceived(self,data):
        print('--> recive data from peer')
        self.transport.write(data)
'''
# 定义一个类，继承protocol.Protocol
class Echo(protocol.Protocol):
    # 定义一个方法，用来处理接受数据到
    def dataReceived(self, data):
        '''
        当有数据进来到时候，就会调用这个方法，然后我们再调用transport方法来把数据发送回去
        :param data:  接受到到数据
        :return:
        '''
        print('--> recive data from peer',self.transport.getPeer())
        self.transport.write(data)



def main():
    # 把protocol.ServerFactory 这个实例化，
    factory = protocol.ServerFactory()
    # 把运行到协议指明为echo
    factory.protocol = Echo

    # 开始绑定端口，ip，并把factory这个实例传入进去，类似于socketserver一样，下面也一样
    reactor.listenTCP(8000,factory)
    # 启动，进入循环，
    reactor.run()

if __name__=="__main__":
    main()