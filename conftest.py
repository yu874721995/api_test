# -*- coding : utf-8 -*-
# @Auther    : Careslten
# @time      : 2021/4/12 16:45
# @File      : conftest.py
# @SoftWare  : dengta_api_test

import requests
import pytest
from datetime import datetime


# @pytest.fixture(autouse=True)#统计用例执行时间，暂时不用
# def ex_time(request,cache):
#     nodeid = request.node.nodeid.split(':')[-1]
#     cache_path = f'case_time/{nodeid}'
#     start_time = datetime.now()
#     yield
#     end_time = datetime.now()
#     total_time = (start_time-end_time).total_seconds()
#     cache.set(cache_path,total_time)
#     time = cache.get(cache_path,None)
