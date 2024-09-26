from fastapi import APIRouter
from routers.collection.service import deviceIpService

router = APIRouter()

@router.get("/device")
def getDeviceIpList():
    return deviceIpService.select_all()
