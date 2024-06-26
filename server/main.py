import json,importlib,traceback
from fastapi import FastAPI,Request, UploadFile,File,BackgroundTasks
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from fastapi.responses import JSONResponse
from readMenuitemURL import config
from routers import store,unzip,log,use,Api,get_tbbh,state
from fastapiUtils import include_router,split_args,cell_return
from package.interface.setup import getFunc
static_dir_absolute = f"{config.cwdpath}\\static"
manage_dir_absolute = f"{config.cwdpath}\\manage"
home_dir_absolute = f"{config.cwdpath}\\home"
assets_dir_absolute = f"{config.cwdpath}\\static\\assets"

environment = 0

if environment:
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    app.mount("/assets", StaticFiles(directory=assets_dir_absolute), name="assets")
    app.mount("/home", StaticFiles(directory=home_dir_absolute, html=True), name="home")
    for router in config.routerName:
        app.mount(f"/{router}", StaticFiles(directory=static_dir_absolute, html=True), name=router)
    rewrite = '/api'
else:
    app = FastAPI()
    rewrite = ''

include_router(app,rewrite)
flhpath = r'\\Lzd202201031623\2023年度非粮化验收\1.举证照片成果'
flh_tbbh = get_tbbh()
for tbbh in flh_tbbh:
    try:
        app.mount(f"/{tbbh}", StaticFiles(directory=f"{flhpath}\\{tbbh}"), name=tbbh)
    except RuntimeError:
        pass
    
class Args(BaseModel):
    xm_name:str=''
    menuitemURL:dict={}
    menuitem:dict={}
    data:list=[]
    menuitemName:str=''
    title:str=''
    id:int=0
    routerName:str=''
    reviseRouterName:str=''
    usdel:int=0
    interArgs:dict={}

@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    exc_format = ''.join(traceback.format_exception(exc))
    log.error(exc_format)
    return {"state":state.ERR,"res":f"服务出错了!,请联系管理员!{exc}"}

@app.middleware("http")
async def check_static_access(request: Request, call_next):
    if request.url.path[1:] in config.re_routerName:
        return JSONResponse(content={"detail": "Static content access disabled."}, status_code=404)
    response = await call_next(request)
    return response
@app.post(f"{rewrite}/add_use")
async def add_use(req: Request):
    ip = req.client.host
    use.useApi[ip] = Api(ip)
    (store.uploadPath /ip).mkdir(exist_ok=True, parents=True)
    (store.sendPath / ip).mkdir(exist_ok=True, parents=True)
    log.info("%s连接",ip)
    return 1

@app.get(f"{rewrite}/disconnect")
async def use_disconnect(req: Request = None):
    ip = req.client.host
    store.drop_query(f"ip == '{ip}'")
    log.info("%s断开",ip)


@app.post(f"{rewrite}/upload")
async def create_upload_file(file:UploadFile=File(),filetype:str='', req: Request=None):
    ip = req.client.host
    log.info("upload:%s-%s",ip,file.filename)
    file_content = await file.read()
    filename = file.filename
    extractpath = store.uploadPath / ip / filename
    store.addUseFile(ip,store.uploadPath, filename)
    with open(extractpath, "wb") as buffer:
        buffer.write(file_content)
    if filetype == 'gdb':
        unzip(extractpath, store.uploadPath / ip)
        store.addUseFile(ip,store.uploadPath, f"{filename.split('.')[0]}.gdb")
        return filename
    if filetype == 'zip':
        namelist = unzip(extractpath, store.uploadPath / ip / file.filename)
        for f in namelist:
            store.addUseFile(ip,store.uploadPath, f)
    elif filetype == 'shp':
        filelist = unzip(extractpath, store.uploadPath / ip)
        for f in filelist:
            store.addUseFile(ip,store.uploadPath, f)
    return filename

@app.post(f"{rewrite}/download")
async def create_download_file(fileid,isdel, req: Request,task:BackgroundTasks):
    ip = req.client.host
    log.info("create_download_file:%s",ip)
    # 查找要下载的文件
    path = store.file_id(fileid,'all')

    if int(isdel):
        task.add_task(store.drop_query,f"ID == '{fileid}'")
    if path.shape[0]:
        return FileResponse(path.path.values[0], filename=path.filename.values[0])
    return state.ERR

@app.post(f"{rewrite}/getmenuitemURL")
async def getmenuitemURL(args: Args):
    log.info(args.xm_name)
    try:
        return config.menuitemURL[args.xm_name]["data"]
    except KeyError:
        log.err(f"'{args.xm_name}'路径不存在")

@app.post(f"{rewrite}/addmenuitemURL")
async def addmenuitemURL(args: Args):
    config.menuitemURL[args.xm_name]["data"].append(args.menuitemURL)
    config.upmenuitem()

@app.post(f"{rewrite}/setmenuitemName")
async def setmenuitemName(args: Args):
    config.menuitemURL[args.xm_name]["data"][args.id]['title'] = args.menuitemName
    config.upmenuitem()

@app.post(f"{rewrite}/gettitle")
async def getTitle(args: Args):
    return config.menuitemURL[args.xm_name]["title"]

@app.post(f"{rewrite}/settitle")
async def setTitle(args: Args):
    config.menuitemURL[args.xm_name]["title"] = args.title
    config.upmenuitem()

@app.post(f"{rewrite}/getPermissions")
async def getPermissions(args: Args):
    return config.menuitemURL[args.xm_name]["permissions"]

@app.post(f"{rewrite}/delmenuitemURL")
async def remove(args: Args):
    del config.menuitemURL[args.xm_name]["data"][args.id]
    config.upmenuitem()

@app.post(f"{rewrite}/revise_router")
async def reviseRouter(args: Args):
    temp = config.menuitemURL[args.routerName]
    del config.menuitemURL[args.routerName]
    config.menuitemURL[args.reviseRouterName] = temp
    if args.reviseRouterName in config.re_routerName:
        config.re_routerName.remove(args.reviseRouterName)
    config.re_routerName.append(args.routerName)
    app.mount(f"/{args.reviseRouterName}", StaticFiles(directory="static", html=True), name=args.routerName)
    config.upmenuitem()
        
         
@app.post(f"{rewrite}/upmenuitemURL")
async def upmenuitemURL(args: Args):
    config.menuitemURL[args.xm_name]['data'] = args.data
    config.upmenuitem()
    
@app.post(f"{rewrite}/cell")
async def cell(args:Args,req: Request=None):
    ip = req.client.host
    res = None
    func_item = getFunc(args.interArgs['id'])
    imported_module = importlib.import_module(func_item['module'])
    func = getattr(imported_module,func_item['name'])
    func_args = []
    if args.interArgs['args']:
        for k,v in enumerate(args.interArgs['args']):
            match func_item['args'][k]:
                case 'int':
                    func_args.append(int(v))
                case 'float':
                    func_args.append(float(v))
                case 'ip':
                    func_args.append(ip)
                case 'app':
                    func_args.append(app)
                case 'app':
                    func_args.append(app)
                case 'upload':
                    func_args.append(store.uploadPath / ip / v)
                case 'send':
                    func_args.append(store.sendPath / ip / v)
                case _:
                    func_args.append(v)

        if func_item['return']:
                res = cell_return(func_item['return'],func,func_args,ip)
        else:
            func(*func_args)
    else:
        if func_item['return']:
            res = cell_return(func_item['return'],func,func_args,ip)
        else:
            func(*func_args)
    return {"state":state.RES,"res":res}

if __name__ == "__main__":
    import uvicorn
    if environment:
        uvicorn.run(app, host="192.168.2.139", port=45454)
    else:
        uvicorn.run(app, host="192.168.2.51", port=45454)