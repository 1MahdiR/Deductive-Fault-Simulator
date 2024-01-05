#
#   Synthesizer definition for ISCAS Simulator
#   Synthesizer returns a digital circuit given input and output vectors and gate definitions
#

import copy
from tabulate import tabulate

from gates import *

def generate_binary_patterns(n):
    if n <= 0:
        return []

    patterns = []
    def backtrack(pattern):
        if len(pattern) == n:
            patterns.append(pattern)
            return

        backtrack(pattern + '0')
        backtrack(pattern + '1')

    backtrack('')
    return patterns

class Synthesizer:
    def __init__(self, inputs:list, outputs:list, gates:list):
        self.inputs = inputs
        self.outputs = outputs
        self.gates = gates
        self.nets = dict()
        self.output_dependancy = dict()

        for gate in gates:
            for input_ in gate.inputs:
                if self.nets.get(input_):
                    value = self.nets.get(input_)
                    if type(value) == dict:
                        new_length = len(value) + 1
                        value["{}_{}".format(input_, new_length)] = UNSET
                    else:
                        self.nets[input_] = {"{}".format(input_):UNSET}
                        self.nets[input_]["{}_1".format(input_)] = UNSET
                        self.nets[input_]["{}_2".format(input_)] = UNSET
                else:
                    self.nets[input_] = UNKNOWN
        
        for output in self.outputs:
            self.nets[output] = UNKNOWN

        while True:
            for gate in self.gates:
                max_level = 0
                for input_ in gate.inputs:
                    if input_ not in self.inputs:
                        gatej = None
                        for temp_gate in self.gates:
                            if temp_gate.output == input_:
                                gatej = temp_gate

                        if max_level < gatej.level:
                            max_level = gatej.level
                gate.level = max_level + 1
            if not 0 in [ x.level for x in self.gates ]:
                break

        #print([ (x.inputs, x.output, x.level) for x in self.gates ])

    def __call__(self, input_vector:dict):

        temp_output = self.outputs.copy()
        temp_gates = self.gates.copy()
        temp_nets = self.nets.copy()

        for key, value in input_vector.items():
            if type(temp_nets[key]) != dict:
                temp_nets[key] = value
            else:
                for key2 in temp_nets[key]:
                    temp_nets[key][key2] = value

        while temp_output:
            for gate in temp_gates:
                gate_input_vector = []
                for net in gate.inputs:
                    if type(temp_nets[net]) != dict:
                        gate_input_vector.append(temp_nets[net])
                    else:
                        gate_input_vector.append(list(temp_nets[net].values())[0])

                out = gate(gate_input_vector)

                if out != UNSET:
                    if type(temp_nets[gate.output]) != dict:
                        temp_nets[gate.output] = out
                    else:
                        for key in temp_nets[gate.output].keys():
                            temp_nets[gate.output][key] = out

                    if gate.output in temp_output:
                        temp_output.remove(gate.output)
        
        return temp_nets

    def deductive_fault_simulation(self, input_vector:dict):
        calculated_faults = dict()
        true_value_simulation = self(input_vector)

        for net in self.nets:
            calculated_faults[net] = set()
            if type(self.nets[net]) == dict:
                for net2 in self.nets[net]:
                    calculated_faults[net2] = set()

        output_dependancy = dict()

        temp_nets = copy.deepcopy(self.nets)
        for gate in self.gates:
            gate_output = gate.output
            gate_inputs = gate.inputs
            output_dependancy[gate_output] = []
            for gate_input in gate_inputs:
                gate_input_value = None
                if type(true_value_simulation[gate_input]) == dict:
                    gate_input_value = list(true_value_simulation[gate_input].values())[0]
                else:
                    gate_input_value = true_value_simulation[gate_input]
                if type(temp_nets[gate_input]) == dict:
                    net = temp_nets[gate_input].popitem()[0]
                    output_dependancy[gate_output].append((net, gate_input_value))
                else:
                    output_dependancy[gate_output].append((gate_input, gate_input_value))

        for temp_input in self.inputs:
            value = input_vector[temp_input]
            if value == '0':
                calculated_faults[temp_input].add('{}(1)'.format(temp_input))
            else:
                calculated_faults[temp_input].add('{}(0)'.format(temp_input))

        for net in calculated_faults:
                if (not calculated_faults[net]) and "_" in net:
                    net_main, net_branch = net.split("_")
                    if calculated_faults[net_main]:
                        value = calculated_faults[net_main]
                        for item in value:
                            calculated_faults[net].add(item)
                        if type(true_value_simulation[net_main]) == dict:
                            if list(true_value_simulation[net_main].values())[0] == '0':
                                calculated_faults[net].add('{}(1)'.format(net))
                            else:
                                calculated_faults[net].add('{}(0)'.format(net))
                        else:
                            if true_value_simulation[net_main] == '0':
                                calculated_faults[net].add('{}(1)'.format(net))
                            else:
                                calculated_faults[net].add('{}(0)'.format(net))
        
        temp_gates = copy.deepcopy(self.gates)
        temp_gates.sort(key=lambda x: x.level, reverse=True)

        while temp_gates:
            gate = temp_gates.pop()
            gate_output = gate.output
            gate_output_value = None
            if type(true_value_simulation[gate_output]) == dict:
                gate_output_value = list(true_value_simulation[gate_output].values())[0]
            else:
                gate_output_value = true_value_simulation[gate_output]

            gate_inputs = output_dependancy[gate_output]
            calculated_fault = set()
            
            if type(gate) == NAND or type(gate) == AND:
                if "0" in [ x[1] for x in gate_inputs ]:
                    ls = []
                    for gate_input, value in gate_inputs:
                        if value == "0":
                            ls.append(calculated_faults[gate_input])
                    ls_intersection = set.intersection(*ls)

                    ls = []
                    for gate_input, value in gate_inputs:
                        if value == "1":
                            ls.append(calculated_faults[gate_input])
                    if ls:
                        ls_union = set.union(*ls)
                    else:
                        ls_union = set()
                    
                    calculated_fault = ls_intersection.difference(ls_union)

                else:
                    for gate_input, _ in gate_inputs:
                        for item in calculated_faults[gate_input]:
                            calculated_fault.add(item)
                
                if gate_output_value == "0":
                    calculated_fault.add("{}(1)".format(gate_output))
                else:
                    calculated_fault.add("{}(0)".format(gate_output))

            elif type(gate) == NOR or type(gate) == OR:
                if "1" in [ x[1] for x in gate_inputs ]:
                    ls = []
                    for gate_input, value in gate_inputs:
                        if value == "1":
                            ls.append(calculated_faults[gate_input])
                    ls_intersection = set.intersection(*ls)

                    ls = []
                    for gate_input, value in gate_inputs:
                        if value == "0":
                            ls.append(calculated_faults[gate_input])
                    if ls:
                        ls_union = set.union(*ls)
                    else:
                        ls_union = set()
                    
                    calculated_fault = ls_intersection.difference(ls_union)

                else:
                    for gate_input, _ in gate_inputs:
                        for item in calculated_faults[gate_input]:
                            calculated_fault.add(item)
                
                if gate_output_value == "0":
                    calculated_fault.add("{}(1)".format(gate_output))
                else:
                    calculated_fault.add("{}(0)".format(gate_output))
            
            elif type(gate) == NOT or type(gate) == BUFF:
                gate_input, gate_input_value = gate_inputs[0]
                calculated_fault = calculated_faults[gate_input].copy()
                if gate_output_value == "0":
                    calculated_fault.add("{}(1)".format(gate_output))
                else:
                    calculated_fault.add("{}(0)".format(gate_output))
                
            elif type(gate) == XOR or type(gate) == XNOR:
                fault_line = dict()
                for gate_input, _ in gate_inputs:
                    faults = calculated_faults[gate_input]
                    for fault in faults:
                        if fault_line.get(fault):
                            fault_line[fault].append(gate_input)
                        else:
                            fault_line[fault] = [gate_input]

                for fault, inputs in fault_line.items():
                    if len(inputs) % 2 == 1:
                        calculated_fault.add(fault)
                
                if gate_output_value == "0":
                    calculated_fault.add("{}(1)".format(gate_output))
                else:
                    calculated_fault.add("{}(0)".format(gate_output))

            calculated_faults[gate_output] = calculated_fault

            if type(true_value_simulation[gate_output]) == dict:
                for line, value in true_value_simulation[gate_output].items():
                    if "_" in line:
                        calculated_faults[line] = calculated_fault.copy()
                        if value == "0":
                            calculated_faults[line].add("{}(1)".format(line))
                        else:
                            calculated_faults[line].add("{}(0)".format(line))
                    
        return calculated_faults
    
    def exhuastive_method(self):
        patterns = generate_binary_patterns(len(self.inputs))
        test_vector = dict()

        all_faults = dict()

        for pattern in patterns:
            for i, j in zip(pattern, self.inputs):
                test_vector[j] = i
            
            faults = self.deductive_fault_simulation(test_vector)

            all_faults[pattern] = dict()
            
            output_faults = set()
            for i in self.outputs:
                for j in faults[i]:
                    output_faults.add(j)
            
            all_faults[pattern] = output_faults

        return all_faults
    
    def fault_table_analysis(self):
        all_detectable_faults = self.exhuastic_method()
        all_faults = list()
        for line in self.nets.keys():
            if type(self.nets[line]) == dict:
                for i in self.nets[line].keys():
                    all_faults.append("{}(0)".format(i))
                    all_faults.append("{}(1)".format(i))
            else:
                all_faults.append("{}(0)".format(line))
                all_faults.append("{}(1)".format(line))
        all_faults.sort()

        faults_row = set()
        for i, j in all_detectable_faults.items():
            for k in j:
                faults_row.add(k)

        faults_row = sorted(list(faults_row))
        fault_data = list()
        for pattern, faults in all_detectable_faults.items():
            ls = [pattern]
            for fault in all_faults:
                if fault in faults:
                    ls.append("#")
                else:
                    ls.append("")
            fault_data.append(ls)

        
        table = tabulate(fault_data, list(all_faults), tablefmt="grid")
        print(table)

        fault_test_vector_count = dict()
        for fault in faults_row:
            for pattern, faults in all_detectable_faults.items():
                if fault in faults:
                    if fault_test_vector_count.get(fault):
                        fault_test_vector_count[fault] += 1
                    else:
                        fault_test_vector_count[fault] = 1

        essential_vectors = []
        
        for pattern, faults in all_detectable_faults.items():
            for fault in faults:
                if fault_test_vector_count[fault] == 1:
                    essential_vectors.append(pattern)
                    break

        covered_faults = dict()
        for i in all_faults:
            covered_faults[i] = False
        
        selected_vectors = essential_vectors.copy()

        for pattern in selected_vectors:
            faults = all_detectable_faults[pattern]
            for fault in faults:
                covered_faults[fault] = True

        for pattern, faults in all_detectable_faults.items():
            selected_vectors.append(pattern)
            for fault in faults:
                covered_faults[fault] = True
            if not False in covered_faults.values():
                break
        
        print()
        print("Essential test vectors: ")
        for i in essential_vectors:
            print(i)

        print()
        print("Selected test vectors: ")
        for i in selected_vectors:
            print(i)

        print()
        print("Fault coverage: {}%".format(list(covered_faults.values()).count(True) * (100 / len(covered_faults.values()))))