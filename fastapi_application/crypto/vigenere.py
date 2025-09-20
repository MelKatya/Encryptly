from core import eng_letters, eng_idx, rus_letters, rus_idx


def encrypt(text: str, keyword: str, decrypt: bool = False) -> str:
    encoded_text = []
    key_index = 0
    for sym in text:
        if sym.upper() in eng_letters:
            shift = eng_letters.get(keyword[key_index % len(keyword)].upper())

            if decrypt:
                shift = -shift

            new_char = eng_idx[(eng_letters.get(sym.upper()) + shift) % len(eng_idx)]
            encoded_text.append(new_char if sym.isupper() else new_char.lower())
            key_index += 1

        elif sym.upper() in rus_letters:
            shift = eng_letters.get(keyword[key_index % len(keyword)].upper())

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
