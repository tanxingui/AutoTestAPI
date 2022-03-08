import hashlib
import inspect
import traceback
import requests

from configs.config import HOST
from utils.log_util import log
from utils.yaml_util import read_yaml
from libs.Login import Login


class BaseApi(Login):  # 基类
    def __init__(self, data):
        self.data = data
        # 获取基础BaseApi的子类类名
        self.record = read_yaml("../data/apiConfig.yaml")[self.__class__.__name__]

    def get_md5(self):
        token, sid = self.login()
        data = str(self.data)  # 把传入的data转换成字符串，然后进行拼接加密
        sign = hashlib.md5((token + data).encode("utf-8")).hexdigest()  # md5加密后返回
        return sign, sid

    def get_data(self):
        sign, sid = self.get_md5()
        data = {'sid': sid, 'sign': sign, 'data': self.data}  # 拼接新的data
        return data

    def request_send(self, file=False):
        try:
            funcName = inspect.stack()[1][3]  # 获取调用你这个方法的方法名
            record = self.record[funcName]  # 获取yaml文件对应类方法里面的数据
            # 文件上传的接口
            if file:
                resp = requests.request(record['method'], url=f'{HOST}' + record['url'], files=self.get_data())
                # print('响应体的编码>>>',resp.encoding)
            # 普通参数进行传参
            else:
                resp = requests.request(record['method'], url=f'{HOST}' + record['url'], data=self.get_data())
            return resp.json()
        except:
            print('异常处理', traceback.format_exc())

# ----------------------断言类的封装----------------------
class BaseAssert:
    @classmethod  # 类方法
    def define_api_assert(cls, result, condition, exp_result):
        print(result)
        print(exp_result)
        try:
            if condition == '=':
                assert result == exp_result
            elif condition == 'in':
                assert exp_result in result
            else:
                print('条件不满足')
        except Exception as error:
            # 日志获取详细的异常信息,format_exc()返回字符串
            log.error(traceback.format_exc())
            raise error  # 抛出异常---不影响pytest 运行结果！
