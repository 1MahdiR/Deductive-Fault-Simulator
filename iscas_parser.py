#
# Parser for ISCAS Simulator
# 

class Parser:
    def __init__(self, bench_file, input_file):
        self.bench_data = bench_file.readlines()
        self.input_data = input_file.readlines()

    def parse_bench(self):

        inputs = []
        outputs = []
        gates = []

        for line in self.bench_data:
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

    def parse_input(self):
        input_vector = dict()
        lines = [ x[:-1] for x in self.input_data ]

        input_numbers = lines[0].split()
        input_values = lines[1].split()
        inputs = list(zip(input_numbers, input_values))
        for input_number, input_value in inputs:
            input_vector[input_number] = input_value

        return input_vector
