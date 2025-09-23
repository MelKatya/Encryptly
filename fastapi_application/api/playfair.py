from fastapi import APIRouter, HTTPException, status

from core.schemas.playfair import PlayfairCrypt
from crypto.playfair import encrypt, decrypt

router = APIRouter()


@router.post("")
def playfair_encode(data: PlayfairCrypt):
    if data.operation== "encrypt":
        text = encrypt(text=data.text, keyword=data.keyword, vocabulary=data.vocabulary)
    elif data.operation== "decrypt":
        text = decrypt(encoded_text=data.text, keyword=data.keyword, vocabulary=data.vocabulary)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong operation! How?",
        )

    return text