from sqlmodel import SQLModel
from package.database import TYPE

class PermissionDO(SQLModel, table=True):
    __tablename__ = "permission"
    
    id: int = TYPE.PRIMARY_KEY
    name:str = TYPE.UNIQUE
    permissions:str