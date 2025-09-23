from fastapi import HTTPException, status

from core import eng_letters, eng_idx, rus_letters, rus_idx


def keyword_to_figure(keyword: str) -> list[int]:
    """
    Преобразует ключевое слово в список индексов букв для сдвига.

    Args:
        keyword (str): Ключевое слово для преобразования.
            Допускаются только латинские и кириллические буквы.

    Returns:
        list[int]: Список числовых сдвигов, соответствующих индексам букв
        в английском или русском алфавите.

    Raises:
        HTTPException: Если ключевое слово содержит символы,
            не относящиеся к английскому или русскому алфавиту.
    """
    shift_list = []
    for sym in keyword:
        if sym.upper() in eng_letters:
            shift_list.append(eng_letters.get(sym.upper()))
        elif sym.upper() in rus_letters:
            shift_list.append(rus_letters.get(sym.upper()))
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The keyword can only contain English and Russian letters.",
            )
    return shift_list


def encrypt(text: str, keyword: str, decrypted: bool = False) -> str:
    """
    Шифрует или расшифровывает текст алгоритмом Виженера.

    Args:
        text (str): Текст для обработки. Поддерживаются
            латиница и кириллица; остальные символы остаются без изменений.
        keyword (str): Ключевое слово для генерации сдвигов.
        decrypted (bool): Режим работы. False — шифрование (по умолчанию),
            True — расшифровка (сдвиги в обратную сторону).

    Returns:
        str: Зашифрованный или расшифрованный текст. Регистр букв сохраняется.
    """
    encoded_text = []
    shift_list = keyword_to_figure(keyword)
    key_index = 0
    for sym in text:
        if sym.upper() in eng_letters:
            shift = shift_list[key_index % len(shift_list)]

            if decrypted:
                shift = -shift

            new_char = eng_idx[(eng_letters.get(sym.upper()) + shift) % len(eng_idx)]
            encoded_text.append(new_char if sym.isupper() else new_char.lower())
            key_index += 1

        elif sym.upper() in rus_letters:
            shift = shift_list[key_index % len(shift_list)]

            if decrypted:
                shift = -shift

            new_char = rus_idx[(rus_letters.get(sym.upper()) + shift) % len(rus_idx)]
            encoded_text.append(new_char if sym.isupper() else new_char.lower())
            key_index += 1

        else:
            encoded_text.append(sym)

    return "".join(encoded_text)


def decrypt(encoded_text: str, keyword: str) -> str:
    """
    Расшифровывает текст алгоритмом Виженера.

    Args:
        encoded_text (str): Зашифрованный текст. Поддерживаются латиница и
            кириллица; остальные символы остаются без изменений.
        keyword (str): Ключевое слово для генерации сдвигов.

    Returns:
        str: Расшифрованный текст. Регистр букв сохраняется.
    """
    return encrypt(encoded_text, keyword, decrypted=True)
