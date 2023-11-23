#
# Parser for ISCAS Simulator
# 

class Parser:
    def __init__(self, file):
        self.data = file.readlines()

    def parse_bench(self):

        inputs = []
        outputs = []
        gates = []

        for line in self.data:
            if "INPUT" in line:
                start_p = line.find("(")
                end_p = line.find(")")

                input_number = line[start_p+1:end_p]

                inputs.append(input_number)

            if "OUTPUT" in line:
                start_p = line.find("(")
                end_p = line.find(")")

                output_number = line[start_p+1:end_p]

                outputs.append(output_number)            

            if "=" in line:
                gate_output, gate = line.split(" = ")
                gate_type, gate_inputs_str = gate.split("(")
                gate_inputs = [ x.strip() for x in gate_inputs_str[:-2].split(',') ]

                gates.append((gate_output, gate_type, gate_inputs))
        
        return (inputs, outputs, gates)
