import pika
import uuid
import optparse
import record_log
import os

#获取当前登录用户，用来记录日志
username = os.popen('echo $USER').read()
username = username.split('\n')[0]
log_path='/home/ljf/pycharm_project/Day10/Day10_housework/rlogs/result.log'
rlog=record_log.handler_log(username,log_path)

useage="""
    --exchange  指明exchange到名字
    --type      指明exchange到类型
    --host      指明要链接到host
    --cmd       指明要执行到命令
"""
# 实例化optparse，用来捕获用户输入到参数
parser = optparse.OptionParser(useage)
help="you wanna connection rabbitmq server host"
parser.add_option("--host",help=help,default='localhost')

help="you wanna execute command on rpc mode  "
parser.add_option("--cmd",help=help,default='uptime')

help=" declare exchange type  "
parser.add_option("--type",help=help,default='fanout')

help=" declare exchange's name  "
parser.add_option("--exchange",help=help,default='logs')

options,args= parser.parse_args()

# 把用户输入到参数提取出来
exchange_name=options.exchange
conn_host=options.host
cmd=options.cmd
exc_type=options.type



connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=conn_host))

class FibonacciRpcClient(object):
    def __init__(self,connection):
        #self.connection = pika.BlockingConnection(pika.ConnectionParameters(
        #        host='localhost'))
        # 连接主机
        self.connection=connection
        self.channel = self.connection.channel()
        # 定义一个exchange
        self.channel.exchange_declare(exchange=exchange_name,type=exc_type)
        # 声明一个队列
        result = self.channel.queue_declare()
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    # 判断返回来到id是否和发送过去到一样，一样到化，把返回到信息赋值给self.respone
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='logs',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        # 判断response是否为空，为空就继续循环直到有数据
        while self.response is None:
            self.connection.process_data_events()
        return self.response


fibonacci_rpc = FibonacciRpcClient(connection)

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(cmd)
# 打印返回来的信息
rest=str(response.decode()).split('\\n')
rlog.info("%s %s"%(cmd,rest))
for i in rest:
    print(i)

connection.close()
