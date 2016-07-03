#!/usr/bin/env python
'''
这个用来初始化数据库和导入基本信息的
'''
import os
import sys

path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,Table,ForeignKey
from sqlalchemy import Column,Integer,String,func
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy import create_engine
import yaml
import hashlib


engine = create_engine("mysql+pymysql://root:123@192.168.141.137:3306/bastion")
Base = declarative_base()
Base.metadata.create_all(engine)

# 创建与数据库的会话session class,notice it return class
SessionCls=sessionmaker(bind=engine)
Session=SessionCls()

class UserInfo(Base):
    """
    存放用户信息的数据表结构
    """
    __tablename__ = 'userinfo'
    username=Column(String(128),primary_key=True)
    password=Column(String(128),nullable=False)
    #group_name=Column(String(128),nullable=False)


    def __repr__(self):
        return "user = %s , password = %s ,group_name = %s" %(self.username,self.password,self.group_name)

class Audit_log(Base):
    """
    存放用户执行命令后的结果的数据表结构
    """
    __tablename__ = 'AuditLog'
    id=Column(Integer,primary_key=True,autoincrement=True)
    timestamp=Column(String(128),nullable=False)
    username=Column(String(128),nullable=False)
    login_host=Column(String(128),nullable=False)
    host_group=Column(String(128),nullable=False)
    exec_cmd=Column(String(256),nullable=False)

    def __repr__(self):
        return "id=%s , timestamp=%s , username=%s , login_host=%s , host_group=%s , exec_cmd=%s" \
        %(self.id,self.timestamp,self.username,self.login_host,self.host_group,self.exec_cmd)


class HostInfo(Base):
    """
    定义存放主机信息的数据表结构
    """
    __tablename__ = 'hostinfo'
    hostname=Column(String(254),primary_key=True,nullable=False)
    host_ip=Column(String(254),primary_key=True,nullable=False)
    ssh_port=Column(Integer,default=22,nullable=False)
    host_group=Column(String(254),nullable=False,)


    def __repr__(self):
        return "hostname = %s , host_ip = %s , ssh_port = %s ,host_group = %s" %(self.hostname,self.host_ip,\
                                                                                 self.ssh_port,self.host_group)
# 创建用户和主机之间的关系表
class user2host(Base):
    __tablename__ = 'userbindhost'
    id = Column(Integer,primary_key=True,autoincrement=True)
    urname=Column(String(254),nullable=False)
    hgroup=Column(String(254),nullable=False)

# 创建表
Base.metadata.create_all(engine)

def write2userinfo(filename):
    '''
    这个用来把用户信息导入数据库里面的，同时写入用户信息表和用户主机组关系表
    :param filename:  存放用户信息的文件
    :return: True
    '''
    with open(filename,'r') as f:
        for i in f:
            uname=i.split(':')[0]
            pwd=i.split(":")[1]
            hgroup=i.split(":")[2]
            Session.add_all([
                UserInfo(username=uname,password=func.md5(pwd)),
                user2host(urname=uname,hgroup=hgroup)
            ])
    Session.commit()
    return True

def wrinte2hostinfo(filename):
    """
    这个把主机信息导入数据库里面
    :param filename:  存放主机信息的文件
    :return:
    """
    with open('machine_info.yaml','r') as f:
        mf=yaml.load(f)
        for hn,k in mf.items():
            ip_addr=k[0]
            port=k[1]
            if not isinstance(int,type(port)):
                group=k[2]
                port=22
            Session.add_all([
                    HostInfo(hostname=hn,host_ip=ip_addr,ssh_port=port,host_group=group)
                             ])
    Session.commit()

def CountHostNum_On_Group():
    """
    :param filename:
    :return:
    """
    #Session.query('bastion.hostinfo',func.count()).filter('')
    #web_server_num=Session.query('hostinfo'.func())
    pass

def select_judge_passwd(login_name,passwd):
    """
    根据用户名搜索密码，
    : login_name: 已经登陆的用户名，
    :return:
    """
    import hashlib
    m=hashlib.md5()
    m.update(passwd.encode())
    info=Session.query(UserInfo).filter(UserInfo.username==login_name).first()
    print(info.password,'||',m.hexdigest())
    if info.password == m.hexdigest():
        print("password is True")
        return True
    else:
        print("password is Error")
        return False

def select_user_group(username):
    """
    根据用户名来提取出能够登陆的主机组
    :param username: 已经等登陆的用户
    :return:
    """
    group_info=Session.query(user2host).filter(user2host.urname==username).first()
    if group_info:
        return group_info.hgroup
    else:
        return False

def select_group_host(xgroup):
    """
    这个方法用根据提供组名来获取所有属于改组的主机
    :param group: 要搜索的主机组名
    :return:
    """
    ghost_all=Session.query(HostInfo).filter(HostInfo.host_group==xgroup).all()
    if ghost_all:
        return ghost_all
    else:
        return False

#write2userinfo('user_info.yaml')
#wrinte2hostinfo('machine_info.yaml')
#select_judge_passwd('ljf','123')
#ret=select_user_group('ljf2')
#print(ret)
#ret=select_group_host('LVS_SERVER')
#for line in ret:
#    print(line)

