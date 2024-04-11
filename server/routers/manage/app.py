
import json
from fastapi import  APIRouter
from pydantic import BaseModel
from readMenuitemURL import config
router = APIRouter()

menuitemURLpath = 'menuitemURL.json'
configpath = 'config.json'
class Args(BaseModel):
    routerName: str=''
    permissions:int=0
    menuitemURL:dict={}
    
@router.get(f"/getmenuitem")
async def getmenuitem():
    return config.menuitemURL

@router.get(f"/getRouter")
async def getRouter():
    return config.config['routerName']
         
@router.post(f"/delRouter")
async def delRouter(args: Args):
    config.config['routerName'].remove(args.routerName)
    del config.menuitemURL[args.routerName]
    with open(configpath, 'w',encoding='utf-8') as f:
         f.write(json.dumps(config.config))
    with open(menuitemURLpath, 'w',encoding='utf-8') as f:
         f.write(json.dumps(config.menuitemURL))

@router.post(f"/reviseMenuitemURL")
async def reviseMenuitemURL(args: Args):
    config.menuitemURL[args.routerName] = args.menuitemURL
    with open(menuitemURLpath, 'w',encoding='utf-8') as f:
         f.write(json.dumps(config.menuitemURL))