# Garbled Circuit Python Implementation
This repo provides a workable Garbled Circuit implementation purely in Python.

## Installation
This project requires two cryptography libraries, one is cryptography (an OpenSSL wrapper) and the other one is py-ecc (Ethereum ECC implementation). Tested version is cryptograhpy==41.0.3 py-ecc==6.0.0. No other dependencies are required

## Implemented Protocols
Half And Gate with Free XOR protocol is implemented.

## Usage
### Half and gate verification
Run it with Python and you can find that the XOR operation on all elements of the two output sets should be the same (Note that, a_0 XOR a_1 = delta, but H(a_0) XOR H(a_1) != delta). This verifies the correctness of half and gate.

### Garbler Side Code
1. garbler.garbler_init(): Generate values shared between Garbler and Evaluator. It returns:
    a. delta (bytes): Free XOR label difference
    b. public_one_label (bytes): Label for public value 1 (Used by Evaluator ONLY in INV/NOT gate)
    c. public_one_label_delta (bytes): Label for public value 1 (Used by Garbler ONLY in INV/NOT gate)

2. garbler.generate_garbled_input(): Generate labels for input wires of both Garbler and Evaluator. It returns:
    a. gginput ([[bytes, bytes], [bytes, bytes], ..., [bytes, bytes]]): Garbled Garbler input (i.e. labels for Garbler input)
    b. geinput ([[bytes, bytes], [bytes, bytes], ..., [bytes, bytes]]): Garbled Evaluator input (i.e. labels for Evaluator input)

3. compute_garbled_circuit(): Compute output labels corresponding to all-0-bit output for Garbler. In this method, you should add Garbler's actual input bit list. Evaluator's input are all-0-bit input in this function. It returns:
    a. g_output (bytes): Garbler's output labels
    b. gtt ([bytes, bytes, ..., bytes]): Garbled Truth Table that needs to be sent to the Evaluator

### Evaluator Side Code
1. evaluator.evaluate_garbled_circuit(): Evaluate the garbled circuit. It returns:
    a. e_output (bytes): Evaluator's output labels

### Verify the Result
For the i'th group of bytes in g_output and e_output, if they are the same, it means the current bit is 0. This is because each group of bytes in g_output denote the 0 label.
