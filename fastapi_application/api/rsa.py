from fastapi import APIRouter

from core.schemas.rsa import RsaGenerateKey, RsaKeyRead
from crypto.rsa import create_keys, encrypt, decrypt

router = APIRouter()


@router.post("/generate_keys")
def generate_keys(data: RsaGenerateKey) -> RsaKeyRead:
    private_key, public_key = create_keys(key_size=data.key_size)
    return RsaKeyRead(private_key=private_key, public_key=public_key)

