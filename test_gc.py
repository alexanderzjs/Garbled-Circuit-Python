from oblivious_transfer.base_ot import *
from common.conversion import *
from garbled_circuit.garbler import *
from garbled_circuit.evaluator import *

circuit_file = "./aes.txt"

# Garbler's operation
delta, public_one_label, public_one_label_delta = garbler_init()
num_of_ginput = 256
num_of_einput = 128
num_of_output = 128
ginput = [1,1,1,1,0,1,1,0,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,1,1,1,1,1,1,1,0,0,1,1,0,1,0,1,1,0,1,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1,0,0,0,1,1,1,1,0,0,1,0,1,1,1,0,0,0,0,1,1,1,1,0,0,1,0,1,1,1,0,0,0,1,1,1,0,0,1,1,1,1,1,0,1,1,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,1,0,0,1,0,0, 0,1,1,0,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,0,0,0,0,1,1,0,1,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,0,0,1,0,1,1,0,0,1,1,0,0,1,1,0,0,0,1,1,0,1,1,0,0,1,0,0,0,0,1,1,0,1,1,0,0,1,1,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,1,1,0,1,1,1,0,0,1,1,1,0,0,0,0,0,1,1,0,0,1,0,0,0,1,1,0,0,1,1]
gginput_0, gginput_1, geinput_0, geinput_1 = generate_garbled_input(num_of_ginput, num_of_einput, delta)
g_output, gtt = compute_garbled_circuit(circuit_file, ginput, gginput_0, gginput_1, geinput_0, public_one_label_delta, delta)

# Evaluator Operation
einput = [1,1,0,1,0,0,1,1,1,0,0,0,1,0,0,0,1,0,1,0,0,1,1,0,1,1,0,0,0,1,1,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,0,1,0,0,0,0,1,1,0,1,0,0,0,1,0,1,1,0,1,1,0,0,0,0,0,0,1,0,0,1,0,1,0,1,0,1,1,0,1,0,0,0,1,1,0,0,1,1,0,0,0,1,1,0,1,0,0,0,1,1,1,1,1,1,1,1,1]
new_geinput = list()
# OT operation
message_len_in_bytes = 16
a, A = base_ot_sender_1(num_of_einput)
c, C = base_ot_receiver_1(num_of_einput, einput, A)
e_0, e_1 = base_got_sender_2(num_of_einput, geinput_0, geinput_1, a, A, C, message_len_in_bytes)
new_geinput = base_got_receiver_2(num_of_einput, einput, e_0, e_1, c, A, message_len_in_bytes)

e_output = evaluate_garbled_circuit(circuit_file, gginput_0, new_geinput, public_one_label, gtt)

for i in range(num_of_output):
    if g_output[i] != e_output[i]:
        print(1, end="")
    else:
        print(0, end="")

# aes expected output is 01011100111101001000101011111011111011101010000011111011110011001101111101111011100001010111000110110110000000000110000111101000