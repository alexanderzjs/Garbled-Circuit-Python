from common.conversion import *
from oblivious_transfer.base_ot import *

num_of_ot = 8
m_0 = [b"fo150jlafjgrj1rqr48"] * num_of_ot
m_1 = [b"amvjjafljga845gad1p"] * num_of_ot
message_len_in_bytes = len(m_0[0])
b = [0, 1, 1, 0] * (num_of_ot // 4)

a, A = base_ot_sender_1(num_of_ot)
c, C = base_ot_receiver_1(num_of_ot, b, A)
e_0, e_1 = base_got_sender_2(num_of_ot, m_0, m_1, a, A, C, message_len_in_bytes)
m_b = base_got_receiver_2(num_of_ot, b, e_0, e_1, c, A, message_len_in_bytes)
print(m_b)