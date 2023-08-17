from typing import Union
from common_utils.crypto_utils import get_random_blocks, and_bytes, or_bytes, xor_bytes, hash
from gc_utils.circuit import load_circuit_from_file
import os

def garbler_init() -> Union[bytes, bytes, bytes, bytes]:
    fix_key = os.urandom(16)
    delta = or_bytes(os.urandom(16), b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01', 16)
    public_one_label = os.urandom(16)
    public_one_label_delta = xor_bytes(public_one_label, delta, 16)
    return fix_key, delta, public_one_label, public_one_label_delta

def generate_garbled_input(ginput_bit_length: int, einput_bit_length: int, delta: bytes) -> Union[list, list]:
    gginput_0 = get_random_blocks(0, os.urandom(16), ginput_bit_length)
    gginput_1 = list()
    for i in range(ginput_bit_length):
        gginput_1.append(xor_bytes(gginput_0[i], delta, 16))
    geinput_0 = get_random_blocks(0, os.urandom(16), einput_bit_length)
    geinput_1 = list()
    for i in range(einput_bit_length):
        geinput_1.append(xor_bytes(geinput_0[i], delta, 16))
    return gginput_0, gginput_1, geinput_0, geinput_1

def garble_and_gate(input_a: bytes, input_b: bytes, delta: bytes, and_gate_id: int, fix_key: bytes) -> Union[bytes, bytes, bytes]:
    a_0 = input_a
    a_1 = xor_bytes(input_a, delta, 16)
    b_0 = input_b
    b_1 = xor_bytes(input_b, delta, 16)
    lsb_a_0 = and_bytes(a_0, b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01', 16)[15]
    lsb_b_0 = and_bytes(b_0, b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01', 16)[15]
    hashed_a_0 = hash(a_0)[0 : 16]
    hashed_a_1 = hash(a_1)[0 : 16]
    hashed_b_0 = hash(b_0)[0 : 16]
    hashed_b_1 = hash(b_1)[0 : 16]
    gtt_0 = xor_bytes(hashed_a_0, hashed_a_1, 16)
    if lsb_b_0 == 1:
        gtt_0 = xor_bytes(gtt_0, delta, 16)
    output = hashed_a_0
    if lsb_a_0 == 1:
        output = xor_bytes(output, gtt_0, 16)
    temp = xor_bytes(hashed_b_0, hashed_b_1, 16)
    gtt_1 = xor_bytes(temp, a_0, 16)
    output = xor_bytes(output, hashed_b_0, 16)
    if lsb_b_0 == 1:
        output = xor_bytes(output, temp, 16)
    return output, gtt_0, gtt_1

def garble_or_gate(input_a: bytes, input_b: bytes, delta: bytes, and_gate_id: int, fix_key: bytes) -> Union[bytes, bytes, bytes]:
    and_output, gtt_0, gtt_1 = garble_and_gate(input_a, input_b, delta, and_gate_id, fix_key)
    or_output = xor_bytes(and_output, xor_bytes(input_a, input_b, 16), 16)
    return or_output, gtt_0, gtt_1

def garble_xor_gate(input_a: bytes, input_b: bytes) -> bytes: 
    return xor_bytes(input_a, input_b, 16)

def garble_not_gate(public_label: bytes, input: bytes) -> bytes: 
    return xor_bytes(public_label, input, 16)

def compute_garbled_circuit(circuit_file: str, ginput: list, gginput_0: list, gginput_1: list, geinput_0: list, public_one_label_delta: bytes, delta: bytes, fix_key: bytes) -> Union[list, list]:
    gates, num_of_gate, num_of_wire, num_of_ginput, num_of_einput, num_of_output = load_circuit_from_file(circuit_file)
    wires = list()
    for i in range(num_of_wire):
        wires.append(bytes())
    for i in range(num_of_ginput):
        if ginput[i] == 0:
            wires[i] = gginput_0[i]
        else:
            wires[i] = gginput_1[i]
    for i in range(num_of_einput):
        wires[i + num_of_ginput] = geinput_0[i]
    and_gate_id = 0
    gtt = list()
    for i in range(num_of_gate):
        if gates[4 * i + 3] == 0:
            wires[gates[4 * i + 2]], gtt_0, gtt_1 = garble_and_gate(wires[gates[4 * i]], wires[gates[4 * i + 1]], delta, and_gate_id, fix_key)
            gtt.append(gtt_0)
            gtt.append(gtt_1)
            and_gate_id += 1
        elif gates[4 * i + 3] == 3:
            wires[gates[4 * i + 2]], gtt_0, gtt_1 = garble_or_gate(wires[gates[4 * i]], wires[gates[4 * i + 1]], delta, and_gate_id, fix_key)
            gtt.append(gtt_0)
            gtt.append(gtt_1)
            and_gate_id += 1
        elif gates[4 * i + 3] == 1:
            wires[gates[4 * i + 2]] = garble_xor_gate(wires[gates[4 * i]], wires[gates[4 * i + 1]])
        elif gates[4 * i + 3] == 2:
            wires[gates[4 * i + 2]] = garble_not_gate(public_one_label_delta, wires[gates[4 * i]])
    output = list()
    for i in range(num_of_wire - num_of_output, num_of_wire):
        output.append(wires[i])
    return output, gtt
