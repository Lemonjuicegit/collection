from fastapi import APIRouter
from uuid import uuid4
from routers.collection.vo import RouterArgs, RouterUpdate
from routers.collection.service import routerService
from routers.collection.result import Result


router = APIRouter()


@router.post("/router")
def routerControllerOne(args: RouterArgs):
    res = routerService.select({"path": args.path})
    return res[0]


@router.get("/item_tree")
def getDataItemTree(args: str):
    res = routerService.getDataItemTree(args)
    return Result(data=res)


@router.get("/tree")
async def getTree():
    res = routerService.getDataTree()
    return Result(data=res)


@router.post("/add")
def addRtouter(data: RouterUpdate):
    name = uuid4().hex
    routerService.insert([{**dict(data), "name": name}])
    res = routerService.select({"name": name})
    return Result(data=res)


@router.post("/update")
def upRouter(data: RouterUpdate):
    routerService.update([data.model_dump(exclude_unset=True)])
    return Result()


@router.delete("/delete")
def deleteDataItem(del_id: list[int]):
    routerService.delete(del_id)
    return Result()


@router.get("/eq_path")
def getPathList(path: str):
    res = routerService.select_all()
    path_list = [v.path for v in res]
    if path in path_list:
        return Result()
    else:
        return Result(code=404, msg="请求的网址不存在")


@router.get("/list")
def getList():
    res = routerService.select({"router_type": "collection"})
    return Result(data=res)
