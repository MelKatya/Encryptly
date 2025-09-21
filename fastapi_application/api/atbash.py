from fastapi import APIRouter, HTTPException, status

from core.schemas.atbash import AtbashCrypt
from crypto.atbash import crypt

router = APIRouter()


@router.post("")
def atbash_encode(data: AtbashCrypt):
    if data.operation == "encrypt" or "decrypt":
        text = crypt(text=data.text)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong operation! How?",
        )

    return text

