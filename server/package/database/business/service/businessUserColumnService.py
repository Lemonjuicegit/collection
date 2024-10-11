from package.database import BaseService
from package.database.business.DO import BusinessUserColumn
from package.database.business.service import session


class BusinessUserColumnService(BaseService):
    def __init__(self) -> None:
        super().__init__(BusinessUserColumn, session)


businessUserColumnService = BusinessUserColumnService()
