# -*- coding : utf-8 -*-
# @Auther    : Careslten
# @time      : 2021/4/12 16:55
# @File      : run.py
# @SoftWare  : dengta_api_test
import shutil

import pytest
import time
from random import randint
import os
import platform
import datetime
import socket
import requests
import json
import sys
from config import RunConfig


def get_port():
    '''
    暂时没用
    :return:
    '''
    port = str(randint(50000, 65532))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect(('127.0.0.1', int(port)))
            s.shutdown(2)
            get_port()
        except:
            return port

def dingding(config,count):
    '''
    发送钉钉hock
    :param config:
    :param count:
    :return:
    '''
    headers = {"Content-Type": "application/json"}
    path = '测试环境'
    reportConf = RunConfig.test_allure
    if config == 1 or config == '1':
        path = '测试环境'
        reportConf = RunConfig.test_allure
    elif config == 2 or config == '2':
        path = '预生产环境'
        reportConf = RunConfig.uat_allure
    url = "## 等他接口测试报告({0}){1} \n>".format(path,now_time) + count + "[点击查看测试报告详情]({})".format(reportConf)
    data = {
        'msgtype': 'markdown',
        'markdown': {
            'title': '{}测试报告'.format(now_time),
            'text': url
        },
        'at': {
            "atMobiles": ['15989510396', '13434435107'], 'isAtAll': True
        }
    }
    r = requests.post(
        'https://oapi.dingtalk.com/robot/send?access_token={}'.format(RunConfig.dingding_token),
        data=json.dumps(data), headers=headers)


def clean():
    '''删除历史'''
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'Logs')):  # 无目录则新建
        os.makedirs(os.path.join(os.path.dirname(__file__), 'Logs'))
    log_path = 'Logs/'
    log_new_time = temp_date.strftime("%Y%m%d%H%M")
    log_filelist = os.listdir(log_path)
    for f in log_filelist:
        str = f[:-4]
        old_time = time.mktime(time.strptime(log_new_time, '%Y%m%d%H%M'))
        file_time = time.mktime(time.strptime(str, '%Y%m%d%H%M'))
        if int(file_time) + 604800 < int(old_time):
            os.remove('Logs/' + f)


def report_count(path):
    '''统计执行结果'''
    summary_json = path + '/widgets/summary.json'
    with open(summary_json, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
        statistic = json_data['statistic']
        time = json_data['time']
        pass_total = (statistic['passed'] + statistic['skipped'])  / statistic['total'] * 100
        duration = time['stop'] - time['start']
        str_list = '通过率:{0}%  \n'.format(("%.2f" % pass_total)) +\
                   "共计:{0}条  \n".format(str(statistic['total']))+\
                   '通过:{0}条  \n'.format(str(statistic['passed']))+\
                   '失败:{0}条  \n'.format(str(statistic['failed']))+\
                   '故障:{0}条  \n'.format(str(statistic['broken']))+\
                   '跳过:{0}条  \n'.format(str(statistic['skipped']))+\
                   '用例执行时间:{0}s  \n'.format(str(duration / 1000))
        return str_list,statistic


if __name__ == '__main__':
    # 传入参数 1为test环境，2为uat环境，3为正式，默认报告路径'report/allure_reports'需与jenkins allure插件路径一致
    args = sys.argv
    RunConfig.number = 1
    if len(args) == 1:
        RunConfig.number = 1
        result_path = 'report/allure_reports'
    else:
        RunConfig.number = args[1]
        result_path = args[2]
    temp_date = datetime.datetime.now()
    now_time = temp_date.strftime("%Y-%m-%d_%H-%M")
    port = get_port()
    report_path = 'report/html/{}'.format(now_time)
    # clean()  # 清理日志
    setting = platform.system()  # 判断系统环境
    pytest.main(args=['--cache-clear', '-s', '-q',  '--alluredir', result_path, RunConfig.cases_path])
    if 'Linux' in setting:
        os.system('rm -rf ./report/html/*')
        os.system(f'/opt/allure/bin/allure generate --clean {result_path} -o {report_path}')
    else:
        allure_home = os.environ.get('ALLURE_HOME') + '\\bin\\allure'
        os.system(f'{allure_home} generate --clean {result_path} -o {report_path}')
    old_time = int(time.time())  # 300秒前的时间
    out_time = 300
    while True:
        time.sleep(3)
        if os.path.exists(report_path):
            break
        elif int(time.time()) - old_time >= out_time:
            print('生成报告超时,超时时间{0}秒'.format(out_time))
            break
    count = report_count(report_path) #统计
    if count[1]['failed'] !=0 or count[1]['broken'] !=0:
        dingding(RunConfig.number,count[0]) #发送钉钉消息
    os.system(f'allure serve {result_path} -p 9502')