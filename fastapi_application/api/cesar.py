from fastapi import APIRouter, HTTPException, status

from core.schemas.cesar import CesarCrypt
from crypto.cesar import encrypt, decrypt

router = APIRouter()


@router.post("")
def caesar_encode(data: CesarCrypt):
    if data.operation== "encrypt":
        text = encrypt(text=data.text, shift=data.shift)
    elif data.operation== "decrypt":
        text = decrypt(encoded_text=data.text, shift=data.shift)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong operation! How?",
        )

    return text

