from core import eng_letters, eng_idx, rus_letters, rus_idx


def encrypt(text: str, shift: int = 5) -> str:
    encoded_text = []
    for sym in text:
        if sym.upper() in eng_letters:
            new_char = eng_idx[(eng_letters.get(sym.upper()) + shift) % len(eng_idx)]
            encoded_text.append(new_char if sym.isupper() else new_char.lower())

        elif sym.upper() in rus_letters:
            new_char = rus_idx[(rus_letters.get(sym.upper()) + shift) % len(rus_idx)]
            encoded_text.append(new_char if sym.isupper() else new_char.lower())

        else:
            encoded_text.append(sym)

    return "".join(encoded_text)


def decrypt(encoded_text: str, shift: int = 5) -> str:
    return encrypt(text=encoded_text, shift=-shift)
