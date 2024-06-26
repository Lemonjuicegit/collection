
from fastapi import  APIRouter
from pydantic import BaseModel
from readMenuitemURL import config
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
         