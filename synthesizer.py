#
#   Synthesizer definition for ISCAS Simulator
#   Synthesizer returns a digital circuit given input and output vectors and gate definitions
#

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
