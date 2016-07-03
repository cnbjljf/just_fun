#!/usr/bin/env python
'''
这个模块把所有的功能糅合在一起。
'''
import os
import sys
import getopt
from  multiprocessing import Pool
from  multiprocessing import TimeoutError
from socket import timeout
import socket
import re
#import socket.timeout

path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(path)
import modules
from modules import command,get,pkg,put
from conf import paramiko_conf
from core import load_client_host_info
from core import record_log

pkey_file = paramiko_conf.Pkey_File
# 这个用来获取当前登录的用户，记录日志的时候可以调用这个username
username = os.popen('echo $USER').read()
username = username.split('\n')[0]
log_path = paramiko_conf.log_path
result_log = paramiko_conf.result_log_path




def file_exec(f_name):
    """
    这个函数把yaml格式的配置文件读取出来后，重构数据格式，变成这样的格式{module:[ connect_host, command]}
    :param f_name:  need read file name
    :return:  True
    """
    need_exec_info={}
    fname_path=paramiko_conf.static_conf_file
    f_name=os.path.join(fname_path,f_name)
    load_yaml=load_client_host_info.load_info()
    exec_file=load_yaml.code_yaml_file(f_name)
    #print('exec_file',exec_file)
    # here need to optimize
    for i in exec_file:
        for h in exec_file.get(i):
            host_group = paramiko_conf.connect_host[h]
            for cm in exec_file.get(i)[h]:
                need_exec_info[i]=[host_group,cm]
    return need_exec_info



def Run_main():
    # 获取输入的参数，-c 是命令，-m 下载还是上传模式，-g 指定主机组，-r 远端文件名（绝对路径） -l 本地文件名（相对绝对路径都可以）
    # 指定配置文件的话，使用file 参数 such as ---> file top.ljf
    lchi=load_client_host_info.load_info()
    alog=record_log.handler_log(username,log_path)
    all_opts=sys.argv[1:]
    if not all_opts:
    # 如果没有输入任何参数，那么就打印帮助信息，退出
        exit(
            "\033[35mUseag: %s [ -c command] -m put/down -g host_group  -l local_file_path -r remote_file_path\033[0m" %
            sys.argv[0])
    opts={}
    # 这是选项
    opt=all_opts[0::2]
    # 这事参数
    args=all_opts[1::2]
    # 原来使用的getopt这个方法不好使了，只能自己通过下面这一的for循环把参数和选项结合起来，方便调用
    for o in enumerate(opt):
        opts[o[-1]]=args[o[0]]
    print('opts',opts)
    cmd = opts.get('-c')
    pd = opts.get('-m')
    l_file = opts.get('-l')
    r_file = opts.get('-r')
    host_group = opts.get('-g')
    host_group = paramiko_conf.connect_host.get(host_group)
    if all_opts[0]=='file':
        file_exec(all_opts[1])
    # 如果没有输入主机组，那么就使用所有的主机
    if not host_group:
        host_group = paramiko_conf.connect_host['all_host']
    # 判断主机信息文件是否存在，不存在直接退出了
    if lchi.Read_from_file(host_group) is not False:
        client_host_info = lchi.Read_from_file(host_group)
    # 标记位：为1，那么就走-c -m这样的命令模式，如果为0，那只走配置文件
    Fa=1
    if sys.argv[1]=='file':
        exe_info=file_exec(sys.argv[2])
        print('exe_info',exe_info)
        for mod in exe_info:
            client_host_info=lchi.Read_from_file(exe_info.get(mod)[0])
            cmd=exe_info[mod][1]
            if cmd.split()[-1]=='require':
            cc=re.search('^/.*',cmd)
            if cc:
                l_file=cc.group().split()[0]
                r_file=cc.group().split()[1]
                cmd=None
            connect_exec(client_host_info,cmd,mod,l_file,r_file)
            alog.info(str(opts))
            Fa=0
            #print('l_file,r_file -->',l_file,r_file)
    if Fa:
        connect_exec(client_host_info,cmd,pd,l_file,r_file)
        alog.info(str(opts))
        return  True


def connect_exec(client_host_info,cmd=None,pd=None,l_file=None,r_file=None):
    p=Pool(paramiko_conf.Pprocess_Num)
    # 遍历主机列表
    for line in client_host_info.split('\n')[:-1]:
        try:
            host = str(line.split(',')[0])
            port = int(line.split(',')[1])
            user = line.split(',')[2]
            auth_method = line.split(',')[3]
            password = line.split(',')[4]
            #print(type(host),port,user,auth_method,password,cmd)
            # 如果有命令，那么就走下面的代码块
            if cmd:
                ret = p.apply_async(command.ssh_cmd, (host, port, user, auth_method, password, cmd,pkey_file))
                #ret.get(timeout=2)
            # 如果模式是上传模式，那么就走下面的代码块
            elif pd == 'put':
                if l_file and r_file:
                    ret = p.apply_async(put.sftp_put, (host, port, user, auth_method, l_file, r_file, password,pkey_file))
                else:
                    print("\033[36m  -l local_file_path -r remote_file_path\033[0m")
            elif pd == 'get':
                if l_file and r_file:
                    ret = p.apply_async(get.sftp_down, (host, port, user, auth_method, r_file, l_file, password , pkey_file))
                else:
                    print("\033[36m  -l local_file_path -r remote_file_path\033[0m")
            else:
                print(
                    "\033[36mUseag: %s [ -c command] -m put/down -g host_group  -l local_file_path -r remote_file_path\033[0m" %
                    sys.argv[0])
            ret.get(timeout=2)
        except (socket.timeout,TimeoutError) as e:
            print("\033[31m the host %s can't connect \033[0m" % host)
            continue
        '''
        except Exception as e:
            print("\033[31mError Info:%s:\033[0m" % host, e)
            continue
        '''
    p.close()
    p.join()

