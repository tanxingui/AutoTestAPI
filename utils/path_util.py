#写法一：
import os
Path1 = os.path.dirname(__file__)   #上一级的文件路径
Path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #再上一级的文件路径，os.path.abspath返回绝对路径，\
# print(Path)   #项目的路径
#data路径
data_path =  os.path.join(Path,'data')
#logs路径
logs_path = os.path.join(Path,'logs')
# print(logs_path)
#report路径
report_path = os.path.join(Path,'report')
print(report_path)

# #写法二：
# import os
#
# Path = os.path.dirname(__file__).split('commcon')[0]  # 通过当前文件的路径，切割提取第一位，取出项目路径
# print(Path)
# # data路径
# data_path = Path + 'data'
# # logs路径
# logs_path = Path + 'logs'
# # report路径下的tmp
# report_tmp_path = Path + 'report'
# print(report_tmp_path)
