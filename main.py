#
#   ISCAS Simulator
#   Author: MR
#   Usage: Run command 'python3 main.py test.bench vector1.test vector2.test'
#

import sys

from iscas_parser import Parser
from synthesizer import Synthesizer
from gates import *

if __name__ == "__main__":
    bench_file_path = sys.argv[1]
    true_value_simulation_input_file_path = sys.argv[2]
    deductive_fault_simulation_input_file_path = sys.argv[3]

    inputs = None
    outputs = None
    gates_list = None
    gates = []

    bench_file = open(bench_file_path, "r")
    true_value_simulation_input_file = open(true_value_simulation_input_file_path, "r")
    deductive_fault_simulation_input_file = open(deductive_fault_simulation_input_file_path, "r")
    parser = Parser(bench_file, true_value_simulation_input_file, deductive_fault_simulation_input_file)

    bench_file.close()
    true_value_simulation_input_file.close()
    deductive_fault_simulation_input_file.close()

    inputs, outputs, gates_list = parser.parse_bench()
    true_value_input_vector, deductive_fault_input_vector = parser.parse_input()

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

    nets = synthesizer(true_value_input_vector)

    print("True-value simulation:")
    for key, value in nets.items():
        if type(value) == dict:
            for key2, value2 in value.items():
                print("%s: %s" % (key2, value2))
        else:
            print("%s: %s" % (key, value))
    
    print()
    print("Deductive fault simulation:")
    faults = synthesizer.deductive_fault_simulation(deductive_fault_input_vector)
    for key, value in faults.items():
        text = ", ".join(list(value))
        print("{}: {}".format(key, text))
