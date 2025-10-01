from core import eng_letters, eng_idx, rus_letters, rus_idx
import os
import base64

TABLES = {
    "IP": [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17,  9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ],
    "IP_1": [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25,
    ],
    "SHIFTS_KEY": [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1],
    "PC1": [
        57,49,41,33,25,17,9,
        1,58,50,42,34,26,18,
        10,2,59,51,43,35,27,
        19,11,3,60,52,44,36,
        63,55,47,39,31,23,15,
        7,62,54,46,38,30,22,
        14,6,61,53,45,37,29,
        21,13,5,28,20,12,4
    ],
    "PC2": [
        14,17,11,24, 1, 5,
        3,28,15, 6,21,10,
        23,19,12, 4,26, 8,
        16, 7,27,20,13, 2,
        41,52,31,37,47,55,
        30,40,51,45,33,48,
        44,49,39,56,34,53,
        46,42,50,36,29,32
    ],
    "P": [
        16, 7, 20, 21,
        29, 12, 28, 17,
        1, 15, 23, 26,
        5, 18, 31, 10,
        2, 8, 24, 14,
        32, 27, 3, 9,
        19, 13, 30, 6,
        22, 11, 4, 25,
    ],
    "E": [
        32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1,
    ],
    "S": {
        1: [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
        ],
        2: [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
        ],
        3: [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
        ],
        4: [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
        ],
        5: [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
        ],
        6: [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
        ],
        7: [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
        ],
        8: [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
        ],
    }
}




def create_key() -> list[int]:
    # create key 64 bit
    key = int.from_bytes(os.urandom(7), 'big')
    key_to_bit = format(key, '056b') + format(0, '08b')
    return [int(bit) for bit in key_to_bit]


def text_to_bit_blocks(text: str) -> list[list[int]]:
    encoded_text = text.encode()
    bit_blocks = []

    for idx in range(0, len(encoded_text), 8):
        block = encoded_text[idx:idx + 8]
        if len(block) == 8:
            block_to_int = int.from_bytes(block)
            bit_blocks.append([int(block) for block in format(block_to_int, '064b')])
        else:
            rest = 8 - len(block)
            block += bytes([rest]) * rest
            block_to_int = int.from_bytes(block)
            bit_blocks.append([int(block) for block in format(block_to_int, '064b')])

    return bit_blocks


def get_key_round(c0: list[int], d0: list[int], shift: int) -> list[int]:
    c1 = c0[shift:] + c0[:shift]
    d1 = d0[shift:] + d0[:shift]
    new_key = c1 + d1
    # ready key for xor right part
    return [new_key[pos - 1] for pos in TABLES["PC2"]]


def f_func(R_i_last: list[int], key_i: list[int]) -> list[int]:
    R_by_e = [R_i_last[pos - 1] for pos in TABLES["E"]]
    f_i = [r ^ k for r, k in zip(R_by_e, key_i)]

    sbox_input = [f_i[i:i + 6] for i in range(0, 48, 6)]
    sbox_output = []
    for idx, bits in enumerate(sbox_input):
        row = int(str(bits[0]) + str(bits[5]), 2)
        col = int("".join(map(str, bits[1:5])), 2)
        val = TABLES["S"][idx + 1][row][col]
        sbox_output.extend([int(bit) for bit in format(val, '04b')])

    return [sbox_output[pos - 1] for pos in TABLES["P"]]


def get_blocks_round(first_shift, key_i):
    new_blocks = []
    for block in first_shift:
        L_i_last = block[:32]
        R_i_last = block[32:]

        fi_by_P = f_func(R_i_last=R_i_last, key_i=key_i)

        L_i = R_i_last
        R_i = [r ^ k for r, k in zip(L_i_last, fi_by_P)]
        new_blocks.append(L_i + R_i)

    return new_blocks


def last_shift(encrypted_blocks: list[list[int]]) -> list[str]:
    encrypted_blocks_final = []
    for block in encrypted_blocks:
        revert_block = block[32:] + block[:32]
        block_to_ip_1 = [revert_block[pos - 1] for pos in TABLES["IP_1"]]

        block_int = int("".join(map(str, block_to_ip_1)), 2)
        block_hex = f"{block_int:016x}"

        encrypted_blocks_final.append(block_hex)

    return encrypted_blocks_final


def encrypt(text: str, key: list[int]):
    bit_blocks = text_to_bit_blocks(text=text)

    first_shift = [[block[pos - 1] for pos in TABLES["IP"]] for block in bit_blocks]

    key_to_pc1 = [int(key[pos - 1]) for pos in TABLES["PC1"]]
    c0 = key_to_pc1[:28]
    d0 = key_to_pc1[28:]

    shift = 0
    encrypted_blocks = first_shift
    for round in range(16):
        shift += TABLES["SHIFTS_KEY"][round]
        key_i = get_key_round(c0=c0, d0=d0, shift=shift)

        encrypted_blocks = get_blocks_round(encrypted_blocks,key_i)

    encrypted_blocks_final = last_shift(encrypted_blocks=encrypted_blocks)

    return "".join(encrypted_blocks_final)





text = "мама мыла раму, раму мыла мама, мама мыла раму"

key = create_key()

encrypt(text, key)
