#!/usr/bin/env python
import logging


class Record(object):
    def __init__(self,username):
        #self.logf=open('%s_ATM.log'%username,'wb')
        logging.basicConfig(filename='%s_ATM.log'%username,format='%(asctime)s | %(message)s',datefmt='%Y/%m/%d %H:%M:%S')

    def warn_log(self,content):
        logging.basicConfig(level=logging.WARNING)
        logging.warn(content)

    def info_log(self,content):
        logging.basicConfig(level=logging.INFO)
        logging.info(content)

rd=Record('ljf')
rd.info_log('test messsage')