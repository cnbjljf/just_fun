#_*_coding:utf-8_*_
# This is the Twisted Fast Poetry Server, version 1.0

import optparse, os

from twisted.internet.protocol import ServerFactory, Protocol


# 定义一个用来处理参数的方法
def parse_args():
    usage = """usage: %prog [options] poetry-file

This is the Fast Poetry Server, Twisted edition.
Run it like this:

  python fastpoetry.py <path-to-poetry-file>

If you are in the base directory of the twisted-intro package,
you could run it like this:

  python twisted-server-1/fastpoetry.py poetry/ecstasy.txt

to serve up John Donne's Ecstasy, which I know you want to do.
"""
    # 实例化parse参数
    parser = optparse.OptionParser(usage)

    help = "The port to listen on. Default to a random available port."

    parser.add_option('--port', type='int', help=help)

    help = "The interface to listen on. Default is localhost."
    parser.add_option('--iface', help=help, default='localhost')

    options, args = parser.parse_args()
    print("--arg:",options,args)

    # 判断有没有输入文件名，
    if len(args) != 1:
        parser.error('Provide exactly one poetry file.')

    # 把要传到文件名赋值给poetry_file
    poetry_file = args[0]

    # 判断这个文件是否存在
    if not os.path.exists(args[0]):
        parser.error('No such file: %s' % poetry_file)

    return options, poetry_file


# 定义这个类，用来传送文件到
class PoetryProtocol(Protocol):

    # 定义这个方法， 在链接建立后调用
    def connectionMade(self):
        # 以非阻塞到方式按顺序依次将文件数据写道物理链接上
        print('self.factory.poem',self.factory.poem)
        self.transport.write(self.factory.poem)
        # 将所有到挂起到数据写入，然后关闭链接
        self.transport.loseConnection()


class PoetryFactory(ServerFactory):
    # 指明protocol到协议是什么类型到
    protocol = PoetryProtocol
    # 构造方法
    def __init__(self, poem):
        self.poem = poem


def main():
    # 把端口，ip参数赋值给options，把文件名赋值给poetry_file
    options, poetry_file = parse_args()
    # 读取文件
    poem = open(poetry_file,'rb').read()
    # 把PoetryProtocol实例化，实例名是factory
    factory = PoetryFactory(poem)
    print('factory--type',type(factory))
    # 从twisted里面导入reactor模块
    from twisted.internet import reactor
    # 开始绑定ip和端口号，并且开始监听，把factory作为参数传入进去，类似于socketserver一样。
    port = reactor.listenTCP(options.port or 9000, factory,
                             interface=options.iface)

    print('Serving %s on %s.' % (poetry_file, port.getHost()))
    # 循环运行
    reactor.run()


if __name__ == '__main__':
    main()