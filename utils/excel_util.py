from xlutils.copy import copy
import xlrd, json
from configs.config import configData
from configs.config import excelDir


# 把获取的单元格内容转为字典
def is_json(isStr):
    try:
        isStr = json.loads(isStr)
    except:
        return False
    return isStr


# 读取用户所需要的单元格内容
def get_excel_data(excelDir, sheetName, caseName, *colName, selectCase=['all']):  # 对用户输入的列名进行装包
    """
    :param excelDir: 文件路径
    :param sheetName: 模块名字
    :param caseName: 用例名字
    :param colName: 要获取的列名
    :param selectCase: 要获取的行数
    :return: 返回表格内单元格的内容
    """
    # 把execl加载到内存打开,formatting_info=True按照原格式读取内容
    workbook = xlrd.open_workbook(excelDir, formatting_info=True)
    # 获取对应的sheet
    # print(workbook.sheet_names())
    workSheet = workbook.sheet_by_name(sheetName)
    # 获取第一行
    # print(workSheet.row_values(0))
    # 获取第一列
    # print(workSheet.col_values(0))
    # 获取单元格
    # print(workSheet.cell_value(1,8))  #cell_value(行号，列号)
    colIndxList = []  # 存放用户输入的列名，转换后的列编号
    for i in colName:  # 遍历用户输入的列名
        colIndxList.append(workSheet.row_values(0).index(i))  # 用第一行里的列名去获取下标值
    # print(colIndxList)
    selectData = []  # 存放要获取的列名
    if 'all' in selectCase:
        selectData = workSheet.col_values(0)
    else:  # ['001','003-006']
        for i in selectCase:
            if '-' in i:  # 判断输入的列名是不是分段的
                start, end = i.split('-')
                for a in range(int(start), int(end) + 1):  # 切割后取范围
                    selectData.append(caseName + '_' + f'{a:0>3}')  # 拼接列名，不够3位数左边补0，符合Excel表列名命名规则
            else:
                selectData.append(caseName + '_' + f'{i:0>3}')
    # print(selectData)

    resList = []  # 存放Excel读取的结果
    idex = 0
    for i in workSheet.col_values(0):  # 遍历第1列
        if caseName in i and i in selectData:
            getData = []  # 存放一行中很多列的数据
            for colInd in colIndxList:
                res = workSheet.cell_value(idex, colInd)  # 获取某个单元格的内容
                if is_json(res):  # 如果单元格的内容转字典不报错，直接转成字典
                    res = is_json(res)
                getData.append(res)
            resList.append((getData))
        idex += 1
    return resList


# 向单元格写入结果
def write_value(self, row, col, value):
    data = xlrd.open_workbook(self.file)  # 打开文件
    data_copy = copy(data)  # 复制原文件
    sheet = data_copy.get_sheet(0)  # 取得复制文件的sheet对象
    sheet.write(row, col, value)  # 在某一单元格写入value
    data_copy.save(self.file)  # 保存文件


if __name__ == '__main__':
    shuju = get_excel_data(excelDir, 'B端订单', 'Border', *configData, selectCase=['001-003'])  # 对列名进行拆包的操作
    # print(aaa)
    for i in shuju:
        print(i)
