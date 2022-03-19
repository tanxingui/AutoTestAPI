import hashlib
import inspect
import traceback

import jsonpath
import requests
import re
from configs.config import HOST, NAME_PWD
from utils.decorator import show_time
from utils.log_util import log
from utils.yaml_util import read_yaml
from libs.Login import Login

token, sid = Login().login(NAME_PWD)


class BaseApi:
    def request_send(self, data, file=False):
        # 通过类名作为键去获取对应类的数据
        # ---获取继承 BaseAPI的子类的类名---  self.__class__.__name__
        self.record = read_yaml("../data/apiConfig.yaml")[self.__class__.__name__]
        # self.data = data
        # data = str(self.data)  # 把传入的data转换成字符串，然后进行拼接加密
        sign = hashlib.md5((token + data).encode("utf-8")).hexdigest()  # md5加密
        data = {'sid': sid, 'sign': sign, 'data': data}  # 拼接新的data
        try:
            funcName = inspect.stack()[1][3]  # 获取调用当前函数的那个函数名
            print('\n调用request_send:的函数名是>>> ', funcName)
            record = self.record[funcName]  # 获取apiConfig.yaml里面的函数级别键名
            if file:  # 是文件上传接口
                resp = requests.request(record['method'], url=f'{HOST}' + record['url'], files=data)  # 发送请求
            else:
                resp = requests.request(record['method'], url=f'{HOST}' + record['url'], data=data)  # 发送请求
            # 计算接口耗时单位是s
            # print(resp.elapsed.total_seconds())
            # 修改响应数据编码
            # resp.encoding='gbk'
            # print('响应数据的编码>>> ',resp.encoding)

            return resp.json()  # 返回响应数据
        except Exception as error:
            # 写日志！---调用日志的方法
            log.error(traceback.format_exc())
            raise error  # 抛出异常

    # 文件上传接口
    @show_time
    def file_upload(self, fileDir: ''):
        # 路径/图片名.类型-------  data/123.png
        fileName = fileDir.split('\\')[-1]  # 文件名
        fileType = fileName.split('.')[-1]  # 文件类型
        userFile = {'file': (fileName, open(fileDir, 'rb'), fileType)}  # 请求体
        print('文件路径>>>', fileDir)
        return self.request_send(userFile, file=True)

    # ----------------------正则的封装----------------------
    @classmethod
    def replace(cls, data, pattern='#(.*?)#'):
        for result in re.finditer(pattern, data):
            # 分段提取截取出来的字符串
            print(result.group())  # 匹配所有
            print(result.group(1))  # 匹配第一段
            #   需要替换的数据
            old_value = result.group()
            #   要替换的属性
            prop_name = result.group(1)
            new_value = str(getattr(cls, prop_name))
            data = data.replace(old_value, new_value)
        return data


# ----------------------断言类的封装----------------------
class BaseAssert:
    @classmethod  # 类方法
    def define_api_assert(cls, result, condition, exp_result):
        result = jsonpath.jsonpath(result, '$.errcode')
        exp_result = jsonpath.jsonpath(exp_result, '$.errcode')
        print('实际响应的结果>>', result)
        print('预期响应的结果>>', exp_result)
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
