import pytest

# 钩子函数，解决中文用例名称显示乱码
def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        print(item.name)
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        print(item.nodeid)
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")


@pytest.fixture(scope='session', autouse=True)
def start_runing():
    print('开始接口自动化-------读取Excel')
    yield
    print('自动化测试结束-------清除数据')
