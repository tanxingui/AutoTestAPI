# mock、异步处理模块
import threading  # 子线程库
import requests, time


def test(indata):  # 测试mock；json文件、bat文件在D:\study路径下
    url = 'http://127.0.0.1:9899/car_source/list'
    payload = indata
    resp = requests.post(url, json=payload)
    return resp.text


def get_order_result(orderID, outtime=30):
    """
    :param orderID: id去查
    :param outtime: 延时30秒
    :return: 查询结果
    """
    url = 'http://127.0.0.1:9899/user_order/detail'  # B端订单详情接口
    payload = {'data': {"sid": "46690#660120904222809092", "sign": "fc793a818218c947198d2aa97fcc8fcb", "data": orderID}}
    # print(type(payload))
    # 1-获取开始查询的时间
    startTime = time.time()  # 单位是s
    # 2-结束时间=开始时间+超时时间
    endTime = startTime + outtime
    cnt = 0  # 查询的次数--初始值=0
    # 3- 判断查询是否超时：
    while time.time() < endTime:
        resp = requests.post(url, data=payload)  # http://ip:port/路径?a=1&b=2
        cnt += 1
        # 如果有响应数据：直接结束循环
        if resp.text:
            print(f'第{cnt}次查询，已有结果，退出查询>>> ', resp.text)
            break
        else:
            print(f'第{cnt}次查询，没有结果，请耐心等待！')
            time.sleep(3)  # 频率
    # 4-获取当前查询的时间,获取耗时endTime-starTime
    oneTime = time.time() - startTime
    print('该查询函数已经执行完毕耗时>>>', oneTime)


if __name__ == '__main__':
    data = {"page_id": 1, "page_size": 10, "querys": []}
    print(test(data))
    # print(type(test(data)))
    # res = get_order_result(data)

    # --------------创建子线程--------------------
    """
    threading.Thread(target,args)
    target:你需要把哪一个函数做为子线程执行的任务，就写函数名  get_order_result
    args:这个函数的需要传入的参数--以元组形式    
    """
    # 1- 计时开始时间
    startTime = time.time()  # 单位是s
    t1 = threading.Thread(target=get_order_result, args=(test(data),))
    # 主线程如果结束或者异常退出了，子线程就直接退出！
    t1.setDaemon(True)  # 守护线程，主线程结束子线程就结束
    t1.start()  # 开始执行子线程

    for one in range(3):
        time.sleep(1)  # 模拟其他接口执行的时间
        print(f'{one}---我正在执行其他接口自动化测试操作----')
    # ------------------------------------------------
    endTime = time.time()  # 执行完毕时间
    print('整个自动化执行耗时>>> ', endTime - startTime)
