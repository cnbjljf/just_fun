#_*_coding:utf-8_*_
import pika
import time
import subprocess
import optparse

useage="""
    --exchange  指明exchange的名字
    --type      指明exchange的类型
    --host      指明要链接到host
"""

# 实例化optparse，用来捕获用户输入到参数
parser = optparse.OptionParser(useage)
help="you wanna connection rabbitmq server host"
parser.add_option("--host",help=help,default='localhost')

help=" declare exchange type  "
parser.add_option("--type",help=help,default='fanout')

help=" declare exchange's name  "
parser.add_option("--exchange",help=help,default='logs')

options,args= parser.parse_args()

# 把用户输入到参数提取出来
exchange_name=options.exchange
conn_host=options.host
exc_type=options.type

# 连接rabbitmq服务器
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=conn_host))
channel = connection.channel()
# 声明一个exchange
channel.exchange_declare(exchange=exchange_name,type=exc_type)
# 产生一个队列
quename=channel.queue_declare(exclusive=True)
quename=quename.method.queue
# 把exchange和队列绑定
channel.queue_bind(exchange=exchange_name,queue=quename)

def fib(n):
    """
    这个用来执行命令的方法
    :param n: need to execute command
    :return:
    """
    cmd=subprocess.Popen(n,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result=cmd.stdout.read()
    return  result


def on_request(ch, method, props, body):
    """
    如果我没有记错的话，这个用来是callback函数，用来把执行命令到结果返回给服务端。
    “”“
    :param ch: channel
    :param method:
    :param props: receive correlation_id from server
    :param body: message body
    :return:
    """
    n = str(body.decode())
    print(" [.] fib(%s)" % n)
    response = fib(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue=quename)
print(" [x] Awaiting RPC requests")
channel.start_consuming()