#!/usr/bin/env python
import sys
import os
import time,datetime
import pickle
import re
path=os.path.dirname(os.path.dirname(__file__))
print('xxxxxxxxxxxxxx')
#print(sys.path)
#sys.path.append(path)
#from login.account_caozuo import account_opration
#print(dir(account_opration))
#from login import account_caozuo

class with_draw(object):
    def __init__(self):
        self.f=open('init_account.txt','rb')
        self.account_info=pickle.load(self.f)
        #self.ao=account_opration()

    def begin_time(self):
        begin_time=datetime.date.today()
        return begin_time

    def end_time(self):
        end_time=datetime.date.today()
        return end_time

    def shicha(self,begin_time,end_time):
        diff_time=(end_time-begin_time).days
        print('Diff_time:',diff_time)
        return diff_time

    def calc_interest(self,shicha,consume_money,rate):
        interest=int(consume_money)*int(shicha)*rate
        return interest
    '''
    def with_draw(self,username,begin_time):
        if not self.account_info[username][5]:
            self.account_info[username][5]=begin_time
        money_num=int(input("Input your want to withdraw money ==> "))
        if money_num+self.account_info[username][9] <= self.account_info[username][10] and money_num <= int(self.account_info[username][1]):
            self.account_info[username][1]=int(self.account_info[username][1])-money_num
            self.account_info[username][9]=int(self.account_info[username][9])+money_num+money_num*0.05
            with open('init_account.txt','wb') as fi:
                pickle.dump(self.account_info,fi)
            print(self.account_info[username])
            return True
        else:
            print("你已经没有足够的余额提现")
            return False
    '''
'''
wd=with_draw()
ret=wd.with_draw('ljf',wd.begin_time(),wd.end_time())
print(ret)
'''