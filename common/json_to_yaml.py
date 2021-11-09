# -*- coding : utf-8 -*-
# @Auther    : Careslten
# @time      : 2021/4/22 12:23
# @File      : json_to_yaml.py
# @SoftWare  : interface

'''doclever导出的json格式数据转为testdata中的yaml'''

import json, os

with open('huarenban.json', 'rb') as f:
    jsons = json.load(f)
    interface_data = jsons['data']
    print(interface_data)
datas = []
for moudles in interface_data:
    if moudles['name'] == '#回收站' \
            or moudles['name'] == 'web' \
            or moudles['name'] == '语音匹配（语聊）' \
            or moudles['name'] == '漂流瓶' \
            or moudles['name'] == '官网及公众号' \
            or moudles['name'] == '小程序':
        continue
    for moudle in moudles['data']:
        data = {}
        try:
            for i in moudle['data']:
                data['method'] = i['method']
                data['apiPath'] = i['url']
                data['apiName'] = i['name']
                data['Header'] = i['param'][0]['header']
                data['body'] = i['param'][0]['bodyParam']
        except Exception as e:
            try:
                data['method'] = moudle['method']
                data['apiPath'] = moudle['url']
                data['apiName'] = moudle['name']
                data['Header'] = moudle['param'][0]['header']
            except Exception as e:
                pass
            try:
                data['body'] = moudle['param'][0]['bodyParam']
            except:
                try:
                    data['body'] = moudle['param'][0]['queryParam']
                except:
                    data['body'] = None
        if data['body'] == '' or data['body'] == [] or data['body'] is None:
            pass
        else:
            parme = {}
            for i in data['body']:
                if i['name'] == 'page':
                    parme[i['name']] = 1
                elif i['name'] == 'limit':
                    parme[i['name']] = 10
                elif i['name'] == 'access_token':
                    parme[i['name']] = 'parmes.token'
                elif i['name'] == 'type':
                    parme[i['name']] = 1
                elif i['name'] == 'user_id':
                    parme[i['name']] = 'parmes.user_id'
                else:
                    parme[i['name']] = 1
            data['body'] = parme
        if data['Header'] == '' or data['Header'] == [] or data['Header'] is None:
            pass
        else:
            parme = {}
            for i in data['Header']:
                parme[i['name']] = i['value']
            data['Header'] = parme
        data['assert'] = {'status_code': 200, 'result': True}
        datas.append(data)
from ruamel import yaml
with open(os.path.dirname(os.path.abspath('.')) + '/TestData/data_chinese.yaml','w',encoding='utf-8') as f:
    yaml.dump(datas,f,Dumper=yaml.RoundTripDumper,allow_unicode=True)