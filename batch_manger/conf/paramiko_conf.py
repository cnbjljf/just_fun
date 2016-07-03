#!/usr/bin/env python
'''

'''
Pkey_File='/root/.ssh/id_rsa'
connect_host={
    'all_host':'ssh_login.txt',
    'web_host':'ssh_login_web.txt',
    'db_host':'ssh_login_db.txt',
}
log_path="/home/ljf/pycharm_project/batch_manger/log/access.log"
result_log_path="/home/ljf/pycharm_project/batch_manger/log/exec_result.log"
Pprocess_Num=4
static_conf_file='/home/ljf/pycharm_project/batch_manger_v1.5.6/batch_manger/conf/pm'