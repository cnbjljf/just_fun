#
'''
from twisted.internet import reactor, protocol


class Echoclient(protocol.Protocol):
    """
    if Connected, send message to peer,and print the result
    """

    def connectionMade(self):
        self.transport.write("hellow")

    def dataReceived(self, data):
        """
        receive data from peer,
        :param data:
        :return:
        """
        print("Server said", data)
        self.transport.loseConnection()

    def connectionLost(self, reason):
        print('connection lost')


class EchoFactory(protocol.ClientFactory):
    protocal = Echoclient

    def clientconnectionFaild(self, connector, reason):
        print("connect Faild - goodbye")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("connection lost -- goodbye")
        reactor.stop()

def main():
    f = EchoFactory()
    reactor.connectTCP('127.0.0.1', 8000, f)
    reactor.run()
if __name__=="__main__":
    main()

'''
from twisted.internet import reactor, protocol


# a client protocol

# 定义一个类，里面包含来开启链接，处理链接，关闭链接到方法
class EchoClient(protocol.Protocol):
    """Once connected, send a message, then print the result."""

    # 这里相当是用来处理放送数据到方法，相当与socketserver里面到setup方法
    # connectionMade是在本机和服务器之间建立一条链接
    def connectionMade(self):
        print('--> send data to peer')
        # transport.write是以 非阻塞到方式按顺序依次把数据放给对端
        self.transport.write(bytes("hello alex!",'utf8'))
        print("==> already send")
        #self.transport.write("hello alex!")

    # 这个方法用来处理接受数据后到操作，相当于socketserver到handler方法
    def dataReceived(self, data):
        "As soon as any data is received, write it back."

        print("Server said:", str(data.decode()))
        # 这个方法用来把挂起到数据写入后关闭链接
        self.transport.loseConnection()

    # 写入数据后关闭链接
    def connectionLost(self, reason):
        print("connection lost")

# 这个方法用来处理如果链接异常断开后方法
class EchoFactory(protocol.ClientFactory):
    # 把EchoClient这个类赋值给protocol,相当与重构这个protocol方法，改成自定义到类EchoClient
    protocol = EchoClient
    # 这个方法用来处理链接错误
    def clientConnectionFailed(self, connector, reason):
        print("Connection failed - goodbye!")
        reactor.stop()
    # 这个方法在链接断开后后执行到动作
    def clientConnectionLost(self, connector, reason):
        print("Connection lost - goodbye!")
        reactor.stop()

# this connects the protocol to a server running on port 8000
def main():
    # 把类EchoFactory实例化，实例名称是f
    f = EchoFactory()
    # 绑定端口和ip，并且把实例f当参数传入进去。类似于socketserver绑定端口和IP一样
    reactor.connectTCP("localhost", 8000, f)
    # 等价与socketserver里面到serv_forever()方法一样，开始进入循环
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()