#!/usr/bin/env python

import  pickle
import hashlib
import os
import sys
import datetime
import time
import re
path=os.path.dirname(os.path.dirname(__file__))
sys.path.append(path)
print(sys.path)
from withdraw import withdraw_by_interest


class account_opration(object):
    def __init__(self):
        self.f=open('init_account.txt','rb')
        self.account_info=pickle.load(self.f)
        print(self.account_info)
        #return self.account_info
        print(type(self.account_info['ljf'][-1]))
        self.af=open("admin_account.txt",'rb')
        self.admin_info=pickle.load(self.af)
        self.wd=withdraw_by_interest.with_draw()

    #检查用户名是否存在
    def check_account_exist(self,username):
        #print(self.account_info)
        #print(type(account_info))
        #print(self.account_info.keys())
        if username in self.account_info.keys():
            print( "\n\t\tThe Account Is Exist,But ....\n")
            return True
        else:
            print('\033[31mcheck_account_exis is False!!\033[0m')
            return False

    #判断用户密码是否正确
    def judge_password(self,username,passwd):
        #print(self.account_info[username][0])
        if passwd==self.account_info[username][0]:
            return True
        else:
            return False
    #判断用户是否锁定
    def judge_lock_status(self,username):
        if self.account_info[username][2]==1:
            print("\033[31m\tSorry,the Account is lock!!!\033[0m")
            return True
        else:
            return False

    #改密码
    def change_passwd(self,username):
        oldpasswd=str(input('input your old passwd ==>'))
        if oldpasswd==self.account_info[username][0]:
            newpasswd=str(input('Input Your New Passwd ==>'))
            new2passwd=str(input('Input Your New Passwd ==>'))
            if newpasswd==new2passwd:
                self.account_info[username][0]=newpasswd
                print('\n\tChange Password Sucessfully!')
                return self.finish(self.account_info)
            else:
                print("New Passwords Are not the Same!!")
                return False
        else:
            print("Your password is Error!!")
            return False
    #锁定账户
    def lock_account(self,username,f):
        #f是个标志位，如果f为真，那么就要锁定这个用户，如果为假那么就不锁定
        if f:
            self.account_info[username][2]=1
            self.finish(self.account_info)
            return True
        else:
            self.account_info[username][2]=0
            self.finish(self.account_info)
            return False
    #检查管理员账户密码是否正确
    def check_admin_user(self,adminname,adminpasswd):
        if adminname in self.admin_info.keys():
            if adminpasswd==self.admin_info[adminname]:
                print("\033[42mWelcome to admin login the system\033[0m")
                return True
            else:
                print("Sorry , your password is Error!!")
                return False
        else:
            print("sorry ,the account %s is not Exist!!"%adminname)
            return False
    #管理员操作的方法
    def admin_opration(self,opration,*args):
        #*args 传参的参数是用户，密码，余额，状态锁定信息，邮箱/电话，卡号，取现时间，出账后的金额，已经消费金额,是否已经出账,取现的现金,取现额度
        '''
        if add customer,please pass argument are 用户，密码，余额，状态锁定信息，邮箱/电话，卡号，取现时间，出账后的金额，已经消费金额,是否已经出账,取现的现金,取现额度
        '''

        #添加一个用户的功能
        if opration=="add":
            #print(args)1
            #print(type(args))
            print("输入格式为：用户，密码，余额，状态锁定信息，邮箱/电话，卡号，取现时间，出账后的金额，已经消费金额,是否已经出账,取现的现金,取现额度")
            self.account_info[args[0][0]]=[args[0][1],args[0][2],args[0][3],args[0][4],args[0][5],args[0][6],args[0][7],args[0][8],args[0][9],args[0][10]]
            return self.finish(self.account_info)

        #删除一个用户的功能
        elif opration=="del":
            try:
                self.account_info.pop(args[0])
                return self.finish(self.account_info)
            except KeyError:
                print("\033[31m\t\tThe Account %s is not Exist\033[0m"%args[0][0])

        #锁定一个用户的功能
        elif opration=="lock":
            self.account_info[args[0]][2]=1
            print('Lock The Account!!')
            return self.finish(self.account_info)
        #解锁一个用户的功能
        elif opration=="unlock":
            self.account_info[args[0]][2]=0
            print('Unlock The Account!!')
            return self.finish(self.account_info)
        #查看一个用户的信息
        elif opration=='look':
            msg='''
                Name => %s
                Password => %s
                Balance => %s
                Status => %s
                Email => %s
                Card_num => %s
                WithDraw_time => %s
                还款时间 => %s
                WithDraw_money => %s
                '''
            print(msg%(args[0],self.account_info[args[0]][0],self.account_info[args[0]][1],self.account_info[args[0]][2],self.account_info[args[0]][3],self.account_info[args[0]][4],self.account_info[args[0]][5],self.account_info[args[0]][6],self.account_info[args[0]][7]))
            return True
    #找回密码
    def find_password(self,username,balance,email):
        if self.account_info[username][3]==email:
            if self.account_info[username][1]==balance:
                print("Your Password is %s"%(self.account_info[username][0]))
                return  True
            else:
                print("Sorry, Your Balance is not the same!!")
                return  False
        else:
            print("Sorry, Your Email Address is not the same!!")
            return  False

    #转账api
    def tracnsfer_money_by_card(self,login_username):
            #这里的tr_username是指对方的账户，login_username是指登陆的用户名
            #判断要转账的账户的状态是否正常，如不正常就不能够转账！
            card_number=input("Input peer card number ==>")
            tr_username=input("Input peer username ==>")
            #判断如果对方账户存在，且对方账户没有锁定，那么就往下走
            if self.check_account_exist(tr_username) and not self.judge_lock_status(tr_username):
            #if account_opration.check_account_exist(username) and not account_opration.judge_lock_status(username):
                if str(card_number) == self.account_info[tr_username][4]:
                    tr_m=input("Input your want to transfer Money ==>")
                    yn=input("Are you Sure ?? (y/n) ==>")
                    result=re.match('[Yy]',yn)
                    if result:
                        #print('transfer begin-->',self.account_info)
                        #判断自己的余额是否大于要转账的钱数
                        if  int(self.account_info[login_username][1]) >= int(tr_m) >0:
                            #金额的操作
                            self.account_info[tr_username][1]=int(self.account_info[tr_username][1])+int(tr_m)
                            self.account_info[login_username][1]=int(self.account_info[login_username][1])-int(tr_m)
                            print('你的余额是：%s'%self.account_info[login_username][1])
                            print('你转出的金额 %s'%tr_m)
                            #print('transfer end-->',self.account_info)
                            #调用finish方法来写入数据
                            self.finish(self.account_info)
                            #格式化该信息，用来给日志函数写入日志
                            msg='Transfer %s RMB to %s(%s)'%(tr_m,tr_username,card_number)
                            return msg
                        else:
                            print("你的余额不足，请检查后无误后重试一遍！")
                            return "Transfer was False,Because Balance is too litter!"
                    else:
                        print("你已经选择放弃转账！")
                        return 'give up Transfer money!!'

    #取现API
    def WithDraw(self,username,begin_time):
        #判断是否已经记录了当月第一次消费的情况
        if not self.account_info[username][5]:
            self.account_info[username][5]=begin_time
        money_num=int(input("Input your want to withdraw money ==> "))
        #判断该用户取现总金额是否打印取现额度
        if money_num+self.account_info[username][9] <= self.account_info[username][10] and money_num <= int(self.account_info[username][1]):
            self.account_info[username][1]=int(self.account_info[username][1])-money_num
            self.account_info[username][9]=int(self.account_info[username][9])+money_num+money_num*0.05
            self.finish(self.account_info)
            print(self.account_info[username])
            msg="WithDraw_Money: %s ; Interest: %s ; Rate: %s" %(money_num,money_num*0.05,0.05)
            return msg
        else:
            print("你已经没有足够的余额提现")
            return False



    #信用卡消费款API
    def repayment(self,username,total_money):

        #print('信用卡消费API-->',total_money)
        #把当月消费的钱累加起来
        self.account_info[username][7]=int(self.account_info[username][7])+int(total_money)
        #额度扣掉刚才消费的钱
        balance=self.account_info[username][1]
        balance=int(balance)-int(total_money)
        self.account_info[username][1]=balance
        #判断是否已经记录了当月第一次消费的情况
        if self.account_info[username][5] ==0:
            beg_time=datetime.date.today()
            self.account_info[username][5]=beg_time
        print("结账成功！！")
        return self.finish(self.account_info)


    #计算还款日以及账单日
    def HuanKuan_ZhangDan(self,username):
        today=datetime.date.today().day
        #cur_month=datetime.date.today().month
        #begin_time_month=self.account_info[username][5].month
        #19是账单日
        if today==19:
            with open('init_account.txt','rb') as f:
                self.account_info=pickle.load(f)
            #判断是否已经出账，第8为为1表示已经出账
            if self.account_info[username][8]==0:
                #把当月取现和消费的钱加起来汇总
                self.account_info[username][6]=self.account_info[username][7]+self.account_info[username][9]
                #把取现的钱和消费的钱置为0
                self.account_info[username][9]=self.account_info[username][7]=0
                self.finish(self.account_info)
                #表示已经出账
                self.account_info[username][8]=1
                print('还款日，账户信息第8位',self.account_info[username][8])
            print("\t\033[33m Today is Bill Day \033[0m\n")
            msg='''
            This is Your Bill of this month :
            consume:
                %s
            '''
            print(msg%(self.account_info[username][6]))
            print("\t\033[33mThis is your water_bill\033[0m\n")
            #调用流水账单的方法
            for i in self.show_water_bill(username):
                print(i)
            return  True
        #z7号是账单还款日
        elif today==7:
            print("\t\033[33m Today is Repayment Day!! \033[0m\n")
            print('\n\t You should Repayment %s'%(self.account_info[username][6]))
        #判断当天的日期是否大于7和是否已经还清款项，下面第一步是计算
        '''
        elif cur_month-begin_time_month => 1 or cur_month-begin_time_month ==-11:
            if today>7 and int(self.account_info[username][6]) >0:
                begin_time=self.account_info[username][5]
                today_time=datetime.date.today()
                ret=self.wd.shicha(begin_time,today_time,)
                lixi=self.wd.calc_interest(ret,self.account_info[username][6],rate=0.005)
                self.account_info[username][6]=int(self.account_info[username][6])+lixi
        '''

    #流水账单显示
    def show_water_bill(self,username):
        water_bill=[]
        cur_month=datetime.date.today().month
        last_month=datetime.date.today().month-1
        cur_year=datetime.date.today().year

        #如果这个月小于10月，那么就在格式化输出的时候月份前+0
        if cur_month <10:
            cur_ttstamp="%s-0%s"%(cur_year,cur_month)
        else:
            cur_ttstamp="%s-%s"%(cur_year,cur_month)
        #如果上个月小于10月，那么就在格式化输出的时候月份前+0
        if last_month <10:
            last_ttstamp="%s-0%s"%(cur_year,last_month)
        else:
            last_ttstamp="%s-%s"%(cur_year,last_month)

        print('cur_stamp',cur_ttstamp)
        print('last_stamp',last_ttstamp)
        with open('%s_ATM.log'%(username),'r') as xx:
            for line in xx:
                #如果改行不是空行
                if line:
                    #匹配日志开头的时间戳
                    if line.startswith(cur_ttstamp):
                        day=int(line.split()[0].split('-')[2])
                        #判断如果改行的日志是在当月19号以内的
                        if day <19:
                            #匹配到了下面这三个关键字的话，那就追加到流水账单列表里面
                            if re.search('shopping|Transfer|WithDraw',line):
                                water_bill.append(line)

                    elif line.startswith(last_ttstamp):
                        day=int(line.split()[0].split('-')[2])
                        if int(day) >=19:
                            if re.search('shopping|Transfer|WithDraw',line):
                                water_bill.append(line)

        return water_bill

    #还款API
    def HuanKuan_api(self,username):
        with open('init_account.txt','rb') as f:
            self.account_info=pickle.load(f)
        if int(self.account_info[username][6]) >0:
            today=datetime.date.today().day
            cur_month=datetime.date.today().month
            #判断这个月的第一次消费时间是否为空
            if  self.account_info[username][5]:
                begin_time_month=self.account_info[username][5].month
                #判断这个月是否和第一次消费的月份为邻月
                if cur_month-begin_time_month >= 1 or cur_month-begin_time_month ==-11:
                    #如果当天日期大于7号还款日，那么开始计算利息
                    if today>7 and int(self.account_info[username][6]) >0:
                        print('xc'*20)
                        begin_time=self.account_info[username][5]
                        today_time=datetime.date.today()
                        #调用其他模块的方法
                        ret=self.wd.shicha(begin_time,today_time,)
                        lixi=self.wd.calc_interest(ret,self.account_info[username][6],0.0005)
                        print("\033[35m Your Interest is %s\033[0m"%lixi)
                        self.account_info[username][6]=int(self.account_info[username][6])+lixi

                    print("\n\tYour debt is %s \n"%(self.account_info[username][6]))
                    yn=input("Do you repayment all ??(y:全部还款 | n:还一部分款 | 回车键: 返回主菜单)")
                    if re.match("[yY]",yn):
                        self.account_info[username][1]=int(self.account_info[username][6])+int(self.account_info[username][1])
                        self.account_info[username][8]=self.account_info[username][5]=self.account_info[username][6]=0
                        self.finish(self.account_info)
                        print("\n\t\033[32m Great Happy! You already repayment the bill!!\033[0m")
                        return True
                    elif re.match('[Nn]',yn):
                        money=input("input you want to repayment money ==>")
                        print(self.account_info[username])
                        self.account_info[username][6]=int(self.account_info[username][6])-int(money)
                        self.account_info[username][1]=int(self.account_info[username][1])+int(money)
                        if self.account_info[username][6]==0:
                            self.account_info[username][5]=0
                        print("\n\t\033[31mYour debt is %s\033[0m"%self.account_info[username][6])
                        return self.finish(self.account_info)

                else:pass
            else:
                print("You are already repayment the bill!!")
        else:
            print("\n\tYou needn't repayment the debt!!")
            return True

    def finish(self,account_info):
        self.f.close()
        self.af.close()
        with open('init_account.txt','wb') as fi:
            pickle.dump(account_info,fi)
        with open('init_account.txt','rb') as fi:
            self.account_info=pickle.load(fi)
        print(self.account_info)
        print('信息写入成功')
        return self.account_info

'''
ac=account_opration()
#ac.admin_opration('admin','123','del',['ljf'])
ret=ac.admin_opration('admin','123','look',['lccjf','1cpe','1983033','0','12032yq@live.cn'])
#print(ret)
ab=open('init_account.txt','wb')
pickle.dump(ret,ab)
ab.close()
#ret=ac.admin_opration('admin','123','del',['ljf'])
#print(ret)

ac=account_opration()
ac.HuanKuan_ZhangDan('ljf')

'''