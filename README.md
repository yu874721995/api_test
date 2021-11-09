dengTa api接口测试

1、pip install -r recomon.txt
2、mkdir Logs report 
3、run.py

用例格式：
- method: POST   --请求方式 （必填）
  apiPath: /user/auth/smsLogin  --请求路径 （必填）
  apiName: 登录授权-短信注册/登陆  --接口名称 （必填）
  Header:   --请求Header （字段必填，参数不填默认application/x-www-form-urlencoded）
    Content-Type: application/x-www-form-urlencoded
    sign: func.sign 
  body:   --请求body （字段必填，参数可选）
    phone: func.phone --参数化关键字：func（随机数）、parmes（替换参数） 
    code: parmes.code
  assert:   --断言写法，支持多层断言 （字段必填，参数可选）
    result: true
    info.list[0].name： xxxxx
  vistariced:  --接口提取参数 （可选）
    token: info.access_token
    user_id: info.user_id
    is_band_wx: info.unique_id
  expand:  --扩展字段（必填）
    skip: 1 --是否跳过   1为不跳过 0为跳过

test