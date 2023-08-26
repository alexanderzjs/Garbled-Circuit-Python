from flask import Flask, request, make_response
import json
from common.conversion import hex_to_bytes, list_conversion, bytes_to_hex
from garbled_circuit.evaluator import evaluate_garbled_circuit
from garbled_circuit.garbler import compute_garbled_circuit, garbler_init, generate_garbled_input
from oblivious_transfer.base_ot import base_got_sender_2, base_ot_receiver_1, base_got_receiver_2, base_ot_sender_1

app = Flask(__name__)

@app.route("/evaluator/first", methods=["POST"])
def evaluator_first():
    num_of_einput = 128
    einput = [1,1,0,1,0,0,1,1,1,0,0,0,1,0,0,0,1,0,1,0,0,1,1,0,1,1,0,0,0,1,1,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,0,1,0,0,0,0,1,1,0,1,0,0,0,1,0,1,1,0,1,1,0,0,0,0,0,0,1,0,0,1,0,1,0,1,0,1,1,0,1,0,0,0,1,1,0,0,1,1,0,0,0,1,1,0,1,0,0,0,1,1,1,1,1,1,1,1,1]
    A = list_conversion(request.json['A'], "hex", "point2d")
    c, C = base_ot_receiver_1(num_of_einput, einput, A)
    with open('./c.txt', 'w') as f:
        for i in range(len(c)):
            f.write(str(c[i]) + "\n")
    C_list = list_conversion(C, "point2d", "hex")
    return make_response({"C": C_list})

@app.route("/evaluator/second", methods=["POST"])
def evaluator_second():
    circuit_file = './aes.txt'
    num_of_einput = 128
    message_len_in_bytes = 16
    einput = [1,1,0,1,0,0,1,1,1,0,0,0,1,0,0,0,1,0,1,0,0,1,1,0,1,1,0,0,0,1,1,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,0,1,0,0,0,0,1,1,0,1,0,0,0,1,0,1,1,0,1,1,0,0,0,0,0,0,1,0,0,1,0,1,0,1,0,1,1,0,1,0,0,0,1,1,0,0,1,1,0,0,0,1,1,0,1,0,0,0,1,1,1,1,1,1,1,1,1]
    c = list()
    with open("./c.txt", 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            c.append(int(lines[i]))
    e_0 = list_conversion(request.json["e_0"], "hex", "bytes")
    e_1 = list_conversion(request.json["e_1"], "hex", "bytes")
    A = list_conversion(request.json["A"], "hex", "point2d")
    geinput = base_got_receiver_2(num_of_einput, einput, e_0, e_1, c, A, message_len_in_bytes)
    gginput_0 = list_conversion(request.json["gginput_0"], "hex", "bytes")
    public_one_label = hex_to_bytes(request.json["public_one_label"])
    gtt = list_conversion(request.json["gtt"], "hex", "bytes")
    e_output_bytes = evaluate_garbled_circuit(circuit_file, gginput_0, geinput, public_one_label, gtt)
    e_output = list_conversion(e_output_bytes, "bytes", "hex")
    return make_response({"eOutput": e_output})

@app.route("/garbler/first", methods=["POST"])
def garbler_first():
    num_of_einput = 128
    a, A = base_ot_sender_1(num_of_einput)
    A_list = list_conversion(A, "point2d", "hex")
    with open('./a.txt', 'w') as f:
        for i in range(len(a)):
            f.write(str(a[i]) + "\n")
    return make_response({"A": A_list})

@app.route("/garbler/second", methods=["POST"])
def garbler_second():
    circuit_file = './aes.txt'
    a = list()
    with open("./a.txt", 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            a.append(int(lines[i]))
    A = list_conversion(request.json["A"], "hex", "point2d")
    C = list_conversion(request.json["C"], "hex", "point2d")
    message_len_in_bytes = 16
    num_of_ginput = 256
    num_of_einput = 128
    delta, public_one_label, public_one_label_delta = garbler_init()
    gginput_0, gginput_1, geinput_0, geinput_1 = generate_garbled_input(num_of_ginput, num_of_einput, delta)
    e_0, e_1 = base_got_sender_2(num_of_einput, geinput_0, geinput_1, a, A, C, message_len_in_bytes)
    ginput = [1,1,1,1,0,1,1,0,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,1,1,1,1,1,1,1,0,0,1,1,0,1,0,1,1,0,1,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1,0,0,0,1,1,1,1,0,0,1,0,1,1,1,0,0,0,0,1,1,1,1,0,0,1,0,1,1,1,0,0,0,1,1,1,0,0,1,1,1,1,1,0,1,1,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,1,0,0,1,0,0, 0,1,1,0,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,0,0,0,0,1,1,0,1,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,0,0,1,0,1,1,0,0,1,1,0,0,1,1,0,0,0,1,1,0,1,1,0,0,1,0,0,0,0,1,1,0,1,1,0,0,1,1,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,1,1,0,1,1,1,0,0,1,1,1,0,0,0,0,0,1,1,0,0,1,0,0,0,1,1,0,0,1,1]
    g_output, gtt = compute_garbled_circuit(circuit_file, ginput, gginput_0, gginput_1, geinput_0, public_one_label_delta, delta)
    return make_response({
        "eMessage0": list_conversion(e_0, "bytes", "hex"),
        "eMessage1": list_conversion(e_1, "bytes", "hex"),
        "gGInput0": list_conversion(gginput_0, "bytes", "hex"),
        "publicOneLabel": bytes_to_hex(public_one_label),
        "gtt": list_conversion(gtt, "bytes", "hex"),
        "gOutput": list_conversion(g_output, "bytes", "hex"),
    })

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)