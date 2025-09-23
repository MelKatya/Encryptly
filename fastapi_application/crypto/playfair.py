from fastapi import HTTPException, status

from core import eng_letters, eng_idx, rus_letters, rus_idx

LANGUAGES = {
    "eng": {
        "letters": eng_letters,
        "idx": eng_idx,
        "exclude": "J",
        "exchange": "I",
        "aggregate": "X",
        "cols": 5,
    },
    "rus": {
        "letters": rus_letters,
        "idx": rus_idx,
        "exclude": "Ё",
        "exchange": "Е",
        "aggregate": "Ъ",
        "cols": 4,
    },
}


def check_lang(text: str, lang_letters: dict) -> None:
    """
    Проверяет, что все символы текста принадлежат указанному алфавиту.

    Args:
        text (str): Строка для проверки.
        lang_letters (dict): Словарь, содержащий допустимые символы.

    Raises:
        HTTPException: Если в тесте присутствуют символы, которых нет
            в выбранном алфавите.
    """
    bad = [sym for sym in text if sym not in lang_letters]

    if bad:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid characters "
            f"for the selected alphabet: {", ".join(bad)}",
        )


def playfair_square_build(
    keyword: str,
    vocabulary: str,
) -> list[list[str]]:
    """
    Строит квадрат Плейфера (матрицу букв) для шифрования и
    дешифрования текста.

    Args:
        keyword (str): Ключевое слово (будет приведено к верхнему регистру
            и адаптировано под выбранный алфавит).
        vocabulary (str): Ключ словаря LANGUAGES — указывает,
            какой алфавит использовать при построении.

    Returns:
        list[list[str]]: Двумерный список (матрица), содержащий буквы
            в порядке, необходимом для алгоритма Плейфера.

    Raises:
        HTTPException: Если в тесте присутствуют символы, которых нет
            в выбранном алфавите.
    """
    lang = LANGUAGES[vocabulary]

    keyword_upper = keyword.upper().replace(lang["exclude"], lang["exchange"])
    check_lang(text=keyword_upper, lang_letters=lang["letters"])

    key_list = []
    for letter in keyword_upper:
        if letter not in key_list:
            key_list.append(letter)

    language_list = [
        letter
        for letter in lang["idx"]
        if letter not in key_list and letter != lang["exclude"]
    ]

    key_list.extend(language_list)
    playfair_square = [
        key_list[idx : idx + lang["cols"]]
        for idx in range(0, len(key_list), lang["cols"])
    ]
    return playfair_square


def create_bigram(
    text: str,
    vocabulary: str,
) -> list[list[str]]:
    """
    Формирует биграммы (пары символов) из переданного текста
    по правилам алгоритма Плейфера.

    Args:
        text (str): Исходный текст для разбиения на биграммы.
            Перед обработкой приводится к верхнему регистру и
            убирает исключенные символы.
        vocabulary (str): Ключ словаря LANGUAGES — указывает,
            какой алфавит использовать при построении.

    Returns:
        list[list[str]]: Список биграмм (пар букв). Если встречаются
            две одинаковые буквы подряд — вторая заменяется заполняющим
            символом. Если в конце текста остаётся одиночная
            буква — к ней добавляется заполняющий символ.
    """
    lang = LANGUAGES[vocabulary]

    text_upper = text.upper().replace(lang["exclude"], lang["exchange"])
    temp_text = [sym for sym in text_upper if sym in lang["letters"]]
    bigram_list = []

    while True:
        if len(temp_text) == 1:
            bigram_list.append([temp_text[0], lang["aggregate"]])
            break
        elif len(temp_text) < 1:
            break

        if temp_text[0] != temp_text[1]:
            bigram_list.append(temp_text[0:2])
            temp_text = temp_text[2:]
        else:
            bigram_list.append([temp_text[0], lang["aggregate"]])
            temp_text = temp_text[1:]

    return bigram_list


def search_letter(
    dictionary: list[list[str]],
    first_letter: str,
    second_letter: str,
) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Ищет координаты двух букв в квадрате Плейфера.

    Args:
        dictionary (list[list[str]]): Квадрат Плейфера (двумерный список букв).
        first_letter (str): Первая буква из биграммы.
        second_letter (str): Вторая буква из биграммы.

    Returns:
        tuple[tuple[int, int], tuple[int, int]]: Кортеж из двух координат
            (строка, столбец) — сначала для первой буквы, затем для второй.

    Raises:
        HTTPException: Если хотя бы одна из букв не найдена в квадрате Плейфера.
    """
    first_place = None
    second_place = None

    for row, row_list in enumerate(dictionary):
        if first_letter in row_list:
            first_place = (row, row_list.index(first_letter))
        if second_letter in row_list:
            second_place = (row, row_list.index(second_letter))

    if first_place is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Symbol '{first_letter}' not found in Playfair square",
        )
    if second_place is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Symbol '{second_letter}' not found in Playfair square",
        )

    return first_place, second_place


def shift_letters(
    dictionary: list[list[str]],
    first: tuple[int, int],
    second: tuple[int, int],
    decrypted: bool = False,
) -> tuple[str, str]:
    """
    Выполняет сдвиг пары букв по правилам алгоритма Плейфера.

    Args:
        dictionary (list[list[str]]): Квадрат Плейфера (двумерный список букв).
        first (tuple[int, int]): Координаты первой буквы (строка, столбец).
        second (tuple[int, int]): Координаты второй буквы (строка, столбец).
        decrypted (bool): Режим обработки.
            False — шифрование (сдвиг вперед),
            True — расшифровка (сдвиг назад).

    Returns:
        tuple[str, str]: Новая пара букв, полученная после применения
            правил Плейфера.
    """
    if first[0] == second[0]:
        row = dictionary[first[0]]
        first_letter = row[(first[1] + 1 * (-1) ** decrypted) % len(row)]
        second_letter = row[(second[1] + 1 * (-1) ** decrypted) % len(row)]

    elif first[1] == second[1]:
        idx = first[1]
        first_letter = dictionary[(first[0] + 1 * (-1) ** decrypted) % len(dictionary)][
            idx
        ]
        second_letter = dictionary[
            (second[0] + 1 * (-1) ** decrypted) % len(dictionary)
        ][idx]

    else:
        first_letter = dictionary[first[0]][second[1]]
        second_letter = dictionary[second[0]][first[1]]

    return first_letter, second_letter


def encrypt(text: str, keyword: str, vocabulary: str) -> str:
    """
    Шифрует текст алгоритмом Плейфера.

    Args:
        text (str): Текст для шифрования.
        keyword (str): Ключевое слово.
        vocabulary (str): Ключ словаря LANGUAGES — указывает,
            какой алфавит использовать при построении.

    Returns:
        str: Зашифрованный текст.
    """
    dict_list = playfair_square_build(keyword=keyword, vocabulary=vocabulary)
    bigram_text = create_bigram(text=text, vocabulary=vocabulary)
    encoded_text = []

    for bigram in bigram_text:
        first, second = search_letter(
            dictionary=dict_list,
            first_letter=bigram[0],
            second_letter=bigram[1],
        )

        encoded_text.extend(
            shift_letters(
                dictionary=dict_list,
                first=first,
                second=second,
            )
        )

    return "".join(encoded_text)


def decrypt(encoded_text: str, keyword: str, vocabulary: str) -> str:
    """
    Расшифровывает текст, зашифрованный алгоритмом Плейфера

    Args:
        encoded_text (str): Зашифрованный текст.
        keyword (str): Ключевое слово.
        vocabulary (str): Ключ словаря LANGUAGES — указывает,
            какой алфавит использовать при построении.

    Returns:
        str: Расшифрованный текст.
    """
    lang = LANGUAGES[vocabulary]

    if len(encoded_text) % 2 != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Playfair ciphertext must have an even number of characters",
        )

    dict_list = playfair_square_build(keyword=keyword, vocabulary=vocabulary)
    text_upper = encoded_text.upper().replace(lang["exclude"], lang["exchange"])
    bigram_text = [
        [text_upper[idx], text_upper[idx + 1]] for idx in range(0, len(text_upper), 2)
    ]

    decoded_text = []

    for bigram in bigram_text:
        first, second = search_letter(
            dictionary=dict_list,
            first_letter=bigram[0],
            second_letter=bigram[1],
        )

        decoded_text.extend(
            shift_letters(
                dictionary=dict_list,
                first=first,
                second=second,
                decrypted=True,
            )
        )

    return "".join(decoded_text)
