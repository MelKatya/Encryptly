def encrypt(text: str, shift: int = 5) -> str:
    encoded_text = []
    for sym in text:
        if ("A" <= sym <= "Z") or ("a" <= sym <= "z"):
            new_char = chr((ord(sym.upper()) + shift - ord("A")) % 26 + ord("A"))
            encoded_text.append(new_char if sym.isupper() else new_char.lower())
        elif ("А" <= sym <= "Я") or ("а" <= sym <= "я"):
            new_char = chr((ord(sym.upper()) + shift - ord("А")) % 32 + ord("А"))
            encoded_text.append(new_char if sym.isupper() else new_char.lower())
        else:
            encoded_text.append(sym)

    return "".join(encoded_text)


def decrypt(encoded_text: str, shift: int = 5) -> str:
    return encrypt(encoded_text, -shift)
