
from fastapi import  APIRouter
from pydantic import BaseModel
from readMenuitemURL import config
from routers.collection.vo import *
from routers.manage.service import manageService
from routers.collection.result import Result

router = APIRouter()

class Args(BaseModel):
    routerName: str=''
    permissions:int=0
    menuitemURL:dict={}
    
@router.get("/getmenuitem")
async def getmenuitem():
    return config.getMenuitem()
 
@router.post("/delRouter")
async def delRouter(args: Args):
    config.routerName.remove(args.routerName)
    del config.menuitemURL[args.routerName]
    config.upmenuitem()

@router.post("/reviseMenuitemURL")
async def reviseMenuitemURL(args: Args):
    config.menuitemURL[args.routerName] = args.menuitemURL
    config.upmenuitem()
    
@router.get("/tree")
async def get_tree():
    res = manageService.getDataItemTree()
    return Result(data=res)
    
@router.post("/add_router")
def add_router(args: RouterUpdate):
    
    pass
         