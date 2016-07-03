#!/usr/bin/env python
import sys
import os
import pickle
import re
path=os.path.dirname(os.path.dirname(__file__))
sys.path.append(path)
from login import account_caozuo


class TR_money(object):
    def __init__(self):
        self.f=open('init_account.txt','rb')
        self.account_info=pickle.load(self.f)
        self.ao=account_caozuo.account_opration()
        print(self.ao.__init__())

def tracnsfer_money_by_card(self,login_username):
            #这里的tr_username是指对方的账户，login_username是指登陆的用户名
            #判断要转账的账户的状态是否正常，如不正常就不能够转账！
            card_number=input("Input peer card number ==>")
            tr_username=input("Input peer username ==>")
            if self.ao.check_account_exist(tr_username) and not self.ao.judge_lock_status(tr_username):
            #if account_opration.check_account_exist(username) and not account_opration.judge_lock_status(username):
                if str(card_number) == self.account_info[tr_username][4]:
                    tr_m=input("Input your want to transfer Money ==>")
                    yn=input("Are you Sure ?? (y/n) ==>")
                    result=re.match('[Yy]',yn)
                    if result:
                        print('transfer begin-->',self.account_info)
                        if  int(self.account_info[login_username][1]) >= int(tr_m) >0:
                            self.account_info[tr_username][1]=int(self.account_info[tr_username][1])+int(tr_m)
                            self.account_info[login_username][1]=int(self.account_info[login_username][1])-int(tr_m)
                            print('你的余额是：%s'%self.account_info[login_username][1])
                            print('你转出的金额 %s'%tr_m)
                            print('transfer end-->',self.account_info)
                            self.ao.finish(self.account_info)
                            return  True
                        else:
                            print("你的余额不足，请检查后无误后重试一遍！")
                            return False
                    else:
                        print("你已经选择放弃转账！")
                        return 'giveup'
'''
ad=TR_money()
ret=ad.tracnsfer_money_by_card(6214840107731008,'ljf','yq')
print(ret)
'''