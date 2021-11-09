# -*- coding : utf-8 -*-
# @Auther    : Careslten
# @time      : 2021/4/9 17:55
# @File      : ReadYaml.py
# @SoftWare  : dengta_api_test

import yaml
import os

YAML_PATH = 'D:\dengta_apitest\\TestData'


class HandleYaml:
    '''
    use:yaml = HandleYaml('video').read_allyaml()
    '''

    def __init__(self, filename):
        self.filename = filename
        with open(os.path.join(YAML_PATH, self.filename), 'r', encoding='utf8') as f:
            self.file_content = yaml.load(f, Loader=yaml.FullLoader)

    def read_allyaml(self):
        '''
        :param filename:
        :return: all yaml data
        '''
        return self.file_content

    def read_oneyaml(self, apiName):
        '''
        :param apiName:接口名称
        :return:该api接口内容
        '''
        for i in self.file_content:
            if i['apiName'] == apiName:
                return i


if __name__ == '__main__':
    yaml = HandleYaml('video').read_oneyaml('短视频分类')
    print(yaml)
