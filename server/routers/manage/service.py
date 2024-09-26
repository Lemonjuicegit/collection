from routers.collection.do import RouterDO,DataItemDO,DeviceIpDO
from routers.collection.service import Service
from routers.utils import handleTree


class ManageService:
    def __init__(self):
        self.dataItemService = Service(DataItemDO)
        self.routerService = Service(RouterDO)
        self.deviceService = Service(DeviceIpDO)
        
    def getDataItemTree(self):
        router = self.routerService.select_all()
        result = {}
        for row in router:
            data_item = [dict(x) for x in row.dataItem]
            tree = handleTree(data_item, id="name", parentId="parent_name")
            result[row.name] = {
                'title':row.title,
                'path':row.path,
                'data':tree
            }
        return result
    
    
manageService = ManageService()