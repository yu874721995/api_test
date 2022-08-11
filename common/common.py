from test_case import conftest as case_conf
import conftest as global_conf

def method(method_name, request):
    '''

    :param method_name: 方法名
    :param cache:
    :return:
    '''
    if hasattr(case_conf, method_name):
        data = getattr(case_conf, method_name)
        return data(request)
    else:
        if hasattr(global_conf, method_name):
            data = getattr(global_conf, method_name)
            return data(request)
        else:
            raise ModuleNotFoundError('没有注册该方法：' + method_name)