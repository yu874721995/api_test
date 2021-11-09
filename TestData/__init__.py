# -*- coding : utf-8 -*-
# @Auther    : Careslten
# @time      : 2021/4/9 17:47
# @File      : __init__.py.py
# @SoftWare  : dengta_api_test

'''
测试数据存放目录
'''
import re

a = 'info[0].id'
s = a.split('.')
for i in s:
    if '[' in i and ']' in i:
        print(re.search(r"\[-\]", i))
        print(re.search(r"\d+", i).group())
        print(re.search(r'.*(?=\[\d+\])', i))
