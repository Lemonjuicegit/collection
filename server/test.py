from routers.manage.service import ManageService
serv = ManageService()
res = serv.dataItemService.select({'id':1})
# res = serv.getDataItemTree()
print(res)