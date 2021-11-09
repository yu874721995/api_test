# -*- coding : utf-8 -*-
# @Auther    : Careslten
# @time      : 2021/4/12 16:14
# @File      : api_request.py
# @SoftWare  : dengta_api_test

import requests


class request(object):

    def __init__(self, method):
        self.method = method

    def request(self, **kwargs):
        if self.method == 'POST':
            r = requests.post(**kwargs)
            return r
        elif self.method == 'GET':
            r = requests.get(**kwargs)
            return r
        else:
            raise AttributeError('method参数不正确')
