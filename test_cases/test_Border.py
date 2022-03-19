import os
import jsonpath
import pytest
import allure
from commcon.baseApi import BaseAssert, BaseApi
from configs.config import excelDir, configData
from utils.excel_util import get_excel_data
from utils.mysql_util import DBConnection

order_no_list = []


@allure.epic('后管')
@allure.feature('B端订单模块')  # 测试类
class Test_add_Border(BaseApi, BaseAssert):
    @allure.story('b端订单新建')  # 接口名称
    @allure.title('新建B端订单用例')  # 用例的标题
    @pytest.mark.parametrize('caseTitle,inData,respData', get_excel_data(excelDir, 'B端订单', 'Border_add', *configData))
    @allure.title("{caseTitle}")
    def test_add_border(self, caseTitle, inData, respData):
        res = self.request_send(str(inData))
        self.define_api_assert(res, '=', respData)

    @allure.title('b端订单列表获取order_no')  # 用例的标题
    @pytest.mark.parametrize('caseTitle,inData,respData', get_excel_data(excelDir, 'B端订单', 'Border_list', *configData))
    @allure.title("{caseTitle}")
    def test_list_border(self, caseTitle, inData, respData):
        res = self.request_send(str(inData))
        # 获取order_no
        order_no = jsonpath.jsonpath(res, '$..order_no')[1]
        # 添加到列表，给下一个接口的sql语句使用
        order_no_list.append(order_no)
        self.define_api_assert(res, '=', respData)

    @allure.title('支付凭证上传')
    @pytest.mark.parametrize('caseTitle,inData,respData',
                             get_excel_data(excelDir, 'B端订单', 'Border_shangchuan', *configData))
    @allure.title("{caseTitle}")
    def test_shangchuan_border(self, caseTitle, inData, respData):
        with allure.step('数据库查询审核id'):
            # order_id = DBConnection().select(
            #     "SELECT id from dealer_shop_user_transfer_audit WHERE belong_user_id = '47298' order by id desc LIMIT 1")
            order_id = DBConnection().select(
                "SELECT id from dealer_shop_user_order WHERE order_no = %s" % order_no_list[-1])
            order_id = order_id[0][0]
            print('订单id>>:',order_id)
        with allure.step('上传支付凭证'):
            inData = eval(inData)  # 字符串转字典
            inData['id'] = order_id
            # print('indata???>>>',inData)
            res = self.request_send(str(inData))
            self.define_api_assert(res, '=', respData)

    @allure.title('支付审核')
    @pytest.mark.parametrize('caseTitle,inData,respData',
                             get_excel_data(excelDir, 'B端订单', 'Border_shenhe', *configData))
    @allure.title("{caseTitle}")
    def test_shenhe_border(self, caseTitle, inData, respData):
        with allure.step('数据库查询审核id'):
            shenhe_id = DBConnection().select(
                "SELECT id from dealer_shop_user_transfer_audit WHERE belong_user_id = '47298' order by id desc LIMIT 1")
            shenhe_id = shenhe_id[0][0]
            print('审核id>>:', shenhe_id)
        with allure.step('审核定金支付'):
            inData = eval(inData)
            inData['id'] = shenhe_id
            res = self.request_send(str(inData))
            self.define_api_assert(res, '=', respData)



if __name__ == '__main__':
    # 本地运行处理历史数据
    # 1- 生成报告所需的数据    --alluredir ../report/tmp
    pytest.main(['test_Border.py', '-s', '--alluredir', '../report/tmp'])  # -s 打印print信息
    # 2- 生成打开测试报告---自动打开报告的服务
    os.system('allure serve ../report/tmp  -o ./allure-report/ --clean')
