
import json
from fastapi import  Request,APIRouter
from pydantic import BaseModel

router = APIRouter()

menuitemURLpath = 'menuitemURL.json'
configpath = r'config.json'
with open(menuitemURLpath, 'r',encoding='utf-8') as f:
    menuitemURL = json.loads(f.read())
with open(configpath, 'r',encoding='utf-8') as f:
    config = json.loads(f.read())
produce = 1

class Args(BaseModel):
    routerName: str=''
    permissions:int=0
    menuitemURL:dict={}

@router.get(f"/getRouter")
async def getRouter():
    return config['routerName']
         

@router.post(f"/delRouter")
async def delRouter(args: Args):
    config['routerName'].remove(args.routerName)
    del menuitemURL[args.routerName]
    with open(configpath, 'w',encoding='utf-8') as f:
         f.write(json.dumps(config))
    with open(menuitemURLpath, 'w',encoding='utf-8') as f:
         f.write(json.dumps(menuitemURL))

@router.post(f"/reviseMenuitemURL")
async def reviseMenuitemURL(args: Args):
    menuitemURL[args.routerName] = args.menuitemURL
    with open(menuitemURLpath, 'w',encoding='utf-8') as f:
         f.write(json.dumps(menuitemURL))