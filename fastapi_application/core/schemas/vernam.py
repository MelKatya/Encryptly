from pydantic import BaseModel

from core.config import ValidOperation


class VernamCrypt(BaseModel):
    operation: ValidOperation
    text: str
    keyword: str