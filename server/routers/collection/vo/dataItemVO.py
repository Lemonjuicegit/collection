from pydantic import BaseModel

class addDataItemArgs(BaseModel):
    title: str
    URL: str | None = None
    path: str | None = None
    color: str = "#79bbff"
    parent_name: str
    router_name: str
    is_group: bool
    
class DataItemArgs(BaseModel):
    id:int = None
    title: str = None
    URL: str = None
    path: str = None
    color: str = None
    parent_name: str = None
    router_name: str = None
    is_group: bool = None