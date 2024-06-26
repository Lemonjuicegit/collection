import json
from pathlib import Path
from typing import List
from uuid import uuid4

cwdpath = Path(__file__).parent / "interface.json"

interface_json = json.loads(cwdpath.read_text(encoding="utf-8"))


def getInterface():
    interface_data = json.loads(cwdpath.read_text(encoding="utf-8"))
    return interface_data['interface']

def Select_id():
    def recursion(children,depth='',result=None):
        if result is None:
            result = {}
        for index,item in enumerate(children):
            if item['child']:
                result[item['id']] = f"{depth}-{index}" if depth else str(index)
            else:
                result[item['id']] = f"{depth}-{index}" if depth else str(index)
                recursion(item['children'],index,result)
        return result
    res = recursion(getInterface())
    interface_json['select_id'] = res
    with cwdpath.open('w', encoding='utf-8') as f:
        f.write(json.dumps(interface_json))

def getFunc(select_id: List[int]):
    res = None
    for index in select_id:
        if res is None:
            res = getInterface()[int(index)]
        else:
            res = res['children'][int(index)]
    return res
    
def upInterface(interface_str):
    pass
    
      
if __name__ == '__main__':
    # Select_id()
    getFunc('3')
     
        
