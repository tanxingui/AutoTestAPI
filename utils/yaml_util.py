#方法一(废弃):
# import os.path,yaml
#
# #获取项目的根目录
# def get_obj_path():
#     #通过项目路径，然后用configs进行切割
#     return os.path.dirname(__file__).split("configs")[0]
#
# #获取的项目路径跟yaml路径进行拼接
# def read_yaml(yamlpath):
#     # print(get_obj_path()+yamlpath)
#     with open(get_obj_path()+yamlpath,encoding='utf-8') as f:
#         #通过yaml的FullLoader方式去加载值,转化yaml数据为字典
#         return yaml.load(f,yaml.FullLoader)
#
# if __name__ == '__main__':
#     res = read_yaml("data/apiConfig.yaml")
#     print(res)

#方法二:
import yaml
def read_yamls(yamlpath): #获取多段的yaml，需要通过循环去取值
    with open(yamlpath,encoding='utf-8') as f:
        return yaml.safe_load_all(f.read())

def read_yaml(yamlpath):  #读取yaml文件
    with open(yamlpath,encoding='utf-8') as f:
        return yaml.safe_load(f.read())

def write_yamls(yamlpath,*data):  #将分段数据写入，进行数据装包操作
    with open(yamlpath,'a',encoding='utf-8') as f:
        yaml.safe_dump_all(data,f)

def write_yaml(yamlpath,data):  #将数据写入
    with open(yamlpath,'a',encoding='utf-8') as f:
        yaml.safe_dump(data,f)

if __name__ == '__main__':
    res = read_yaml('../data/apiConfig.yaml')
    # for i in res:
    #     print(i)
    print(res)
    # write_yaml('../data/apiConfig.yaml',{'aaa':'111'})  #单个数据传入
    # write_yamls('../data/apiConfig.yaml', {'aaa': '111'},[111,222],[{'name':985}])  #分段数据传入
