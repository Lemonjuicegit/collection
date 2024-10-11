from package.database import BaseService
from package.database.business.DO import BusinessCoreColumn
from package.database.business.service import session


class BusinessCoreColumnService(BaseService):
    def __init__(self) -> None:
        super().__init__(BusinessCoreColumn, session)


businessCoreColumnService = BusinessCoreColumnService()
