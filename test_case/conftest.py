# -*- coding : utf-8 -*-
# @Auther    : Careslten
# @time      : 2021/4/12 16:45
# @File      : conftest.py
# @SoftWare  : dengta_api_test
import re
import json
import requests
import pytest
import time
import os
import random
from config import RunConfig


path = RunConfig.PRO_PATH + '/image/{}.png'.format(random.randint(1,5))
phone_end = 17999999999

def user_phone(request):
    user_phone = random.randint(17000000000, phone_end)
    request.config.cache.set('user_phone', user_phone)
    return user_phone

def user_phone2(request):
    user_phone2 = random.randint(17000000000, phone_end)
    request.config.cache.set('user_phone2', user_phone2)
    return user_phone2

def moving_phone(request):
    moving_phone = random.randint(17000000000, phone_end)
    request.config.cache.set('moving_phone', moving_phone)
    return moving_phone

def moving_phone2(request):
    moving_phone2 = random.randint(17000000000, phone_end)
    request.config.cache.set('moving_phone2', moving_phone2)
    return moving_phone2

def phone(request):
    phones = random.randint(17000000000, 17999999999)
    return phones

def name(request):
    '''随机name'''
    ming = '三江而带五湖赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜'
    M = "".join(random.choice(ming) for i in range(3))
    request.config.cache.set('name', '接口' + M)
    return M

def sign(request):
    sign = 'ASDFGHJKL'
    request.config.cache.set('sign', sign)
    return sign

def image_url(request):
    try:
        files = {'file': open(path, 'rb')}
        r = requests.post('https://dev-api.51dengta.net/common/oss/upload', files=files)
        url = r.json()
        image_url = url['info']['url']
        request.config.cache.set('image_url', image_url)
        return image_url
    except Exception as e:
        raise Exception('上传文件失败',e)

def sleep(request,time1 = 1):
    time.sleep(time1)

def share_url(request):
    share_sign = request.config.cache.get('share_url', None)
    share_sign = re.findall(r"share_sign=(.+?)&a=1", share_sign)
    return share_sign[0]

def spread_link(request):
    Key = request.config.cache.get('spread_link', None)
    Key = re.findall(r"slink=(.+?)&a=1", Key)
    return Key[0]

def version(request):
    version = RunConfig.version
    return version

def nextop_openapi_header_true(request):
    token = request.config.cache.get('token', None)
    return 'Bearer '+token

def nextop_openapi_header_false(request):
    token = request.config.cache.get('token', None)
    return 'Bearer '+ token + '123456----------------------'

def assert_page(request):
    body = request.keywords.node.funcargs['data']['body']
    header = request.keywords.node.funcargs['data']['Header']
    if header and isinstance(header, dict):
        if header['Authorization'] != 'Bearer ' + request.config.cache.get('token',None):
            return 2000
    if body and isinstance(body, dict):
        if body['limit'] == '好' or body['page'] == '好':
            return 4000
        return 0
    raise ValueError('body报错了')

def return_token(request):
    return 'Bearer ' + request.config.cache.get('token', None)

def get_session(request):
    header = request.keywords.node.funcargs['data']['Header']
    return header['cookie']

def return_reqid(request):
    times = str(int(time.time() * 1000)) + '.0125'
    return times
def return_reqtime(reqeust):
    times = str(int(time.time() * 1000))
    return times

