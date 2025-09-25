from core import eng_letters, eng_idx, rus_letters, rus_idx
import os
import base64

text = "мама мыла раму, раму мыла мама, мама мыла раму"
text = text.encode()

my_blocks = []

for idx in range(0, len(text), 8):
    block = text[idx:idx + 8]
    if len(block) == 8:
        block_to_int = int.from_bytes(block)
        my_blocks.append(format(block_to_int, '064b'))
    else:
        rest = 8 - len(block)
        block += bytes([rest]) * rest
        block_to_int = int.from_bytes(block)
        my_blocks.append(format(block_to_int, '064b'))

print(my_blocks)

key = int.from_bytes(os.urandom(7))
key_to_bit = format(key, '056b')



