from routers.collection.service.service import Service
from routers.collection.do import RouterDO
from routers.utils import handleTree

class RouterService(Service):
    def __init__(self):
        super().__init__(RouterDO)

    def getDataItemTree(self, path):
        res = super().select({"path": path})
        data_item = [dict(x) for x in res[0].dataItem]
        result = handleTree(data_item, id="name", parentId="parent_name")

        return {**dict(res[0]), "dataItem": result}

    def getDataTree(self):
        router = super().select({"router_type": "collection"})
        result = {}
        for row in router:
            data_item = [dict(x) for x in row.dataItem]
            tree = handleTree(data_item, id="name", parentId="parent_name")
            result[row.name] = {**dict(row), "dataItem": tree}
        return result


routerService = RouterService()
