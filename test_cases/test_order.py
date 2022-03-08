import os
import time
import jsonpath
import pytest
from commcon.baseApi import BaseAssert
from utils.path_util import report_path
from configs.config import excelDir, configData
from commcon.baseLei import Add_b, Add_c
from utils.excel_util import get_excel_data

@pytest.mark.Border #allure报告B端订单名字的标签
# @pytest.mark.skip(reason = '这个类用例不运行！ ----强行不执行--注释')
@pytest.mark.skipif(1==2,reason='跳过这个类，跳过类中所有方法')
class Test_Border(BaseAssert):
    @pytest.mark.parametrize('inBody,exData',get_excel_data(excelDir,'B端订单','Border',*configData))
    def test_borDer(self,inBody,exData):
        inBody = str(inBody)
        res = Add_b(inBody).add_b()
        #用jsonpath去获取errcode的值
        res = jsonpath.jsonpath(res, '$.errcode')
        exData = jsonpath.jsonpath(exData,'$.errcode')
        self.define_api_assert(res,'=',exData)

@pytest.mark.Corder #C端订单名字的标签
class Test_Corder(BaseAssert):
    @pytest.mark.parametrize('inBody,exData',get_excel_data(excelDir,'C端订单','Corder',*configData))
    def test_corDer(self,inBody,exData):
        inBody = str(inBody)
        res = Add_c(inBody).add_c()
        self.define_api_assert(res['errcode'],'=',exData['errcode'])

# 啊啊啊
if __name__ == '__main__':
    time.sleep(1)
    pytest.main(['test_order.py', '-vs', '--alluredir', f'{report_path}','--clean-alluredir'])
    # os.system(f'allure generate {report_path}')  #serve是自动打开
    os.system(f'allure serve {report_path}')  #serve是自动打开
