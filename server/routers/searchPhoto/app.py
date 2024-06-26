
from fastapi import  APIRouter,Query,Request,Response
from starlette.responses import FileResponse
from pydantic import BaseModel
from .. import search_picture,state,store,use,log

router = APIRouter()



@router.post("/get_photo_data")
async def get_photo_data(zj=Query(None)):
    res = search_picture(zj.split(','))
    return res

@router.post("/search")
async def get_photo_url(url, req: Request):
    ip = req.client.host
    filename = url.split('\\')[-1]
    log.info("create_download_file:%s",ip)
    with open(url, "rb") as image_f:
        imag_data = image_f.read()
    
    return Response(content=imag_data, media_type="image/jpeg")
        
    # 查找要下载的文件

    
