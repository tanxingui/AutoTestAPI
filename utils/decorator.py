import time


def show_time(fun):  # 外函数
    def innertime(*args, **kwargs):  # 内函数
        starttime = time.time()
        resp = fun(*args, **kwargs)
        endtime = time.time()
        print('接口请求耗时 >>> %.2fs' % (endtime - starttime))  # 保留2位小数
        return resp

    return innertime  # 返回函数对象


@show_time  # 等价于test = show_time(test)
def test(*args, **kwargs):  # 参数写入内函数里面去行参
    print('开始自动化测试', args, **kwargs)
    time.sleep(1)


if __name__ == '__main__':
    # test = show_time(test)   #闭包的缺点，都要加上这一行代码
    test((1, {8}, [9999]), {4444: 'pppp'})
