# gtt_0: H(a_0) xor H(a_1) xor (lsb_b_0 * delta)
# gtt_1: H(b_0) xor H(b_1) xor a_0
# g_output: H(a_0) xor (lsb_a_0 * gtt_0) xor H(b_0) xor (lsb_b_0 * (H(b_0) xor H(b_1)))
# e_output: H(a_a) xor H(b_b) xor (lsb_a_a * gtt_0) xor (lsb_b_b * (a_a xor gtt_1))

def verify(a, b, lsb_a_0, lsb_b_0):
    lsb_a_1 = 1 - lsb_a_0
    lsb_b_1 = 1 - lsb_b_0
    gtt_0 = set()
    gtt_0 = gtt_0 ^ {'H_a_0'}
    gtt_0 = gtt_0 ^ {'H_a_1'}
    if lsb_b_0 == 1:
        gtt_0 = gtt_0 ^ {'delta'}
    gtt_1 = set()
    gtt_1 = gtt_1 ^ {'H_b_0'}
    gtt_1 = gtt_1 ^ {'H_b_1'}
    gtt_1 = gtt_1 ^ {'a_0'}
    g_output = set()
    g_output = g_output ^ {'H_a_0'}
    if lsb_a_0 == 1:
        g_output = g_output ^ gtt_0
    g_output = g_output ^ {'H_b_0'}
    if lsb_b_0 == 1:
        g_output = g_output ^ {'H_b_0'}
        g_output = g_output ^ {'H_b_1'}
    e_output = set()
    if a == 0:
        e_output = e_output ^ {'H_a_0'}
    else:
        e_output = e_output ^ {'H_a_1'}
    if b == 0:
        e_output = e_output ^ {'H_b_0'}
    else:
        e_output = e_output ^ {'H_b_1'}
    if a == 0 and lsb_a_0 == 1:
        e_output = e_output ^ gtt_0
    elif a == 1 and lsb_a_1 == 1:
        e_output = e_output ^ gtt_0
    if b == 0 and lsb_b_0 == 1:
        e_output = e_output ^ gtt_1
        if a == 0:
            e_output = e_output ^ {'a_0'}  
        else:
            e_output = e_output ^ {'a_1'}
    elif b == 1 and lsb_b_1 == 1:
        e_output = e_output ^ gtt_1
        if a == 0:
            e_output = e_output ^ {'a_0'}  
        else:
            e_output = e_output ^ {'a_1'}
    return g_output, e_output

print(verify(0, 0, 0, 0))
print(verify(0, 0, 0, 1))
print(verify(0, 0, 1, 0))
print(verify(0, 0, 1, 1))

print(verify(0, 1, 0, 0))
print(verify(0, 1, 0, 1))
print(verify(0, 1, 1, 0))
print(verify(0, 1, 1, 1))

print(verify(1, 0, 0, 0))
print(verify(1, 0, 0, 1))
print(verify(1, 0, 1, 0))
print(verify(1, 0, 1, 1))

print(verify(1, 1, 0, 0))
print(verify(1, 1, 0, 1))
print(verify(1, 1, 1, 0))
print(verify(1, 1, 1, 1))
