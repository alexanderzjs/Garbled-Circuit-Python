import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from py_ecc.secp256k1 import secp256k1
from py_ecc.typing import PlainPoint2D
from typing import cast
from common.conversion import *

def hash(input: bytes) -> bytes:
    digest = hashes.Hash(hashes.SHA256())
    digest.update(input)
    result = digest.finalize()
    return result

def encrypt(plaintext: bytes, password: bytes, counter: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(password[0 : 16]), modes.CTR(counter[0 : 16]))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext)
    ciphertext += encryptor.finalize()
    return ciphertext

def add_points(a: list, b: list) -> list:
    if len(a) != 2 or len(b) != 2:
        raise Exception("Points are invalid")
    A = cast("PlainPoint2D", (a[0], a[1]))
    B = cast("PlainPoint2D", (b[0], b[1]))
    C = secp256k1.add(A, B)
    return [C[0], C[1]]

def inv_point(a: list) -> list:
    if len(a) != 2:
        raise Exception("Point is invalid")
    inv_a = cast("PlainPoint2D", (a[0], secp256k1.P - a[1]))
    return [inv_a[0], inv_a[1]]

def mul_point_number(a: list, b: int) -> list:
    if len(a) != 2:
        raise Exception("Point is invalid")
    A = cast("PlainPoint2D", (a[0], a[1]))
    C = secp256k1.multiply(A, b)
    return [C[0], C[1]]

def get_generator_point() -> list:
    return [secp256k1.G[0], secp256k1.G[1]]

def get_encrypted_mask(password: list, byte_len: int) -> bytes:
    if byte_len % 16 != 0:
        raise Exception("Byte length error: " + str(byte_len))
    plaintext = int_to_bytes(0, byte_len)
    x = int_to_bytes(password[0], 32)
    y = int_to_bytes(password[1], 32)
    key = hash(xor_bytes(x, y, 32))[0 : 16]
    keyHex = bytes_to_hex(key)
    return encrypt(plaintext, key, b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

def get_random_blocks(counter: int, password: bytes, num_of_blocks: int) -> list:
    plaintext = bytes()
    for i in range(num_of_blocks):
        plaintext += int_to_bytes(counter + i, 16)
    blocks = encrypt(plaintext, password, b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    result = list()
    for i in range(num_of_blocks):
        result.append(blocks[i * 16 : i * 16 + 16])
    return result

def generate_random_int_with_range(lower_bound: int, upper_bound: int) -> int:
    if lower_bound <= 0 or upper_bound < lower_bound:
        raise Exception("Cannot generate random number with given range: [" + str(lower_bound) + "," + str(upper_bound) + ")")
    bit_len = len(bin(upper_bound)) - 2
    if bit_len % 8 != 0:
        raise Exception("Bit length illegal: " + str(bit_len))
    len_in_bytes = bit_len // 8
    random_int = bytes_to_int(os.urandom(len_in_bytes))
    while random_int >= upper_bound:
        random_int = bytes_to_int(os.urandom(len_in_bytes))
    return random_int
