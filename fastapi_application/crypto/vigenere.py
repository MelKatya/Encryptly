from fastapi import HTTPException, status

from core import eng_letters, eng_idx, rus_letters, rus_idx


def keyword_to_figure(keyword: str) -> list[int]:
    shift_list = []
    for sym in keyword:
        if sym.upper() in eng_letters:
            shift_list.append(eng_letters.get(sym.upper()))
        elif sym.upper() in rus_letters:
            shift_list.append(rus_letters.get(sym.upper()))
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="В ключевом слове могут быть только английские и русские буквы",
            )
    return shift_list


def encrypt(text: str, keyword: str, decrypt: bool = False) -> str:
    encoded_text = []
    shift_list = keyword_to_figure(keyword)
    key_index = 0
    for sym in text:
        if sym.upper() in eng_letters:
            shift = shift_list[key_index % len(shift_list)]

            if decrypt:
                shift = -shift

            new_char = eng_idx[(eng_letters.get(sym.upper()) + shift) % len(eng_idx)]
            encoded_text.append(new_char if sym.isupper() else new_char.lower())
            key_index += 1

        elif sym.upper() in rus_letters:
            shift = shift_list[key_index % len(shift_list)]
            if decrypt:
                shift = -shift

            new_char = rus_idx[(rus_letters.get(sym.upper()) + shift) % len(rus_idx)]
            encoded_text.append(new_char if sym.isupper() else new_char.lower())
            key_index += 1

        else:
            encoded_text.append(sym)

    return "".join(encoded_text)


def decrypt(encoded_text: str, keyword: str) -> str:
    return encrypt(encoded_text, keyword, decrypt=True)
