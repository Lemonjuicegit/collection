import importlib,inspect,sys
from typing import Any, List
from uuid import uuid4
from routers import store,unzip,log,use,Api,get_tbbh,state,zip_list
import importlib

def include_router(app,rewrite):
    # 批量挂载路由
    modules = ['routers.manage','routers.exf','routers.searchPhoto','routers.coordinateStr']
    for module in modules:
        imported_module = importlib.import_module(module)
        tag = module.split('.')[-1]
        app.include_router(imported_module.router,prefix=f"{rewrite}/{tag}",tags=[tag],)
        
def split_args(args:str)->dict:
    args = args.split('&')
    args = list(map(lambda x:x.split('='),args))
    args = dict(args)
    return args

def cell_return(return_list,func,args,ip):
    '''
    处理有返回值的接口
    '''
    file_id = str(uuid4())
    for v in return_list:
        match v:
            case "filelist":
                use.useApi[ip].zipFileName = func(*args)
                name = use.useApi[ip].zipFileName[0].stem
                zip_list(use.useApi[ip].zipFileName,store.sendPath / ip / f'{name}.zip')
                file_id = store.addUseFile(ip, store.sendPath, f'{name}.zip')
                use.drop_zipFile(ip)
                use.useApi[ip].zipFileName = []
                return file_id
            case _:
                if args:
                    return func(*args)
                else:
                    return func()
            
def reload_module(module_name):
    """递归地重新加载模块"""
    importlib.reload(module_name)  # 重新加载当前模块
    for attr_name in dir(module_name):  # 遍历模块的所有属性
        attr = getattr(module_name, attr_name)
        if isinstance(attr, type(importlib.import_module)):  # 检查是否为模块类型
            sub_module_name = f"{module_name}.{attr_name}"
            reload_module(sub_module_name)  # 递归重新加载子模块
            


                
