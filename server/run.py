import json
from fastapi import FastAPI,Request, UploadFile,File
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from routers import manage,exf,searchPhoto
from readMenuitemURL import config
from routers import store,unzip,log,use,Api,get_tbbh

static_dir_absolute = f"{config.cwdpath}\\static"
manage_dir_absolute = f"{config.cwdpath}\\manage"
home_dir_absolute = f"{config.cwdpath}\\home"
assets_dir_absolute = f"{config.cwdpath}\\static\\assets"
app = FastAPI()

menuitemURLpath = r'.\menuitemURL.json'

flhpath = r'\\Lzd202201031623\2023年度非粮化验收\1.举证照片成果'
flh_tbbh = get_tbbh()

app.mount("/manage", StaticFiles(directory=manage_dir_absolute, html=True), name="manage")
app.mount("/assets", StaticFiles(directory=assets_dir_absolute), name="assets")
app.mount("/home", StaticFiles(directory=home_dir_absolute, html=True), name="home")
for tbbh in flh_tbbh:
    try:
        app.mount(f"/{tbbh}", StaticFiles(directory=f"{flhpath}\\{tbbh}"), name=tbbh)
    except RuntimeError:
        pass
for router in config.config['routerName']:
    app.mount(f"/{router}", StaticFiles(directory=static_dir_absolute, html=True), name=router)
rewrite = '/api'
rewrite = ''

app.include_router(manage.router,prefix=f"{rewrite}/manage",tags=["manage"],)
app.include_router(exf.router,prefix=f"{rewrite}/exf",tags=["exf"],)
app.include_router(searchPhoto.router,prefix=f"{rewrite}/searchPhoto",tags=["searchPhoto"],)

class Args(BaseModel):
    xm_name:str=''
    menuitemURL:dict={}
    menuitem:dict={}
    data:list=[]
    menuitemName:str=''
    title:str=''
    id:int=0
    routerName:str=''
 
@app.post(f"{rewrite}/add_use")
async def add_use(req: Request):
    ip = req.client.host
    use.useApi[ip] = Api(ip)
    (store.uploadPath /ip).mkdir(exist_ok=True, parents=True)
    (store.sendPath / ip).mkdir(exist_ok=True, parents=True)
    log.info(f"{ip}连接")
    return 1

@app.post(f"{rewrite}/upload")
async def create_upload_file(file:UploadFile=File(),filetype:str='', req: Request=None):
    ip = req.client.host
    log.info(f"upload:{ip}-{file.filename}")
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
async def create_download_file(filename, req: Request):
    ip = req.client.host
    log.info(f"create_download_file:{ip}")
    # 查找要下载的文件
    path = store.useFile[
        (store.useFile.ip == ip)
        & ((store.useFile.name == filename) | (store.useFile.filename == filename))
    ]
    if path.shape[0]:
        return FileResponse(path.path.values[0], filename=path.filename.values[0])
    else:
        return 0


@app.post(f"{rewrite}/getmenuitemURL")
async def getmenuitemURL(args: Args):
    log.info(f"{args.xm_name}")
    try:
        return config.menuitemURL[args.xm_name]["data"]
    except KeyError:
        log.err(f"'{args.xm_name}'路径不存在")

@app.post(f"{rewrite}/addmenuitemURL")
async def addmenuitemURL(args: Args):
    config.menuitemURL[args.xm_name]["data"].append(args.menuitemURL)
    with open(menuitemURLpath, 'w',encoding='utf-8') as f:
         f.write(json.dumps(config.menuitemURL))

@app.post(f"{rewrite}/setmenuitemName")
async def setmenuitemName(args: Args):
    config.menuitemURL[args.xm_name]["data"][args.id]['title'] = args.menuitemName
    with open(menuitemURLpath, 'w',encoding='utf-8') as f:
         f.write(json.dumps(config.menuitemURL))

@app.post(f"{rewrite}/gettitle")
async def getTitle(args: Args):
    return config.menuitemURL[args.xm_name]["title"]

@app.post(f"{rewrite}/settitle")
async def setTitle(args: Args):
    config.menuitemURL[args.xm_name]["title"] = args.title
    with open(menuitemURLpath, 'w',encoding='utf-8') as f:
         f.write(json.dumps(config.menuitemURL))

@app.post(f"{rewrite}/getPermissions")
async def getPermissions(args: Args):
    return config.menuitemURL[args.xm_name]["permissions"]

@app.post(f"{rewrite}/delmenuitemURL")
async def remove(args: Args):
    del config.menuitemURL[args.xm_name]["data"][args.id]
    with open(menuitemURLpath, 'w',encoding='utf-8') as f:
         f.write(json.dumps(config.menuitemURL))


@app.post(f"{rewrite}/addRouter")
async def addRouter(args: Args):
    app.mount(f"/{args.routerName}", StaticFiles(directory=f"static", html=True), name=args.routerName)
    config.config['routerName'].append(args.routerName)
    config.menuitemURL[args.routerName] = Args.menuitem
    with open(r".\config.json", 'w',encoding='utf-8') as f:
         f.write(json.dumps(config.config))
    with open(menuitemURLpath, 'w',encoding='utf-8') as f:
         f.write(json.dumps(config.menuitemURL))
         
@app.post(f"{rewrite}/upmenuitemURL")
async def upmenuitemURL(args: Args):
    config.menuitemURL[args.xm_name]['data'] = args.data
    with open(menuitemURLpath, 'w',encoding='utf-8') as f:
         f.write(json.dumps(config.menuitemURL))

if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="192.168.2.139", port=45454)
    uvicorn.run(app, host="192.168.2.51", port=45454)