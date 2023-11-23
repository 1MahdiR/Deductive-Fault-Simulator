#
#   ISCAS Simulator
#   Author: MR
#   Usage: Run command 'python3 main.py test.bench vector.test'
#

import sys

from iscas_parser import Parser
from synthesizer import Synthesizer
from gates import *

if __name__ == "__main__":
    bench_file_path = sys.argv[1]
    input_file_path = sys.argv[2]

    inputs = None
    outputs = None
    gates_list = None
    gates = []

    bench_file = open(bench_file_path, "r")
    input_file = open(input_file_path, "r")
    parser = Parser(bench_file, input_file)

    bench_file.close()
    input_file.close()

    inputs, outputs, gates_list = parser.parse_bench()
    input_vector = parser.parse_input()

    for gate_tuple in gates_list:
        gate_output, gate_type, gate_inputs = gate_tuple
        gate = None
        
        if gate_type == "AND":
            gate = AND(gate_inputs, gate_output)
        elif gate_type == "OR":
            gate = OR(gate_inputs, gate_output)
        elif gate_type == "NAND":
            gate = NAND(gate_inputs, gate_output)
        elif gate_type == "NOR":
            gate = NOR(gate_inputs, gate_output)
        elif gate_type == "XOR":
            gate = XOR(gate_inputs, gate_output)
        elif gate_type == "XNOR":
            gate = XNOR(gate_inputs, gate_output)
        elif gate_type == "NOT":
            gate = NOT(gate_inputs, gate_output)
        elif gate_type == "BUFF":
            gate = BUFF(gate_inputs, gate_output)

        gates.append(gate)

    synthesizer = Synthesizer(inputs, outputs, gates)

    nets = synthesizer(input_vector)

    for key, value in nets.items():
        if type(value) == dict:
            for key2, value2 in value.items():
                print("%s: %s" % (key2, value2))
        else:
            print("%s: %s" % (key, value))
