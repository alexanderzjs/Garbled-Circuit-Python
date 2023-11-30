from common.conversion import *
from common.crypto import *


g = get_generator_point()

g_2_add = add_points(g, g)
g_3_add = add_points(g_2_add, g)

g_3_mul = mul_point_number(g, 3)
print(g_3_add == g_3_mul)

inv_g = inv_point(g)
g_inv_add = add_points(g_2_add, inv_g)
print(g_inv_add == g)
