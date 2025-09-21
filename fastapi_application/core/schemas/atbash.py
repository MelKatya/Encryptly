from pydantic import BaseModel

from core.config import ValidOperation


class AtbashCrypt(BaseModel):
    operation: ValidOperation
    text: str
