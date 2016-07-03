#!/usr/bin/env python
import sys
import pickle
import datetime




def record_user_log(username,content):
    with open('%s_ATM.log'%(username),'a') as f:
        log_content="%s | %s | %s \n"%(datetime.datetime.today(),username,content)
        f.write(log_content)
    return True



general_func_list=['Change_Password','Shop','Transfer_Money','WithDraw','Exit']
tmp=[]
from login import account_caozuo
from shop import shopping_cart
#from transfer_money import transfer
from withdraw import withdraw_by_interest

ac=account_caozuo.account_opration()
sc=shopping_cart.shopping()
#tm=transfer.TR_money()
wd=withdraw_by_interest.with_draw()

def login_check(func):
    def check_user_info(username):
            #检测用户名是否存在
            if ac.check_account_exist(username):
                #如果用户状态没有被锁定，那么就走下面的代码块
                if not ac.judge_lock_status(username):
                    Sflag=1
                    passwd=input("\nInput Your Password(forget Password please input 1)==>")
                    #如果用户忘记了自己的密码，这里提供找回密码的方法
                    if passwd !=str(1):
                        #判断用户输入的密码是否正确
                        if ac.judge_password(username,passwd):
                            print('login sucessfully!!')
                        else:
                            tmp.append(username)
                            print("\n\t\033[31mPassword is Error\033[0m")
                            if tmp.count(username) > 3:
                                if ac.lock_account(username,1):
                                    exit("Input error password to many times,the account is lock!")

                    else:
                        record_user_log(username,'find password when login')
                        #提供找回密码的方式
                        email=input('Please Input Your Email Address ==> ')
                        balance=input('Please Input Your Balance ==>')
                        if not ac.find_password(username,balance,email):
                            print("\033[31m\tSorry,You input info Eorror!!\033[0m\n")

            return func(username)
    return check_user_info
#print(dir(account_caozuo))

@login_check
def main(username):
        Flag=1
        xx="Bank System"
        print(xx.center(100,'*'))
    #try:

        while Flag:
            print('\n\n')
            ac.HuanKuan_ZhangDan(username)
            ac.HuanKuan_api(username)
            #遍历功能列表
            print("\n\n\033[32mFunction options\n\033[0m")
            for k,v in enumerate(general_func_list):
                print(k,'\t',v)
            chose=input("\n请输入功能的序号 ==>")
            if chose==str(0):
                ac.change_passwd(username)
                record_user_log(username,'change password')
            elif chose==str(1):
                sc.chose_goods()
                ret=sc.payment(username)
                record_user_log(username,'shopping,and Pay %s'%(ret))
            elif chose==str(2):
                #tm.tracnsfer_money_by_card(username)
                ret=ac.tracnsfer_money_by_card(username)
                record_user_log(username,ret)
            elif chose==str(3):
                ret=ac.WithDraw(username,datetime.date.today())
                record_user_log(username,ret)
            elif chose==str(4):
                record_user_log(username,'logout the system')
                exit("You logout the system Now!!")

        #print(ret)
        #ab=open('init_account.txt','wb')
        #pickle.dump(ret,ab)
    #except BaseException as e:
    #    print(e)
    #    print("\033[31m\t\tThe Account Is Not Exist!!\033[0m")

if __name__ == "__main__":
    #选择管理员登陆还是普通用户登陆！
    whether_admin=input("管理员请按1，普通用户请按2！==>")
    #whether_admin=str(2):
    if whether_admin==str(2):
        username=input("\nInput Your Name ==> ")
        record_user_log(username,'Try to login the system!')
        main(username)
    if whether_admin==str(1):
        adminname=input("Input adminstrator name ==>")
        adminpasswd=input("Input adminstrator Password ==>")
        if ac.check_admin_user(adminname,adminpasswd):

            while 1:
                opration=input("Do you want to do of the General account (add/del/LOOK/lock/unlock),Exit please input Q ==>")
                #如果输入的是Q/q，那么就退出系统
                if opration=='q' or opration == 'Q':
                    break
                #非添加用户的操作，那么就下面的代码
                if opration !='add':
                    option=input("input the account name ==>")
                    if ac.admin_opration(opration,option):
                        print("\t\t\n操作成功！！")
                #如果是添加用户，那么就走下的代码
                elif opration =='add':
                    option=input("please input account inof,例如：用户，密码，余额，状态锁定信息，邮箱/电话，卡号，当月第一次消费时间，出账后的金额，已经消费金额,是否已经出账,取现的现金,取现额度，账单日以后的第一次消费时间 ，以空格分割==>").strip().split()
                    #判断管理员输入的信息是否完整，等于9个表示信息是完整的！
                    if len(option)==11:
                        if ac.admin_opration(opration,option):
                            print("\n\tadd the account is Sucessfully!\n")
                    else:
                        print("输入的用户信息不全，请在尝试一次！")
                        continue