from core import eng_letters, eng_idx, rus_letters, rus_idx


def encrypt(text: str, shift: int = 5) -> str:
    """
    Шифрует текст алгоритмом Цезаря.

    Args:
        text (str): Текст для шифрования. Поддерживаются латиница и кириллица.
        shift (int): Сдвиг букв в алфавите. По умолчанию 5.

    Returns:
        str: Зашифрованный текст. Регистр букв сохраняется.
    """
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
    """
    Расшифровывает текст, зашифрованный алгоритмом Цезаря

    Args:
        encoded_text (str): Текст для расшифрования. Поддерживаются латиница и кириллица.
        shift (int): Сдвиг букв в алфавите. По умолчанию 5.

    Returns:
        str: Расшифрованный текст. Регистр букв сохраняется.
    """
    return encrypt(text=encoded_text, shift=-shift)
