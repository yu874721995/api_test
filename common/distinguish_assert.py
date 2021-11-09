# -*- coding : utf-8 -*-
# @Auther    : Careslten
# @time      : 2021/4/16 17:41
# @File      : distinguish_assert.py
# @SoftWare  : dengta_api_test

from common.logger import Logger
import re

AssertLog = Logger(logger='AssertLog').getlog()

#已移动到check_utils中
def distAssert(response, assertData):
    AssertLog.info('断言内容:{}'.format(assertData))
    for i in assertData.keys():
        assert response.status_code == 200, 'code不对'
        if not isinstance(response, dict):
            raise TypeError('json串格式不正确')
        lets = i.split('.')
        if len(lets) == 1:
            assert response[i] == assertData[i]
        else:
            response_data = ''
            for let in range(len(lets)):
                if '[' in lets[let] and ']' in lets[let]:
                    index = int(re.search(r"\d+", lets[let]).group())
                    parme = re.search(r'.*(?=\[\d+\])', lets[let]).group()
                    response_data = response.get(parme)[index]
                    response = response_data
                else:
                    response_data = response.get(lets[let])
                    response = response_data
            assert response_data == assertData[i]
            return True
