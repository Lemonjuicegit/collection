from sqlmodel import SQLModel
from routers.collection.common.TYPE import TYPE


class DeviceIpDO(SQLModel, table=True):
    __tablename__ = "device_ip"

    id: int = TYPE.PRIMARY_KEY
    title: str | None
    name: str = TYPE.UNIQUE
    ip: str
    grant:bool
