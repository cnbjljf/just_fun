#!/usr/bin/env python


import time
import re
goods_list={'house':3000000,'car':150000,'lumia950xlL':4500,'sufface':9200,'shirt':180,'shoes':290}  #定义一个商品列表

mark='cut-off-line'
u_i={}                  #定义存放用户信息的字典
temp_list=[]            #定义一个临时列表，用来存储密码错误的用户
lock=0                  #定义一个变量，用来更改用户锁定状态的
user_info=open('login_user.txt','r+')   #打开用户信息文件
for line in user_info:      #遍历文件内容
    u_i[line.split()[0]]=[]                     #提取用户名
    for a in range(1,4):                #循环三次
        u_i[line.split()[0]].append(line.split()[a])            #将用户名，密码，用户锁定状态以及金额做成一个字典
#print(u_i)



def rebuild_info(user_info,name,u_i,lock):
     user_info.seek(0)                 #把文件内容指针重新定义到文件内容开头
     account_info=user_info.readlines()     #读取文件所有内容
     user_info.seek(0)                  #把文件内容指针重新定义到文件内容开头
     for i1 in user_info:               #遍历读取到login_user。txt
         if name in i1:                 #只针对当前用户修改数据
            account_info[account_info.index(i1)]='%s %s %s %s\n'%(name,u_i[name][0],lock,u_i[name][2])       #记录当前用户的数据,把用户的信息做成一个列表元素
     user_info.close()
     f=open('login_user.txt','w')      #打开文件，重新写入文件内容,这是用户状态码更新后的内容。
     for x in account_info:
         f.writelines(x)                #使用writelines，自动添加换行符
     f.close()


def check_account(u_i,user_info,lock):                #定义一个检查用户名密码信息的函数

    i=0
    print(u_i)
    while i< 3:  #判断错误计数器是否大于0
        name=input("input your name ==>").strip()
        passwd=input("input your password ==>").strip()
        if name in u_i.keys():                   #判断用户输入的用户名是否有效
            if str(0)==u_i[name][1]:          #判断用户状态是否锁定,0代表不锁定，1代表锁定
                if passwd==u_i[name][0]:      #校验密码是否正确
                     print("\n\twelcome to %s login the system\n"%name)
                     shop_function(u_i,name)            #调用购物这个函数
                     rebuild_info(user_info,name,u_i,lock)       #调用修改用户信息文件的函数

                     break

                else:
                    temp_list.append(name)      #把密码错误的用户名放入错误统计次数列表里面
                    times=3-temp_list.count(name)       #计算该用户名还剩多少次的输入机会
                    print("your password is wrong!please try again,and your chance leave over %s times\n"%times)
                    i=temp_list.count(name)     #把用户名输入错误次数赋值给i
            else:
                print("sorry , your account %s is lock!\n"%name)
                break
        else:
            print("sorry your account is not exits!! \t please check your account!\n")
            break
    else:                           #如果用户输入密码连续超过三次，那么执行下面的内容
         print("你的输入错误密码次数过多，已经锁定该用户")
         lock=1
         rebuild_info(user_info,name,u_i,lock)


def shop_function(u_i,name):
    car_list=[]                                 #定义购物车列表
    balance=int(u_i[name][2])                   #定义余额
    print("your balance : %s\n\n" %u_i[name][2])            #打印余额

    Flags=1                                 #设定标志位，用户跳出循环
    while Flags:
        print("你的余额是： %s"%balance)
        for k,v in goods_list.items():              #遍历商品信息
            print(k,v)
        good_name=input("请输入要选择商品名称")
        if good_name not in goods_list.keys():          #判断用户输入是否在商品列表里面
            print("我们没有此产品出售\n")
            continue
        else:
            print("the goods info is\n\tname: %s\n\tprice: %s "%(good_name,goods_list[good_name]))
            yn=re.match('^y|^Y',input('are you sure buy it ??(y/n)'))           #提示用户是否确定购买，不购买的话回到打印商品信息那页
            if yn:
                if balance > goods_list.get(good_name):                        #判断用户资金是否大于商品价钱，不够的话提示用户
                    balance=balance-goods_list.get(good_name)                   #用户资金减去商品价钱
                    car_list.append(good_name)                                  #购物车添加商品
                    print("your shop car already add goods %s ,and your shop car have goods:\n\t%s"%(good_name,car_list))
                    print(mark.center(100,'*'))


                else:
                    print("你的余额已经不经不够了\n")
            else:
                continue

            while Flags:
                option=input("balance == > %s\nDo you want to do? \n\tAny Button: continue buying\n\tN: do not continue buying\n\tS: show shop_car\n\tD: deltel shop car goods"%balance).lower()

                if option == "n":                                       #判断用户输入的选择，如果为n的话，退出当前循环
                    Flags=0
                elif option == "s":                                     #如果为s，展现购物车的内容
                    print('\n\n\t%s'%car_list)
                    any=input()

                elif option == "d":                                     #如果是d的话，删除商品，
                    for  x  in enumerate(car_list):
                        print(x)
                    del_gd=int(input('请输入要删除商品的序号 ==>>'))
                    car_list.remove(car_list[del_gd])                   #购物车移除该商品
                    balance=balance+goods_list.get(good_name)           #并且把钱退回到用户的账上

                else:
                    print(mark.center(100,'*'))                         #什么都没匹配，返回到商品信息那列
                    break
    u_i[name][2]=balance                                                #重新赋值该登陆用户的余额
    return u_i                                                          #返回用户信息


if __name__=="__main__":
    check_account(u_i,user_info,lock)
