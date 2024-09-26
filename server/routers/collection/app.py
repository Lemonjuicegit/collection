from fastapi import APIRouter, Depends
from .hooks import include_router
from routers.collection.common.token import verify_token

router = APIRouter()


include_router(router)
