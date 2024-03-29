#
# Parser for ISCAS Simulator
# 

class Parser:
    def __init__(self, bench_file, true_value_input_file, deductive_fault_input_file):
        self.bench_data = bench_file.readlines()
        self.true_value_input_data = true_value_input_file.readlines()
        self.deductive_fault_input_data = deductive_fault_input_file.readlines()

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
        true_value_input_vector = dict()
        lines = [ x[:-1] for x in self.true_value_input_data ]

        input_numbers = lines[0].split()
        input_values = lines[1].split()
        inputs = list(zip(input_numbers, input_values))
        for input_number, input_value in inputs:
            true_value_input_vector[input_number] = input_value

        deductive_fault_input_vector = dict()
        lines = [ x[:-1] for x in self.deductive_fault_input_data ]

        input_numbers = lines[0].split()
        input_values = lines[1].split()
        inputs = list(zip(input_numbers, input_values))
        for input_number, input_value in inputs:
            deductive_fault_input_vector[input_number] = input_value

        return (true_value_input_vector, deductive_fault_input_vector)

