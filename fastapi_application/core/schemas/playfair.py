from pydantic import BaseModel

from core.config import ValidOperation, ValidLanguage


class PlayfairCrypt(BaseModel):
    operation: ValidOperation
    text: str
    keyword: str
    vocabulary: ValidLanguage