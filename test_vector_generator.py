#
#   Random test vector generator for ISCAS simulator
#   Usage: python3 test_vector_generator.py [input count]
#

import sys
import random
import time

from iscas_parser import Parser

if __name__ == "__main__":
    bench_file_path = sys.argv[1]
    random.seed(time.clock_gettime_ns(1)%100)
    true_value_values_high_prop = ('1', '0')
    true_value_values_low_prop = ('Z', 'U')
    deductive_fault_values = ('1', '0')
    bench_file = open(bench_file_path, "r")
    _ = open(bench_file_path, "r")
    parser = Parser(bench_file, _, _)
    _.close()
    bench_file.close()

    inputs = parser.parse_bench()[0]

    with open("bench/true_value_input.txt", "w") as f:
        f.write(" ".join(inputs))
        f.write("\n")
        ls = []
        for i in range(len(inputs)):
            if random.randint(0, 9):
                ls.append(random.choice(true_value_values_high_prop))
            else:
                ls.append(random.choice(true_value_values_low_prop))
        f.write(" ".join(ls))
        f.write("\n")

    with open("bench/deductive_fault_input.txt", "w") as f:
        f.write(" ".join(inputs))
        f.write("\n")
        ls = []
        for i in range(len(inputs)):
            ls.append(random.choice(deductive_fault_values))
        f.write(" ".join(ls))
        f.write("\n")
