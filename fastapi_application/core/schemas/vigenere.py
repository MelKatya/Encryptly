from pydantic import BaseModel

from core.config import ValidOperation


class VigenereCrypt(BaseModel):
    operation: ValidOperation
    text: str
    keyword: str