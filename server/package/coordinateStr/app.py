import json,sys
from pathlib import Path
from uuid import uuid4
from fastapi import Request
from routers import store,state,zip_list
from . import gardens
    
current = Path(store.cwdpath) / 'routers' / 'coordinateStr'
templaet_list = json.loads((Path(current) / 'templaet.json').read_text(encoding="utf-8"))
async def coordinate_str(shpname,templaet:int,ip):
    jd = store.sendPath / ip / '节点.shp'
    file_id = str(uuid4())
    shp_path = store.useFile[store.useFile.filename == f'{shpname}.zip']
    if not shp_path.shape[0]:
        return {'state':state.ERR,'res':'未找到该文件'}
    gar = gardens(jd,shp_path.path.values[0],templaet_list[templaet])
    shpfiles =list((store.sendPath / ip).glob('节点.*'))

    gar.get_coordinate_string(store.sendPath / ip / f'{shpname}.txt')
    shpfiles.append(store.sendPath / ip / f'{shpname}.txt') 
    zip_list(shpfiles,store.sendPath / ip / f"{shpname}.zip")
    store.addUseFile(ip,store.sendPath,f'{shpname}.zip',file_id)
    for shpfile in shpfiles:
        shpfile.unlink()
    return {'state':state.END,'res':'txt坐标串完成','fileID':file_id}


