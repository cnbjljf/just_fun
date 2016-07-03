#!/usr/bin/env python
import logging

def handler_log(username):
        #实例化模块,这个全局的日志级别是优先级最高的！！
        logger=logging.getLogger(username)
        logger.setLevel(logging.INFO)

        #create console handler and set level to debug
        ch=logging.StreamHandler()
        ch.setLevel(logging.ERROR)

        #create file handler and set level to debug
        fh=logging.FileHandler('access.log')
        fh.setLevel(logging.INFO)

        #set log format
        formatter=logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')

        #add formatter to ch and fh
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        #add ch and fh to logger
        logger.addHandler(ch)
        logger.addHandler(fh)

        return logger

'''
ret=handler_log('ljf')
ret.error('xxxxxxxxx')
'''