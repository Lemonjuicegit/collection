from package.database import BaseService
from package.database.business.DO import BusinessContractDO
from package.database.business.service import session


class BusinessContractService(BaseService):
    def __init__(self) -> None:
        super().__init__(BusinessContractDO, session)


businessContractService = BusinessContractService()
