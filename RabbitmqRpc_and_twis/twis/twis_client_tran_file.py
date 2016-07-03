# This is the Twisted Get Poetry Now! client, version 3.0.

# NOTE: This should not be used as the basis for production code.

import optparse

from twisted.internet.protocol import Protocol, ClientFactory


def parse_args():
    usage = """usage: %prog [options] [hostname]:port ...

This is the Get Poetry Now! client, Twisted version 3.0
Run it like this:

  python get-poetry-1.py port1 port2 port3 ...
"""

    parser = optparse.OptionParser(usage)

    # _以下划线开头，那个下划线只是充当占位符到作用。
    _, addresses = parser.parse_args()

    # 如果没有输入地址，那么就提示信息并且推出
    if not addresses:
        print(parser.format_help())
        parser.exit()

    # 把ip地址做处理下，截取冒号前面到
    def parse_address(addr):
        if ':' not in addr:
            host = '127.0.0.1'
            port = addr
        else:
            host, port = addr.split(':', 1)

        if not port.isdigit():
            parser.error('Ports must be integers.')

        return host, int(port)

    # map到方法就是把address 这里面到东西交给parse_address去运算，运算完以后在重新赋值到address里面
    return map(parse_address, addresses)


class PoetryProtocol(Protocol):
    poem = ''

    # 定义接受数据到动作，把字符串重复添加
    def dataReceived(self, data):
        data = str(data.decode())
        self.poem += data

    # 定义链接关闭的动作，调用类self.factory.poem_finished 方法，而self.factory.poem_finished 又调用类callback，
    def connectionLost(self, reason):
        self.poemReceived(self.poem)

    # 用来处理文件接受结束到。
    def poemReceived(self, poem):
        self.factory.poem_finished(poem)


class PoetryClientFactory(ClientFactory):
    # 指明协议类型
    protocol = PoetryProtocol

    # 构造方法，把callback赋值给self.callback
    def __init__(self, callback):
        self.callback = callback

    # 文件接受结束到动作，调用callback方法
    def poem_finished(self, poem):
        self.callback(poem)


# 从所指定到主机中下载文件并且调用callback方法
def get_poetry(host, port, callback):
    """
    Download a poem from the given host and port and invoke

      callback(poem)

    when the poem is complete.
    """
    # 导入reactor
    from twisted.internet import reactor
    # 实例化PoetryClientFactory，
    factory = PoetryClientFactory(callback)
    # 连接远程主机
    reactor.connectTCP(host, port, factory)


def poetry_main():
    # 获取ip地址和端口号
    addresses = parse_args()

    # 统计addresses到长度
    count = 0
    for ad in addresses:
        print('address',ad)
        count += 1

    # 导入reactor
    from twisted.internet import reactor

    poems = []

    # 把
    def got_poem(poem):
        print('poems -->', poem)
        poems.append(poem)
        # 判断已经接受数据到长度是否大于ip地址到长度
        if len(poems) == count:
            reactor.stop()

    ## 获取ip地址和端口号
    addresses = parse_args()
    # 遍历addresses，把ip和端口号分别提取出来，然后把got_poem当作callback参数传入get_poetry里面
    for address in addresses:
        host, port = address
        # 调用下载poem到方法
        get_poetry(host, port, got_poem,)
    # 启动运行
    reactor.run()

    # 遍历poems，并且打印出来
    for poem in poems:
        print(poem)


if __name__ == '__main__':
    poetry_main()
