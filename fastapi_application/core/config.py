from typing import Literal

from pydantic import BaseModel

ValidOperation = Literal["encrypt", "decrypt"]
ValidLanguage = Literal["eng", "rus"]


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class Alphabet(BaseModel):
    eng_idx: tuple[str] = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    eng_letters: dict[str, int] = {letter: index for index, letter in enumerate(eng_idx)}

    rus_idx: tuple[str] = tuple("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
    rus_letters: dict[str, int] = {letter: index for index, letter in enumerate(rus_idx)}


class Settings(BaseModel):
    run: RunConfig = RunConfig()
    alphabet: Alphabet = Alphabet()


settings = Settings()
