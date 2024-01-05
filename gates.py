#
#   Gate definitions for ISCAS Simulator
#

### CONSTANTS ###
LOW = "0"
HIGH = "1"
UNKNOWN = "U"
HI_IMPEDANCE = "Z"
UNSET = "-"
###

class AND:
    def __init__(self, inputs:list, output, level):
        self.inputs = inputs
        self.output = output
        self.level = level

    def __call__(self, inputs):
        if len(inputs) != len(self.inputs):
            raise ValueError("Input vector does not match the gate's definition!")
        if LOW in inputs:
            return LOW
        if UNKNOWN in inputs:
            return UNKNOWN
        if HI_IMPEDANCE in inputs:
            return UNKNOWN
        return HIGH
    
class OR:
    def __init__(self, inputs:list, output, level):
        self.inputs = inputs
        self.output = output
        self.level = level

    def __call__(self, inputs):
        if len(inputs) != len(self.inputs):
            raise ValueError("Input vector does not match the gate's definition!")
        if HIGH in inputs:
            return HIGH
        if UNKNOWN in inputs:
            return UNKNOWN
        if HI_IMPEDANCE in inputs:
            return UNKNOWN
        return LOW
    
class NAND:
    def __init__(self, inputs:list, output, level):
        self.inputs = inputs
        self.output = output
        self.level = level

    def __call__(self, inputs):
        if len(inputs) != len(self.inputs):
            raise ValueError("Input vector does not match the gate's definition!")
        if LOW in inputs:
            return HIGH
        if UNKNOWN in inputs:
            return UNKNOWN
        if HI_IMPEDANCE in inputs:
            return UNKNOWN
        return LOW
    
class NOR:
    def __init__(self, inputs:list, output, level):
        self.inputs = inputs
        self.output = output
        self.level = level

    def __call__(self, inputs):
        if len(inputs) != len(self.inputs):
            raise ValueError("Input vector does not match the gate's definition!")
        if HIGH in inputs:
            return LOW
        if UNKNOWN in inputs:
            return UNKNOWN
        if HI_IMPEDANCE in inputs:
            return UNKNOWN
        return HIGH
    
class XOR:
    def __init__(self, inputs:list, output, level):
        self.inputs = inputs
        self.output = output
        self.level = level

    def __call__(self, inputs):
        if len(inputs) != len(self.inputs):
            raise ValueError("Input vector does not match the gate's definition!")
        if UNKNOWN in inputs:
            return UNKNOWN
        if HI_IMPEDANCE in inputs:
            return UNKNOWN
        if inputs.count(HIGH) % 2 == 1: # Number of high inputs is odd
            return HIGH
        return LOW
    
class XNOR:
    def __init__(self, inputs:list, output, level):
        self.inputs = inputs
        self.output = output
        self.level = level

    def __call__(self, inputs):
        if len(inputs) != len(self.inputs):
            raise ValueError("Input vector does not match the gate's definition!")
        if UNKNOWN in inputs:
            return UNKNOWN
        if HI_IMPEDANCE in inputs:
            return UNKNOWN
        if inputs.count(HIGH) % 2 == 0: # Number of high inputs is even
            return HIGH
        return LOW
    
class NOT:
    def __init__(self, inputs:list, output, level):
        self.inputs = inputs
        self.output = output
        self.level = level

    def __call__(self, inputs):
        if not len(inputs):
            raise ValueError("Input vector does not match the gate's definition!")
        if inputs[0] == HIGH:
            return LOW
        if inputs[0] == HI_IMPEDANCE:
            return UNKNOWN
        if inputs[0] == UNKNOWN:
            return UNKNOWN
        return HIGH
    
class BUFF:
    def __init__(self, inputs:list, output, level):
        self.inputs = inputs
        self.output = output
        self.level = level

    def __call__(self, inputs):
        if not len(inputs):
            raise ValueError("Input vector does not match the gate's definition!")
        if inputs[0] == HIGH:
            return HIGH
        if inputs[0] == HI_IMPEDANCE:
            return UNKNOWN
        if inputs[0] == UNKNOWN:
            return UNKNOWN
        return LOW
    