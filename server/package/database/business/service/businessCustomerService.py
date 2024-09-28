from package.database import BaseService
from package.database.business.DO import BusinessCustomerDO
from package.database.business.service import session


class BusinessCustomerService(BaseService):
    def __init__(self) -> None:
        super().__init__(BusinessCustomerDO, session)


businessCustomerService = BusinessCustomerService()
