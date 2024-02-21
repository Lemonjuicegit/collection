import json
from config import routerName
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

app = FastAPI()
menuitemURLpath = r'.\menuitemURL.json'
with open(menuitemURLpath, 'r',encoding='utf-8') as f:
    menuitemURL = json.loads(f.read())
produce = 0

if produce:

    app.mount(f"/{routerName[0]}", StaticFiles(directory=f"static/xm1", html=True), name=routerName[0])
    app.mount(f"/{routerName[1]}", StaticFiles(directory=f"static/xm2", html=True), name=routerName[1])
    app.mount(f"/{routerName[2]}", StaticFiles(directory=f"static/xm3", html=True), name=routerName[2])
    app.mount(f"/{routerName[3]}", StaticFiles(directory=f"static/xm4", html=True), name=routerName[3])
    app.mount(f"/{routerName[4]}", StaticFiles(directory=f"static/xm5", html=True), name=routerName[4])
    app.mount(f"/{routerName[5]}", StaticFiles(directory=f"static/xm6", html=True), name=routerName[5])
    app.mount(f"/{routerName[6]}", StaticFiles(directory=f"static/xm7", html=True), name=routerName[6])

    rewrite = '/api'
else:
    rewrite = ''
     
class Args(BaseModel):
    xm_name:str=''
    menuitemURL:dict={}
    title:str=''
    id:int=0
@app.post(f"{rewrite}/getmenuitemURL")
async def getmenuitemURL(args: Args):
    print(args.xm_name)
    return menuitemURL[args.xm_name]["menuitemURL"]

@app.post(f"{rewrite}/addmenuitemURL")
async def addmenuitemURL(args: Args):
    menuitemURL[args.xm_name]["menuitemURL"].append(args.menuitemURL)
    with open(menuitemURLpath, 'w',encoding='utf-8') as f:
         f.write(json.dumps(menuitemURL))

@app.post(f"{rewrite}/gettitle")
async def getTitle(args: Args):
    return menuitemURL[args.xm_name]["title"]

@app.post(f"{rewrite}/settitle")
async def setTitle(args: Args):
    menuitemURL[args.xm_name]["title"] = args.title
    with open(menuitemURLpath, 'w',encoding='utf-8') as f:
         f.write(json.dumps(menuitemURL))

@app.post(f"{rewrite}/delmenuitemURL")
async def remove(args: Args):
    del menuitemURL[args.xm_name]["menuitemURL"][args.id]
    with open(menuitemURLpath, 'w',encoding='utf-8') as f:
         f.write(json.dumps(menuitemURL))   

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.2.51", port=55555)