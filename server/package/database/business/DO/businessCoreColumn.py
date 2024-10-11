from sqlmodel import SQLModel
from package.database import TYPE
from datetime import date


class BusinessCoreColumn(SQLModel, table=True):
    __tablename__ = "business_core_column"
    id: int = TYPE.PRIMARY_KEY
    module: str = None
    column_name: str = None
    column_cn: str = None
    searchable: int = None
    column_type: str = None
    search_type: str = None
    condition: str = None
    dic_id: int = None
    deleted: int = None
    creator: str = None
    updater: str = None
    create_time: date = None
    update_time: date = None
    sort: int = None
    original: int = None
    parent_name: str = None
    formatter: str = None
    viewable: int = None
    min_width: int = None
    param_type: str = None
    date_formatter: str = None
    number_formatter: str = None
