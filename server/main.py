import json
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

app = FastAPI()
menuitemURLpath = r'.\menuitemURL.json'
with open(menuitemURLpath, 'r',encoding='utf-8') as f:
    menuitemURL = json.loads(f.read())
with open(r".\config.json", 'r',encoding='utf-8') as f:
    config = json.loads(f.read())
produce = 1

if produce:
    for router in config['routerName']:
        app.mount(f"/{router}", StaticFiles(directory=f"static", html=True), name=router)
    rewrite = '/api'
else:
    rewrite = ''
     
class Args(BaseModel):
    xm_name:str=''
    menuitemURL:dict={}
    menuitemName:str=''
    title:str=''
    id:int=0
    routerName:str=''
    
@app.post(f"{rewrite}/getmenuitemURL")
async def getmenuitemURL(args: Args):
    return menuitemURL[args.xm_name]["menuitemURL"]

@app.post(f"{rewrite}/addmenuitemURL")
async def addmenuitemURL(args: Args):
    menuitemURL[args.xm_name]["menuitemURL"].append(args.menuitemURL)
    with open(menuitemURLpath, 'w',encoding='utf-8') as f:
         f.write(json.dumps(menuitemURL))

@app.post(f"{rewrite}/setmenuitemName")
async def setmenuitemName(args: Args):
    menuitemURL[args.xm_name]["menuitemURL"][args.id]['title'] = args.menuitemName
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

@app.post(f"{rewrite}/addRouter")
async def addRouter(args: Args):
    app.mount(f"/{args.routerName}", StaticFiles(directory=f"static", html=True), name=args.routerName)
    config['routerName'].append(args.routerName)
    with open(r".\config.json", 'w',encoding='utf-8') as f:
         f.write(json.dumps(config))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.2.51", port=55555)