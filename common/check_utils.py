#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: 
@file: check_utils.py
@time: 2021/6/30 14:07
@desc: 
"""
import re
from common.logger import Logger



class CheckUtils:
    def __init__(self, check_response=None):
        self.ck_response = check_response

    def no_check(self):
        return self.pass_result

    def check_key(self, check_data=None):
        check_data_list = check_data.split(',')
        res_list = []  # 存放每次比较的结果
        wrong_key = []  # 存放比较失败的key
        for check_data in check_data_list:
            if check_data in self.ck_response.json().keys():
                res_list.append(self.pass_result)
            else:
                res_list.append(self.fail_result)
                wrong_key.append(check_data)
        # print(res_list,wrong_key)
        if self.fail_result in res_list:
            return self.fail_result
        else:
            return self.pass_result

    def check_keyvalue(self, check_data=None):
        '''
        暂时没用
        :param check_data:
        :return:
        '''
        res_list = []  # 存放每次比较的结果
        wrong_key = []  # 存放比较失败的key
        for check_item in check_data.items():
            # if check_item in self.ck_response.json().items():
            if self.dist_assert(self.ck_response, check_data):
                res_list.append(self.pass_result)
            else:
                res_list.append(self.fail_result)
                wrong_key.append(check_item)
        print(res_list)
        if self.fail_result in res_list:
            return self.fail_result
        else:
            return self.pass_result

    def check_regexp(self, check_data=None):
        pattern = re.compile(check_data)
        if re.findall(pattern, self.ck_response.text):
            print(1)
            return self.pass_result
        else:
            print(2)
            return self.fail_result

    def run_check(self, check_data=None):
        '''
        入口函数
        :param check_data: 断言json
        :return:
        '''
        code = self.ck_response.status_code
        self.fail_result = {
            'code': 2,  # 请求是否成功标志
            'response_code': self.ck_response.status_code,
            'response_headers': self.ck_response.headers,
            'response_body': self.ck_response.text,
            'check_result': False,
            'message': 'json键值对不匹配'  # 扩展
        }
        try:
            self.pass_result = {
                'code': 0,  # 请求是否成功标志
                'response_code': self.ck_response.status_code,
                'response_headers': self.ck_response.headers,
                'response_body': self.ck_response.text,
                'response_body_json': self.ck_response.json(),
                'check_result': True,
                'message': '通过'  # 扩展
            }
        except:
            return self.fail_result
        if code == 200:
            result = self.dist_assert(self.ck_response, check_data)
            if result['code'] == 0:
                Logger.info('断言内容:{} , 断言结果：{}'.format(check_data, self.pass_result['message']))
            else:
                Logger.error('断言内容 {} , 断言结果 {}'.format(check_data, self.fail_result['message']))
            return result
        else:
            self.fail_result['message'] = "请求的响应状态码%s" % str(code)
            Logger.error('断言内容 {} , 断言结果 {}'.format(check_data, self.fail_result['message']))
            return self.fail_result

    def dist_assert(self, response, assertData):
        '''
        断言匹配
        :param response: 接口原始返回对象
        :param assertData: 断言json
        :return:
        '''
        try:
            response = response.json()
            for i in assertData.keys():
                lets = i.split('.')
                if len(lets) == 1:
                    if response[i] != assertData[i]:
                        return self.fail_result
                else:
                    response_data = ''
                    for let in range(len(lets)):
                        # 正则匹配规则
                        if '[' in lets[let] and ']' in lets[let]:
                            index = int(re.search(r"\d+", lets[let]).group())
                            parme = re.search(r'.*(?=\[\d+\])', lets[let]).group()
                            response_data = response.get(parme)[index]
                            response = response_data
                        else:
                            response_data = response.get(lets[let])
                            response = response_data
                    if response_data != assertData[i]:
                        return self.fail_result
            return self.pass_result
        except Exception as e:
            return self.fail_result