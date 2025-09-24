from pydantic import BaseModel

from typing import Literal


class RsaGenerateKey(BaseModel):
    key_size: Literal[1024, 2048, 4096]


class RsaEncrypt(BaseModel):
    text: str
    public_key: str


class RsaDecrypt(BaseModel):
    text: str
    private_key: str
