def encoding(text: str, shift: int = 5) -> str:
    encoded_text = []
    for sym in text:
        if "A" <= sym <= "Z":
            encoded_text.append(chr((ord(sym) + shift - ord("A")) % 26 + ord("A")))
        elif "a" <= sym <= "z":
            encoded_text.append(chr((ord(sym) + shift - ord("a")) % 26 + ord("a")))
        elif "А" <= sym <= "Я":
            encoded_text.append(chr((ord(sym) + shift - ord("А")) % 32 + ord("А")))
        elif "а" <= sym <= "я":
            encoded_text.append(chr((ord(sym) + shift - ord("а")) % 32 + ord("а")))
        else:
            encoded_text.append(sym)

    return "".join(encoded_text)


def decoding(encoded_text: str, shift: int = 5) -> str:
    return encoding(encoded_text, -shift)
