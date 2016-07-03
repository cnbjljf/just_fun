import pickle
import hashlib

hmd5=hashlib.md5()
hmd5.update(b'123')
# quota 的单位是兆
account_info= {
    'ljf':{'pwd': hmd5.hexdigest(),'email': '198402913@qq.com', 'home_dir': '/home/ljf','lock':'no','quota':30},
    'yq':{'pwd': hmd5.hexdigest(), 'email': '1984913@sina.cn', 'home_dir': '/home/yq','lock':'no','quota':30}
}
ab=open('init_account.txt','wb')
pickle.dump(account_info,ab)


account_inof={
    'admin':{'pwd':'123','email':'159780125@sina.cn',}
}
ab=open('admin_account.txt','wb')
pickle.dump(account_inof,ab)
ab.close()