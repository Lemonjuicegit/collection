from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()


class Args(BaseModel):
    shp: str = ""
    templaet: int = 0
    