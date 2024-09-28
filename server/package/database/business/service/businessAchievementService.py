from package.database import BaseService
from package.database.business.DO import BusinessAchievementDO
from package.database.business.service import session


class BusinessAchievementService(BaseService):
    def __init__(self) -> None:
        super().__init__(BusinessAchievementDO, session)


businessAchievementService = BusinessAchievementService()
