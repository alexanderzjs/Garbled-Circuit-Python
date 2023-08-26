from typing import cast
from py_ecc.typing import PlainPoint3D
from py_ecc.secp256k1 import secp256k1

def int_to_bytes(input: int, byte_len: int) -> bytes:
    bit_len = len(bin(input)) - 2
    if byte_len * 8 >= bit_len:
        return int.to_bytes(input, byte_len)
    else:
        binary_str = bin(input)[-(byte_len * 8):]
        result = bytes()
        for i in range(byte_len):
            result += int.to_bytes(int(binary_str[i * 8 : i * 8 + 8], 2))
        return result

def bytes_to_int(input: bytes) -> int:
    return int.from_bytes(input)

def int_to_hex(input: int, hex_len: int) -> str:
    hex_input = hex(input)[2:]
    if len(hex_input) < hex_len:
        padding_length = hex_len - len(hex_input)
        hex_input = ('0' * padding_length) + hex_input
    return hex_input

def hex_to_int(input: str) -> int:
    return int(input, 16)

def int_to_unicode(input: int) -> str:
    return str(input)

def unicode_to_int(input: str) -> int:
    return int(input)

def bytes_to_hex(input: bytes) -> str:
    return input.hex()

def hex_to_bytes(input: str) -> bytes:
    return bytes.fromhex(input)

def bytes_to_unicode(input: bytes) -> str:
    return input.decode("utf-8")

def unicode_to_bytes(input: str) -> bytes:
    return bytes(input, encoding="utf-8")

def hex_to_unicode(input: str) -> str:
    return bytes_to_unicode(hex_to_bytes(input))

def unicode_to_hex(input: str) -> str:
    return bytes_to_hex(unicode_to_bytes(input))

def and_bytes(a: bytes, b: bytes, byte_len: int) -> bytes:
    return int_to_bytes(bytes_to_int(a) & bytes_to_int(b), byte_len)

def or_bytes(a: bytes, b: bytes, byte_len: int) -> bytes:
    return int_to_bytes(bytes_to_int(a) | bytes_to_int(b), byte_len)

def xor_bytes(a: bytes, b: bytes, byte_len: int) -> bytes:
    return int_to_bytes(bytes_to_int(a) ^ bytes_to_int(b), byte_len)

def list_conversion(input: list, from_type: any, to_type: any) -> list:
    output = list()
    for item in input:
        if from_type == "unicode" and to_type == "hex":
            output.append(unicode_to_hex(item))
        elif from_type == "hex" and to_type == "unicode":
            output.append(hex_to_unicode(item))
        elif from_type == "bytes" and to_type == "unicode":
            output.append(bytes_to_unicode(item))
        elif from_type == "unicode" and to_type == "bytes":
            output.append(unicode_to_bytes(item))
        elif from_type == "hex" and to_type == "bytes":
            output.append(hex_to_bytes(item))
        elif from_type == "bytes" and to_type == "hex":
            output.append(bytes_to_hex(item))
        elif from_type == "hex" and to_type == "int":
            output.append(hex_to_int(item))
        elif from_type == "unicode" and to_type == "int":
            output.append(unicode_to_int(item))
        elif from_type == "bytes" and to_type == "int":
            output.append(bytes_to_int(item))
        elif from_type == "hex" and to_type == "point2d":
            point = cast("PlainPoint3D", (hex_to_int(item[0]), hex_to_int(item[1]), hex_to_int(item[2])))
            output.append(secp256k1.from_jacobian(point))
        elif from_type == "int" and to_type == "point2d":
            point = cast("PlainPoint3D", (item[0], item[1], item[2]))
            output.append(secp256k1.from_jacobian(point))
        elif from_type == "hex" and to_type == "point3d":
            point = cast("PlainPoint3D", (hex_to_int(item[0]), hex_to_int(item[1]), hex_to_int(item[2])))
            output.append(point)
        elif from_type == "int" and to_type == "point3d":
            point = cast("PlainPoint3D", (item[0], item[1], item[2]))
            output.append(point)
        elif from_type == "point2d" and to_type == "int":
            point = secp256k1.to_jacobian(item)
            output.append([point[0], point[1], point[2]])
        elif from_type == "point2d" and to_type == "hex":
            point = secp256k1.to_jacobian(item)
            output.append([int_to_hex(point[0], -1), int_to_hex(point[1], -1), int_to_hex(point[2], -1)])
        elif from_type == "point3d" and to_type == "int":
            output.append([item[0], item[1], item[2]])
        elif from_type == "point3d" and to_type == "hex":
            output.append([int_to_hex(item[0], -1), int_to_hex(item[1], -1), int_to_hex(item[2], -1)])
        else:
            raise Exception("Type not supported in list_conversion")
    return output

