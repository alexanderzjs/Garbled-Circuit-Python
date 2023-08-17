from common_utils.crypto_utils import and_bytes, xor_bytes, hash
from gc_utils.circuit import load_circuit_from_file

def evaluate_and_gate(wire_a: bytes, wire_b: bytes, delta: bytes, gtt_0: bytes, gtt_1: bytes, and_gate_id: int, fix_key: bytes) -> bytes:
    lsb_a = and_bytes(wire_a, b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01', 16)[15]
    lsb_b = and_bytes(wire_b, b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01', 16)[15]
    hashed_a = hash(wire_a)[0 : 16]
    hashed_b = hash(wire_b)[0 : 16]
    output = xor_bytes(hashed_a, hashed_b, 16)
    if lsb_a == 1:
        output = xor_bytes(output, gtt_0, 16)
    if lsb_b == 1:
        output = xor_bytes(xor_bytes(output, gtt_1, 16), wire_a, 16)
    return output

def evaluate_or_gate(input_a: bytes, input_b: bytes, delta: bytes, gtt_0: bytes, gtt_1: bytes, and_gate_id: int, fix_key: bytes) -> bytes:
    and_output = evaluate_and_gate(input_a, input_b, delta, gtt_0, gtt_1, and_gate_id, fix_key)
    or_output = xor_bytes(and_output, xor_bytes(input_a, input_b, 16), 16)
    return or_output

def evaluate_xor_gate(input_a: bytes, input_b: bytes) -> bytes: 
    return xor_bytes(input_a, input_b, 16)

def evaluate_not_gate(input: bytes, public_label: bytes) -> bytes: 
    return xor_bytes(input, public_label, 16)

def evaluate_garbled_circuit(circuit_file: str, gginput: list, geinput: list, public_one_label: bytes, delta: bytes, gtt: list, fix_key: bytes) -> list:
    gates, num_of_gate, num_of_wire, num_of_ginput, num_of_einput, num_of_output = load_circuit_from_file(circuit_file)
    wires = list()
    for i in range(num_of_wire):
        wires.append(bytes())
    for i in range(num_of_ginput):
        wires[i] = gginput[i]
    for i in range(num_of_einput):
        wires[i + num_of_ginput] = geinput[i]
    and_gate_id = 0
    for i in range(num_of_gate):
        if gates[4 * i + 3] == 0:
            wires[gates[4 * i + 2]] = evaluate_and_gate(wires[gates[4 * i]], wires[gates[4 * i + 1]], delta, gtt[2 * and_gate_id], gtt[2 * and_gate_id + 1], and_gate_id, fix_key)
            and_gate_id += 1
        elif gates[4 * i + 3] == 3:
            wires[gates[4 * i + 2]] = evaluate_or_gate(wires[gates[4 * i]], wires[gates[4 * i + 1]], delta, gtt[2 * and_gate_id], gtt[2 * and_gate_id + 1], and_gate_id, fix_key)
            and_gate_id += 1
        elif gates[4 * i + 3] == 1:
            wires[gates[4 * i + 2]] = evaluate_xor_gate(wires[gates[4 * i]], wires[gates[4 * i + 1]])
        elif gates[4 * i + 3] == 2:
            wires[gates[4 * i + 2]] = evaluate_not_gate(wires[gates[4 * i]], public_one_label)
    output = list()
    for i in range(num_of_wire - num_of_output, num_of_wire):
        output.append(wires[i])
    return output