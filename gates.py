#
# Gate definitions for ISCAS Simulator
#

### CONSTANTS ###
LOW = "0"
HIGH = "1"
UNKNOW = "U"
HI_IMPEDANCE = "Z"
###

class AND:
    def __init__(self, inputs:list, output):
        self.inputs = inputs
        self.output = output

    def __call__(self, inputs):
        if len(inputs) != len(self.inputs):
            raise ValueError("Input vector does not match the gate's definition!")
        for i in inputs:
            if i == LOW:
                return LOW
        return HIGH
    
class OR:
    def __init__(self, inputs:list, output):
        self.inputs = inputs
        self.output = output

    def __call__(self, inputs):
        if len(inputs) != len(self.inputs):
            raise ValueError("Input vector does not match the gate's definition!")
        for i in inputs:
            if i == HIGH:
                return HIGH
        return LOW
    
class NAND:
    def __init__(self, inputs:list, output):
        self.inputs = inputs
        self.output = output

    def __call__(self, inputs):
        if len(inputs) != len(self.inputs):
            raise ValueError("Input vector does not match the gate's definition!")
        for i in inputs:
            if i == LOW:
                return HIGH
        return LOW
    
class NOR:
    def __init__(self, inputs:list, output):
        self.inputs = inputs
        self.output = output

    def __call__(self, inputs):
        if len(inputs) != len(self.inputs):
            raise ValueError("Input vector does not match the gate's definition!")
        for i in inputs:
            if i == HIGH:
                return LOW
        return HIGH
    
class XOR:
    def __init__(self, inputs:list, output):
        self.inputs = inputs
        self.output = output

    def __call__(self, inputs):
        if len(inputs) != len(self.inputs):
            raise ValueError("Input vector does not match the gate's definition!")
        if inputs.count(HIGH) % 2 == 1: # Number of high inputs is odd
            return HIGH
        return LOW
    
class XNOR:
    def __init__(self, inputs:list, output):
        self.inputs = inputs
        self.output = output

    def __call__(self, inputs):
        if len(inputs) != len(self.inputs):
            raise ValueError("Input vector does not match the gate's definition!")
        if inputs.count(HIGH) % 2 == 0: # Number of high inputs is even
            return HIGH
        return LOW
    
class NOT:
    def __init__(self, input:int, output):
        self.input = input
        self.output = output

    def __call__(self, input):
        if input == HIGH:
            return LOW
        return HIGH
    
class BUFF:
    def __init__(self, input:int, output):
        self.input = input
        self.output = output

    def __call__(self, input):
        if input == HIGH:
            return HIGH
        return LOW
    