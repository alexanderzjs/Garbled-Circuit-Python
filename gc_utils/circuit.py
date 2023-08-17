from typing import Union

def load_circuit_from_file(circuit_file: str) -> Union[list, int, int, int, int, int]:
    gates = list()
    with open(circuit_file, "r") as circuit_f:
        lines = circuit_f.readlines()
        # circuit statistics
        line = lines[0].split()
        num_of_gate, num_of_wire = int(line[0]), int(line[1])
        line = lines[1].split()
        num_of_ginput, num_of_einput, num_of_output = int(line[0]), int(line[1]), int(line[2])
        for i in range(3, len(lines)):
            line = lines[i].split()
            if line[0] == '2':
                gates.append(int(line[2]))
                gates.append(int(line[3]))
                gates.append(int(line[4]))
                if line[5] == 'AND':
                   gates.append(0)
                elif line[5] == 'XOR':
                   gates.append(1)
                elif line[5] == 'OR':
                   gates.append(3)
            elif line[0] == '1':
                gates.append(int(line[2]))
                gates.append(-1)
                gates.append(int(line[3]))
                gates.append(2)
    return gates, num_of_gate, num_of_wire, num_of_ginput, num_of_einput, num_of_output

