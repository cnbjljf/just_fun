#!/usr/bin/env python

import collections
import re
import pickle
import sys
import os
path=os.path.dirname(os.path.dirname(__file__))
sys.path.append(path)
from login.account_caozuo import account_opration
ac=account_opration()

#定义一个商品列表
goods_list={'house':3000000,'car':150000,'lumia950xl':4500,'sufface':9200,'shirt':180,'shoes':290}

class shopping(object):
    def __init__(self):
        self.car_list=[]

    def chose_goods(self):
        for k,v in goods_list.items():
            print(k,v)
        chose=input('请输入你要购买的商品(注：如果输入多件，那么每个商品之间用空格相隔) ==>').strip()
        #分割用户输入的数据，使其能够遍历
        print(chose.split())
        for i in chose.split():
            if i not in goods_list.keys():
                print("Sorry , we not sell the %s"%(chose))
                return False
            else:
                #如果用户输入的商品在商品列表里面，那么就添加到购物车里面
                self.car_list.append(i)
                #print(self.car_list)
        print(self.car_list)
        return  self.car_list

    def del_goods_on_car(self,car_ret):
        #遍历购物车，打印出购物的所有商品！
        for i in self.car_list:
            print(i)
        del_goods=input("Input your want to delete goods on shop car(注：只能一个一个的删除商品) ==> ").strip()
        if del_goods not in car_ret.keys():
            print("Sorry , your input goods not in the goods_list!! please check again!")
        del_goods_num=int(input('Input your want to delete goods of number ==>'))
        #car_ret.get(del_goods)
        car_ret[del_goods]=int(car_ret.get(del_goods))-del_goods_num
        print(car_ret.get(del_goods))
        if  int(car_ret[del_goods]) <=0:
            car_ret.pop(del_goods)
            return car_ret
        return car_ret

    def payment(self,username):
        summ=0
        #根据用户名来提取余额
        with open('init_account.txt','rb') as f:
            acc_info=pickle.load(f)
            balance=acc_info[username][1]
        car_ret=collections.Counter(self.car_list)
        #print('car-ret',car_ret)
        print("商品名称  该商品数量")
        for k,v in car_ret.items():
            print("%s\t\t\t%s"%(k,v))
        yn=input("Are you Sure buy them?(y:Buy it | n:not buy Them | d:del one of them)")
        if re.match('[Yy]',yn):
            print("\tOK,Now you should pay for money ")
            for goods in self.car_list:
                summ=summ+int(car_ret.get(goods))*int(goods_list.get(goods))
            if int(balance) < summ:
                print("Sorry, Your Balance is to litter!!")
                return False

            else:
                balance=int(balance)-summ
                print("Now your balance is %d"%balance)
                self.car_list=[]
                ac.repayment(username,summ)
                return summ
        elif re.match('[dD]',yn):
            self.car_list=self.del_goods_on_car(car_ret)
            print(self.car_list)

        elif re.match('[Nn]',yn):
            self.car_list=[]


'''
sp=shopping()
#ret=ac.chose_goods()
#print(ret)
sp.chose_goods()
sp.payment('ljf')
'''