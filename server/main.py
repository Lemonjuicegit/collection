import json
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from routers import manage
from readMenuitemURL import config

app = FastAPI()
menuitemURLpath = r'.\menuitemURL.json'

# app.mount(f"/manage", StaticFiles(directory=f"manage", html=True), name="manage")
# app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")
for router in config.config['routerName']:
    app.mount(f"/{router}", StaticFiles(directory=f"static", html=True), name=router)
# rewrite = '/api'
rewrite = ''

app.include_router(manage.router,prefix=f"{rewrite}/managerouter",tags=["manage"],)
class Args(BaseModel):
    xm_name:str=''
    menuitemURL:dict={}
    data:list=[]
    menuitemName:str=''
    title:str=''
    id:int=0
    routerName:str=''
    
@app.post(f"{rewrite}/getmenuitemURL")
async def getmenuitemURL(args: Args):
    try:
        return config.menuitemURL[args.xm_name]["data"]
    except KeyError:
        return False

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
    config.menuitemURL[args.routerName] = {
        "menuitemURL":[],
    "title": args.routerName
    }
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
    uvicorn.run(app, host="192.168.2.51", port=55555)