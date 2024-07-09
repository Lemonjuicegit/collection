import json
from pathlib import Path
from routers import store,state,zip_list
from .execute import gardens
    
current = Path(store.cwdpath) / 'package' / 'coordinateStr'
templaet_list = json.loads((Path(current) / 'template.json').read_text(encoding="utf-8"))
def coordinate_txt(shppath,templaet,ip):
    jd = store.sendPath / ip / '节点.shp'
    if not shppath.exists():
        return {'state':state.ERR,'res':'未找到该文件'}
    if templaet['default']:
        gar = gardens(jd,shppath,Path(templaet_list[int(templaet['default'])]))
    else:
        temp_file = store.file_id(templaet['file_id'],'path')
        gar = gardens(jd,shppath,temp_file)
    shpfiles = list((store.sendPath / ip).glob('节点.*'))
    save_path = gar.get_coordinate_string(store.sendPath / ip / f'{shppath.stem}.txt')
    shpfiles.insert(0,save_path)
    return shpfiles


