from typing import List
from sqlmodel import SQLModel, Relationship
from routers.collection.common.TYPE import TYPE


class RouterDO(SQLModel, table=True):
    __tablename__ = "router"
    id: int = TYPE.PRIMARY_KEY
    title: str
    name: str = TYPE.UNIQUE
    path: str | None
    router_type: str | None

    dataItem: List["DataItemDO"] | None = Relationship(
        back_populates="router", passive_deletes=True
    )  # type: ignore # noqa: F821
