#/usr/bine/env python
"""
用户操作数据文件的
"""
import sys
import os
import pickle
path=os.path.dirname(os.path.dirname(__file__))
sys.path.append(path)



class oprateion_db(object):
    def __init__(self):
        pass

    def db_is_file(self,filename,action,info=None):
        """
        用来读取存储用户信息是文件类型
        :param filename: 要读取的文件
        :param action:  要执行的动作，是 r还是w
        :param info: 要写入文件的数据
        :return:
        """
        #print("---- Storage_engine is File ------")
        with open('%s'%filename,'%sb'%action) as f:
            if action == "r":
                self.account_info=pickle.load(f)
                return  self.account_info
            elif action=="w" or action=='a':
                self.account_info=pickle.dump(info,f)
                return True

        def db_is_mysql(self):
            """
            以后有需求再增加
            :param self:
            :return:
            """
            pass


