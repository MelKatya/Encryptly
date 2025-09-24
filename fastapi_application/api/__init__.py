from fastapi import APIRouter

from .cesar import router as cesar_router
from .vigenere import router as vigenere_router
from .atbash import router as atbash_router
from .vernam import router as vernam_router
from .playfair import router as playfair_router
from .rsa import router as rsa_router

router = APIRouter()

router.include_router(cesar_router, prefix="/cesar")
router.include_router(vigenere_router, prefix="/vigenere")
router.include_router(atbash_router, prefix="/atbash")
router.include_router(vernam_router, prefix="/vernam")
router.include_router(playfair_router, prefix="/playfair")
router.include_router(rsa_router, prefix="/rsa")
