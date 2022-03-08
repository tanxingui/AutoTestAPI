import time
import logging
from utils.path_util import logs_path

def logger(fileLog=True,name=__name__):   #定义日志文输出控制台or文件
    #日志存放的路径:路径+当前的时间+后缀名
    nowtime = time.strftime('%Y%m%d %H-%M-%S')
    # print(nowtime)
    logDir = fr"{logs_path}\{nowtime}.log"
    # print(logDir)
    #创建日志对象
    logObject = logging.getLogger(name)
    #设置级别
    logObject.setLevel(logging.INFO)
    #设置日志的内容格式：打印时间-级别-当前执行程序名[当前行号]:日志报文
    fmt = '%(asctime)s - %(levelname)s - %(filename)s[%(lineno)d]:%(message)s'
    format = logging.Formatter(fmt)  #把日志格式设置进去

    #文件日志
    if fileLog:
        #设置日志渠道--文件方式
        handle = logging.FileHandler(logDir,encoding='utf-8')
        #2- 日志内容绑定渠道
        handle.setFormatter(format)
        #3- 日志对象跟渠道绑定
        logObject.addHandler(handle)

    else:   #控制输出
        #设置日志渠道--控制台方式
        handle2 = logging.StreamHandler()
        #2- 日志内容绑定渠道
        handle2.setFormatter(format)
        #3- 日志对象跟渠道绑定
        logObject.addHandler(handle2)

    return logObject

log = logger()

# if __name__ == '__main__':
#     print(time.strftime('%Y-%m-%d %H:%M:%S'))