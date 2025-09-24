from fastapi import APIRouter

from core.schemas.rsa import RsaGenerateKey, RsaKeyRead, RsaEncrypt, RsaDecrypt
from crypto.rsa import create_keys, encrypt, decrypt

router = APIRouter()


@router.post("/generate_keys")
def generate_keys(data: RsaGenerateKey) -> RsaKeyRead:
    private_key, public_key = create_keys(key_size=data.key_size)
    return RsaKeyRead(private_key=private_key, public_key=public_key)


@router.post("/encrypt")
def rsa_encrypt(data: RsaEncrypt) -> str:
    encrypted_text = encrypt(text=data.text, public_pem=data.public_key)
    return encrypted_text


@router.post("/decrypt")
def rsa_decrypt(data: RsaDecrypt) -> str:
    decrypted_text = decrypt(encoded_text=data.text, private_pem=data.private_key)
    return decrypted_text