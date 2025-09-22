from fastapi import APIRouter, HTTPException, status

from core.schemas.vernam import VernamCrypt
from crypto.vernam import encrypt, decrypt

router = APIRouter()


@router.post("")
def vernam_encode(data: VernamCrypt):
    if data.operation== "encrypt":
        text = encrypt(text=data.text, keyword=data.keyword)
    elif data.operation== "decrypt":
        text = decrypt(encoded_text=data.text, keyword=data.keyword)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong operation! How?",
        )

    return text