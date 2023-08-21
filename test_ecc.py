from common_utils.conversion_utils import *
from common_utils.crypto_utils import *

g = get_generator_point()

g_2_add = add_points(g, g)
g_3_add = add_points(g_2_add, g)

g_3_mul = mul_point_number(g, 3)
print(g_3_add == g_3_mul)

inv_g = inv_point(g)
g_inv_add = add_points(g_2_add, inv_g)
print(g_inv_add == g)
# from common_utils.crypto_utils import encrypt
# from common_utils.conversion_utils import *
# plaintext = int_to_bytes(1, 16)
# ciphertext = encrypt(plaintext, int_to_bytes(0, 16), int_to_bytes(0, 16))
# print(bytes_to_hex(ciphertext))