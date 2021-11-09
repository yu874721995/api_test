import os



class RunConfig:

    """
    运行测试配置
    """
    #项目根路径
    PRO_PATH = os.path.dirname(os.path.abspath(__file__))

    # 运行测试用例的目录或文件
    cases_path = "test_case/test_demo.py"

    #环境
    path_number = 1
    version = '2.0.1'
    if path_number == 2:
        url = 'https://uat-api.51dengta.net'
    elif path_number == 3:
        url = 'https://api.51dengta.net'
    else:
        url = 'https://test-api.51dengta.net'

    #jenkins
    test_allure = 'http://121.201.57.207:8080/job/python-api/allure/'
    uat_allure = 'http://121.201.57.207:8080/job/api-uat/allure/'

    #钉钉机器人token
    dingding_token = '061d9ed9fdc27eaff09b1436a8fac294b5d95d46d6783f1f3922fd8901966e61'

