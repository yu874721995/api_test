#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: dxl
@file: test_public.py
@time: 2021/7/29 15:04
@desc: 
"""
import allure
import pytest

import os
from common.yaml_utils import YamlUtils
from common.requests_utils import RequesteUtils
from config import RunConfig
yaml_path = RunConfig.PRO_PATH + '/TestData/data_public.yaml'


runs = RequesteUtils()
yaml = YamlUtils(file_path=yaml_path)
# 用于报告展示数据
results = yaml.run_allyaml()
@allure.suite("公用") #标题
@pytest.mark.parametrize("data", results)
def test_user(data,request):
    result = runs.request(data,request)
    allure.dynamic.title(str(result['apiName']))
    allure.dynamic.description(f"{str(result['apiName'])} {str(result['url'])}")
    if result['expand']['skip'] == 0:
        pytest.skip("跳过用例")
    # 备注信息
    with allure.step(f"message:{str(result['message'])}"):
        pass
    # 请求类型
    with allure.step(f"method:{str(result['method'])}"):
        pass
    # 请求url
    with allure.step(f"url:{str(result['url'])}"):
        pass
    # 请求参数
    with allure.step(f"data:{str(result['body'])}"):
        pass
    # 期望结果
    with allure.step(f"expect_result:{str(result['assert'])}"):
        pass
    # 响应结果
    with allure.step(f"res:{str(result['response_body'])}"):
        pass
    assert result['check_result'] == True

