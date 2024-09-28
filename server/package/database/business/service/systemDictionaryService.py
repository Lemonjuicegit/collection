from package.database import BaseService
from package.database.business.DO import SystemDictionaryDO
from package.database.business.service import session


class SystemDictionaryService(BaseService):
    def __init__(self) -> None:
        super().__init__(SystemDictionaryDO, session)


systemDictionaryService = SystemDictionaryService()
