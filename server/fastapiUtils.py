import importlib
from uuid import uuid4
from routers import store,unzip,log,use,Api,get_tbbh,state,zip_list

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
    file_id = str(uuid4())
    for v in return_list:
        match v:
            case "filelist":
                use.useApi[ip].zipFileName = func(*args)
                name = use.useApi[ip].zipFileName[0].stem
                zip_list(use.useApi[ip].zipFileName,store.sendPath / ip / f'{name}.zip')
                store.addUseFile(ip, store.sendPath, f'{name}.zip',file_id)
                use.drop_zipFile(ip)
                use.useApi[ip].zipFileName = []
                return file_id
            case _:
                return func(*args)
                
