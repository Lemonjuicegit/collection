from routers.collection.service.service import Service
from routers.collection.do import DataItemDO
from routers.utils import handleTree


class DataItemService(Service):
    def __init__(self):
        super().__init__(DataItemDO)



dataItemService = DataItemService()
