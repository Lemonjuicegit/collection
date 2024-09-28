from package.database import BaseService
from package.database.business.DO import BusinessProjectDO
from package.database.business.service import session


class BusinessProjectService(BaseService):
    def __init__(self) -> None:
        super().__init__(BusinessProjectDO, session)


businessProjectService = BusinessProjectService()
