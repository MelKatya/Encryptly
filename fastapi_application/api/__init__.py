from fastapi import APIRouter

from .cesar import router as cesar_router
from .vigenere import router as vigenere_router
from .atbash import router as atbash_router

router = APIRouter()

router.include_router(cesar_router, prefix="/cesar")
router.include_router(vigenere_router, prefix="/vigenere")
router.include_router(atbash_router, prefix="/atbash")
