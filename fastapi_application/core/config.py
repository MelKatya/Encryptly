from typing import Literal

from pydantic import BaseModel

ValidOperation = Literal["encrypt", "decrypt"]


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class Settings(BaseModel):
    run: RunConfig = RunConfig()


settings = Settings()
