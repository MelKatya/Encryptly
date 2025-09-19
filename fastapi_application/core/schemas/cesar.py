from pydantic import BaseModel

from core.config import ValidOperation


class CesarCrypt(BaseModel):
    operation: ValidOperation
    text: str
    shift: int
