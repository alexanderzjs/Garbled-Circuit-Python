from typing import Union
from common_utils.conversion_utils import *
from common_utils.crypto_utils import add_points, inv_point, mul_point_number, get_generator_point, generate_random_int_with_range, get_encrypted_mask
from py_ecc.secp256k1 import secp256k1

def base_ot_sender_1(num_of_ot: int) -> Union[list, list]:
    a = list()
    A = list()
    for i in range(num_of_ot):
        current_a = generate_random_int_with_range(1, secp256k1.N)
        current_A = mul_point_number(get_generator_point(), current_a)
        a.append(current_a)
        A.append([current_A[0], current_A[1]])
    return a, A

def base_ot_receiver_1(num_of_ot: int, b: list, A_in: list) -> Union[list, list]:
    A = list_conversion(A_in, "int", "ec_point")
    c = list()
    C = list()
    for i in range(num_of_ot):
        current_c = generate_random_int_with_range(1, secp256k1.N)
        current_C = mul_point_number(get_generator_point(), current_c)
        if b[i] == 1:
            current_C = add_points(current_C, A[i])
        c.append(current_c)
        C.append([current_C[0], current_C[1]])
    return c, C

def base_got_sender_2(num_of_ot: int, m_0: list, m_1: list, a: list, A_in: list, C_in: list, message_len_in_bytes: int) -> Union[list, list]:
    A = list_conversion(A_in, "int", "ec_point")
    C = list_conversion(C_in, "int", "ec_point")
    e_0 = list()
    e_1 = list()
    for i in range(num_of_ot):
        temp_a_C = mul_point_number(C[i], a[i])
        mask_0 = get_encrypted_mask(temp_a_C, message_len_in_bytes)
        e_0.append(xor_bytes(m_0[i], mask_0, 16))
        temp_a_C_A = mul_point_number(add_points(C[i], inv_point(A[i])), a[i])
        mask_1 = get_encrypted_mask(temp_a_C_A, message_len_in_bytes)
        e_1.append(xor_bytes(m_1[i], mask_1, 16))
    return e_0, e_1

def base_got_receiver_2(num_of_ot: int, b: list, e_0: list, e_1: list, c: list, A_in: list, message_len_in_bytes: int) -> list:
    A = list_conversion(A_in, "int", "ec_point")
    m_b = list()
    for i in range(num_of_ot):
        temp_c_A = mul_point_number(A[i], c[i])
        mask_b = get_encrypted_mask(temp_c_A, message_len_in_bytes)
        if b[i] == 0:
            m_b.append(xor_bytes(e_0[i], mask_b, 16))
        else:
            m_b.append(xor_bytes(e_1[i], mask_b, 16))
    return m_b

