from fastapi import APIRouter

from .cesar import router as cesar_router

router = APIRouter()

router.include_router(cesar_router, prefix="/cesar")

