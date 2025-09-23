from core import eng_letters, eng_idx, rus_letters, rus_idx


def crypt(text: str) -> str:
    """
    Шифрует и расшифровывает текст алгоритмом Атбаш (обратный алфавит).

    Args:
        text (str): Текст для шифрования/расшифрования.
            Поддерживаются латиница и кириллица.

    Returns:
        str: Зашифрованный или расшифрованный текст. Регистр букв сохраняется.
    """
    encoded_text = []
    for sym in text:
        if sym.upper() in eng_letters:
            new_char = eng_idx[len(eng_idx) - eng_letters[sym.upper()] - 1]
            encoded_text.append(new_char if sym.isupper() else new_char.lower())
        elif sym.upper() in rus_letters:
            new_char = rus_idx[len(rus_idx) - rus_letters[sym.upper()] - 1]
            encoded_text.append(new_char if sym.isupper() else new_char.lower())
        else:
            encoded_text.append(sym)

    return "".join(encoded_text)
