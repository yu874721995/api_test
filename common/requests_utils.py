#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: 
@file: requests_utils.py
@time: 2021/6/30 14:07
@desc: 
"""
import re

import requests
import os
from jsonpath import jsonpath
from common.check_utils import CheckUtils
from requests.exceptions import RequestException
from requests.exceptions import ProxyError
from requests.exceptions import ConnectionError
from common.logger import Logger
from common.common import method
from test_case import conftest as case_conf
from config import RunConfig


class RequesteUtils:
    def __init__(self):
        '''
        初始化
        '''
        self.hosts = RunConfig.url
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.session = requests.session()

    def __get(self, get_infos,request):
        '''
        get方法
        :param get_infos: 单条用例的所有数据
        :return:
        '''
        Logger.info( " 请求信息-GET " + get_infos['url']  + "POST" + str(get_infos["body"]))
        try:
            response = self.session.get(url=get_infos['url'],
                                        headers=get_infos['Header'],
                                        params=get_infos["body"]
                                        )
            response.encoding = response.apparent_encoding
            result = CheckUtils(response).run_check(request,get_infos['assert'])
        except ProxyError as e:
            result = {'code': 4, 'message': '代理错误异常'}
        except ConnectionError as e:
            result = {'code': 4, 'message': '连接超时异常'}
        except RequestException as e:
            result = {'code': 4, 'message': 'Request异常，原因：%s' % (e.__str__())}
        except Exception as e:
            result = {'code': 4, 'message': '请求异常，原因：%s' % (e.__str__())}
        return result

    def __post(self, post_infos,body_type,request):
        '''
        :param post_infos:单条用例的所有数据
        :return:
        '''
        Logger.info( " 请求信息-POST " + post_infos['url']  + str(post_infos["body"]))
        try:

            if body_type == 'data':
                response = self.session.post(url=post_infos['url'],
                                             headers=post_infos['Header'],
                                             data=aesEncrypt(post_infos["body"])
                                             )
            else:
                response = self.session.post(url=post_infos['url'],
                                             headers=post_infos['Header'],
                                             json=post_infos["body"]
                                             )
            response.encoding = response.apparent_encoding
            result = CheckUtils(response).run_check(request,post_infos['assert'])
        except ProxyError as e:
            result = {'code': 4,  'message': '代理错误异常,原因：%s' % (e.__str__())}
        except ConnectionError as e:
            result = {'code': 4,  'message': '连接超时异常,原因：%s' % (e.__str__())}
        except RequestException as e:
            result = {'code': 4, 'message': 'Request异常，原因：%s' % (e.__str__())}
        except Exception as e:
            result = {'code': 4, 'message': '请求异常，原因：%s' % (e.__str__())}
        return result



    def request(self,step_infos,request):
        '''

        :param step_infos: fixture参数化时传递的内容，单条用例的所有原始信息
        :param cache: 用例执行时传递的pytest cache对象
        :return:
        '''
        try:
            Logger.info('***************用例名称: {}***************'.format(step_infos['apiName']))
            step_infos['url'] = self.hosts + step_infos['apiPath']
            requests_method = step_infos["method"]
            body_type = step_infos['body_type']
            body = step_infos['body']
            header = step_infos['Header']

            # 存在parmes和func时进行替换
            if isinstance(body, dict):
                step_infos['body']['version'] = RunConfig.version
                for key in body.keys():
                    if 'parmes.' in str(body[key]):
                        body[key] = request.config.cache.get(body[key].split('.')[1], None)
                    if 'func.' in str(body[key]):
                        body[key] = method(body[key].split('.')[1],request)
            else:
                step_infos['body'] = {}
                step_infos['body']['version'] = RunConfig.version
            if isinstance(header, dict):
                for key in header.keys():
                    if 'parmes.' in str(header[key]):
                        header[key] = request.config.cache.get(header[key].split('.')[1], None)
                    if 'func.' in str(header[key]):
                        header[key] = method(header[key].split('.')[1],request)
            else:
                step_infos['Header'] = self.headers

            #判断是否跳过
            if step_infos.__contains__('expand'):
                if step_infos['expand'].__contains__('skip'):
                    if step_infos['expand']['skip'] == 0:
                        result = {'code': 5,
                                  'message': "跳过用例"}
                        result = dict(result, **step_infos)
                        return result
                if step_infos['expand'].__contains__('sleep'):
                    case_conf.sleep(request,step_infos['expand']['sleep'])
                if step_infos['expand'].__contains__('list'):
                    if step_infos['expand']['list'] == 0:
                        step_infos['body'] = [step_infos['body']]

            if requests_method == "GET":
                result = self.__get(step_infos,request)
            elif requests_method == "POST":
                result = self.__post(step_infos,body_type,request)
            else:
                result = {'code': 3, 'message': '请求方式不支持'}

            # 提取响应内容到缓存中，判断vistariced存在且不为空
            if step_infos.__contains__('vistariced') and result['code'] == 0 and step_infos['vistariced'] != None:
                if step_infos['vistariced'] is not None:
                        data = step_infos['vistariced']
                        for i in data.keys():
                            values = data.get(i, None)
                            response = result['response_body_json']
                            for s in values.split('.'):
                                if '[' in s and ']' in s:
                                    index = int(re.search(r"\d+", s).group())
                                    parme = re.search(r'.*(?=\[\d+\])', s).group()
                                    ex = response.get(parme, None)[index]
                                    response = ex
                                else:
                                    ex = response.get(s, None)
                                    response = ex
                            request.config.cache.set(i, str(response))
        except Exception as e:
            result = {'code': 4,
                      'message': '非请求异常，原因：%s' % (e.__str__())}
            result = dict(result, **step_infos)
            Logger.error('非请求异常，原因：%s' % (e.__str__()))
        else:
            if result['code'] == 0 or result['code'] == 2:
                result = dict( result, **step_infos )
                Logger.info('响应结果 ' + result['response_body'])
            else:
                result = dict( result, **step_infos )
                Logger.error(result)
        return result