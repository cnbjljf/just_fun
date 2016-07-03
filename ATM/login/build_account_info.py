#!/usr/bin/env python
#记录用户信息的格式如下：
#key,  0, 1      ,2         ,3     ,4       5   ,           6          7        ,8      ,9        ,10        11
#用户，密码，余额，状态锁定信息，邮箱/电话，卡号，当月第一次消费时间，出账后的金额，已经消费金额,是否已经出账,取现的现金,取现额度，账单日以后的第一次消费时间
import pickle
account_info={
    'ljf':['123','15000','0','1310035@qq.com','6214840107731008',0,0,0,0,0,7500,0],
    'yq':['1234','20000','0','11298ljf@sina.com','6317000993224155',0,0,0,0,0,10000,0]
}
ab=open('init_account.txt','wb')
pickle.dump(account_info,ab)

account_inof={
    'admin':'123'
}
ab=open('admin_account.txt','wb')
pickle.dump(account_inof,ab)
ab.close()