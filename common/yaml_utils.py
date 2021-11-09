#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: 
@file: yaml_utils.py
@time: 2021/6/30 14:07
@desc:
"""
import os
import yaml
from common.logger import Logger
from config import RunConfig
import numpy as np
yaml_path = RunConfig.PRO_PATH + '/TestData/demo.yaml'



class YamlUtils:

    def __init__(self, file_path):
        self.file_path = file_path

    def read_allyaml(self):
        try:
            with open(self.file_path, 'r', encoding='utf8') as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        except:
            Logger.error('yaml格式不正确或未找到yaml文件')

    def run_allyaml(self):
        '''
        读取所有用例，同时根据用例body参数化生成新用例
        '''
        results = self.read_allyaml()
        datas = []
        for result in results:
            number = 0
            if isinstance(result['body'],dict):
                array = []
                assert_dict = {}
                for value in result['body'].values():
                    if isinstance(value, list):
                        array.append(value)
                    else:
                        parmes = []
                        parmes.append(str(value))
                        array.append(parmes)
                querys = self.cartesian(array).tolist()
                for key, value in result['assert'].items():
                    assert_dict[key] = value
                for a in querys:
                    number += 1
                    resu = result.copy()
                    parmes = resu['body'].copy()
                    for key,num in zip(parmes.keys(),range(len(parmes.keys()))):
                        parmes[key] = a[num]
                    resu['body'] = parmes
                    resu['assert'] = {}
                    for key, value in assert_dict.items():
                        if isinstance(value, list):
                            try:
                                resu['assert'][key]= value[number-1]
                            except:
                                resu['assert'][key]= value[-1]
                        else:
                            resu['assert'][key]= value
                    resu['apiName'] = resu['apiName'] + str(number)
                    if number != 1: #相同用例只在首次需要提取
                        resu.pop('vistariced')
                    datas.append(resu)
        return datas

    def cartesian(self,arrays, out=None):
        '''
        根据多个数组穷举所有组合
        '''
        arrays = [np.asarray(x) for x in arrays]
        dtype = np.dtype((str, 1000))
        n = np.prod([x.size for x in arrays])
        if out is None:
            out = np.zeros([n, len(arrays)], dtype=dtype)
        m = n // arrays[0].size
        out[:,0] = np.repeat(arrays[0],m)
        if arrays[1:]:
            self.cartesian(arrays[1:], out=out[0:m,1:])
        for j in range(1, arrays[0].size):
            out[j * m:(j + 1) * m,1:] = out[0:m,1:]
        return out


if __name__ == '__main__':
    yaml = YamlUtils(file_path=yaml_path).run_allyaml()


