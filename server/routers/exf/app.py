
import json
from fastapi import  APIRouter,Request
from pydantic import BaseModel
from readMenuitemURL import config
from . import exf,lq_exf
from ..Store import state,store
router = APIRouter()

class Args(BaseModel):
    gdb: str=''
    
@router.get(f"/lq_exf")
async def lqexf(args: Args,req: Request=None):
    ip = req.client.host
    gdb = store.useFile[store.useFile.filename == args.gdb].path.values[0]
    
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