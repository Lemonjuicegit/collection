import traceback
from fastapi import FastAPI, Query, Request, UploadFile, File, BackgroundTasks
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers import store, unzip, log, use, Api, get_tbbh, state
from fastapiUtils import include_router, handle, cwdpath
from routers.collection.common.token import create_access_token
from routers.collection.result import Result
from routers.collection.service import deviceIpService

ip_list = deviceIpService.getIpList()
manage_dir_absolute = f"{cwdpath}\\manage"
home_dir_absolute = f"{cwdpath}\\home"
assets_dir_absolute = f"{cwdpath}\\static\\assets"
assets_manage_absolute = f"{cwdpath}\\manage\\assets"
environment = 1
if environment:
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    app.mount(
        "/manage", StaticFiles(directory=manage_dir_absolute, html=True), name="manage"
    )
    app.mount("/assets", StaticFiles(directory=assets_manage_absolute), name="assets")
    app.mount("/home", StaticFiles(directory=home_dir_absolute, html=True), name="home")
    rewrite = ""
else:
    app = FastAPI()
    rewrite = ""

# @app.middleware("http")
# async def check_static_access(request: Request, call_next):
#     if request.url.path[1:] in config.re_routerName:
#         return JSONResponse(
#             content={"detail": "Static content access disabled."}, status_code=404
#         )
#     print(request)
#     response = await call_next(request)
#     return response

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
include_router(app, rewrite)
flhpath = r"\\Lzd202201031623\2023年度非粮化验收\1.举证照片成果"
flh_tbbh = get_tbbh()
for tbbh in flh_tbbh:
    try:
        app.mount(f"/{tbbh}", StaticFiles(directory=f"{flhpath}\\{tbbh}"), name=tbbh)
    except RuntimeError:
        pass


class Args(BaseModel):
    xm_name: str = ""
    menuitemURL: dict = {}
    menuitem: dict = {}
    data: list = []
    menuitemName: str = ""
    title: str = ""
    id: int = 0
    routerName: str = ""
    reviseRouterName: str = ""
    usdel: int = 0
    interArgs: dict = {}


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    exc_format = "".join(traceback.format_exception(exc))
    log.error(exc_format)
    return {"state": state.ERR, "res": f"服务出错了!,请联系管理员!{exc}"}


@app.post(f"{rewrite}/add_use")
async def add_use(req: Request):
    ip = req.client.host
    use.useApi[ip] = Api(ip)
    (store.uploadPath / ip).mkdir(exist_ok=True, parents=True)
    (store.sendPath / ip).mkdir(exist_ok=True, parents=True)
    log.info("%s连接", ip)
    return 1


@app.get(f"{rewrite}/disconnect")
async def use_disconnect(req: Request = None):
    ip = req.client.host
    store.drop_query(f"ip == '{ip}'")
    log.info("%s断开", ip)


@app.post(f"{rewrite}/upload")
async def create_upload_file(
    file: UploadFile = File(), filetype: str = "", req: Request = None
):
    ip = req.client.host
    log.info("upload:%s-%s", ip, file.filename)
    file_content = await file.read()
    filename = file.filename
    extractpath = store.uploadPath / ip / filename
    center_id = store.addUseFile(ip, store.uploadPath, filename)
    res = {"center_file_id": center_id, "engender": []}
    with open(extractpath, "wb") as buffer:
        buffer.write(file_content)
    if filetype == "gdb":
        unzip(extractpath, store.uploadPath / ip)
        engender = store.addUseFile(
            ip, store.uploadPath, f"{filename.split('.')[0]}.gdb"
        )
        res["engender"] = engender
        return res
    if filetype == "zip":
        namelist = unzip(extractpath, store.uploadPath / ip / file.filename)
        for f in namelist:
            res["engender"].append(store.addUseFile(ip, store.uploadPath, f))
    elif filetype == "shp":
        filelist = unzip(extractpath, store.uploadPath / ip)
        for f in filelist:
            if f.endswith(".shp"):
                res["shp"] = store.addUseFile(ip, store.uploadPath, f)
                res["engender"].append(res["shp"])
                continue
            res["engender"].append(store.addUseFile(ip, store.uploadPath, f))
    return res


@app.post(f"{rewrite}/download")
async def create_download_file(fileid, isdel, req: Request, task: BackgroundTasks):
    ip = req.client.host
    log.info("create_download_file:%s", ip)
    # 查找要下载的文件
    path = store.file_id(fileid, "path")
    if int(isdel):
        task.add_task(store.drop_query, f"ID == '{fileid}'")
    if path:
        return FileResponse(path, filename=path.name)
    return state.ERR


if environment:

    @app.get("/{xm_name}")
    async def getHtml(xm_name):
        return FileResponse(rf"{cwdpath}/manage/index.html")


async def cell(args: Args, query=Query(None), req: Request = None):
    res = handle(args, app, query, req)
    return res


@app.get("/get_user")
async def get_user(req: Request):
    ip = req.client.host
    if ip not in ip_list:
        return Result(code=401, msg="设备没有权限访问!")
    token = create_access_token({"ip": ip})
    device = deviceIpService.select({"ip": ip})
    return Result(data={"accessToken": token, "device": device[0]})


if __name__ == "__main__":
    import uvicorn

    if environment == 1:
        uvicorn.run(app, host="192.168.2.139", port=45454)
    else:
        uvicorn.run(app, host="192.168.2.51", port=45454)
        # uvicorn.run(app, host="127.0.0.0", port=45454)
