#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: dxl
@file: Logger.py
@time: 2021/8/19 14:08
@desc:
"""
import logging
import os
from datetime import datetime

import colorlog
from config import RunConfig

log_colors_config = {
    'DEBUG': 'white',  # cyan white
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}


Logger = logging.getLogger('logger_name')

# 输出到控制台
console_handler = logging.StreamHandler()
# 输出到文件
log_time = datetime.now().strftime("%Y%m%d")
if not os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'Logs')):  # 无目录则新建
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'Logs'))
filename = RunConfig.PRO_PATH + '/logs/'
filename = filename + log_time +'.log'
file_handler = logging.FileHandler(filename=filename, mode='a', encoding='utf8')

# 日志级别，Logger 和 handler以最高级别为准，不同handler之间可以不一样，不相互影响
Logger.setLevel(logging.INFO)
console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)

# 日志输出格式
file_formatter = logging.Formatter(
    fmt='[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
    datefmt='%Y-%m-%d  %H:%M:%S'
)
console_formatter = colorlog.ColoredFormatter(
    fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
    datefmt='%Y-%m-%d  %H:%M:%S',
    log_colors=log_colors_config
)
console_handler.setFormatter(console_formatter)
file_handler.setFormatter(file_formatter)

# 重复日志问题：
# 1、防止多次addHandler；
# 2、loggername 保证每次添加的时候不一样；
# 3、显示完log之后调用removeHandler
if not Logger.handlers:
    Logger.addHandler(console_handler)
    Logger.addHandler(file_handler)

console_handler.close()
file_handler.close()


if __name__ == '__main__':
    Logger.debug('debug')
    Logger.info('info')
    Logger.warning('warning')
    Logger.error('error')
    Logger.critical('critical')


