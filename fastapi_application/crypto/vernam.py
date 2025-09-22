import base64


def encrypt(text: str, keyword: str) -> str:
    text_bytes = text.encode()
    key_bytes = keyword.encode()
    encoded_text = [sym ^ key_bytes[idx_key % len(key_bytes)] for idx_key, sym in enumerate(text_bytes)]

    return base64.b64encode(bytes(encoded_text)).decode()


def decrypt(encoded_text: str, keyword: str) -> str:
    encoded_bytes = base64.b64decode(encoded_text)
    key_bytes = keyword.encode()
    decoded_text = [sym ^ key_bytes[idx_key % len(key_bytes)] for idx_key, sym in enumerate(encoded_bytes)]

    return bytes(decoded_text).decode()
