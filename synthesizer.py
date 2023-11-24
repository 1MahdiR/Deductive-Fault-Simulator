#
#   Synthesizer definition for ISCAS Simulator
#   Synthesizer returns a digital circuit given input and output vectors and gate definitions
#

import copy

from gates import *

class Synthesizer:
    def __init__(self, inputs:list, outputs:list, gates:list):
        self.inputs = inputs
        self.outputs = outputs
        self.gates = gates
        self.nets = dict()

        for gate in gates:
            for input_ in gate.inputs:
                if self.nets.get(input_):
                    value = self.nets.get(input_)
                    if type(value) == dict:
                        new_length = len(value) + 1
                        value["{}_{}".format(input_, new_length)] = UNKNOWN
                    else:
                        self.nets[input_] = {"{}_1".format(input_):UNKNOWN}
                        self.nets[input_]["{}_2".format(input_)] = UNKNOWN
                else:
                    self.nets[input_] = UNKNOWN
        
        for output in self.outputs:
            self.nets[output] = UNKNOWN

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

                if out != UNKNOWN:
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

        for net in self.nets:
            calculated_faults[net] = set()
            if type(self.nets[net]) == dict:
                for net2 in self.nets[net]:
                    calculated_faults[net2] = set()

        for temp_input in self.inputs:
            value = input_vector[temp_input]
            if value == '0':
                calculated_faults[temp_input].add('{}(1)'.format(temp_input))
            else:
                calculated_faults[temp_input].add('{}(0)'.format(temp_input))

        while True:
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

            for gate in self.gates:
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
                    for gate_input, _ in gate_inputs:
                            for item in calculated_faults[gate_input]:
                                calculated_fault.add(item)
                    
                    if gate_output_value == "0":
                        calculated_fault.add("{}(1)".format(gate_output))
                    else:
                        calculated_fault.add("{}(0)".format(gate_output))

                calculated_faults[gate_output] = calculated_fault
            
            if not (set() in list(calculated_faults.values())):
                break

        return calculated_faults
