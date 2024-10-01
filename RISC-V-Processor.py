



def read_input(file_txt):
    with open(file_txt, 'r') as f:
        instructions = [line.strip() for line in f.readlines()]
    return instructions



registers = {'r1':0,'r2':0,'r3':0}

class Instruction:
    def __init__(self):
        self.opcode = ""
    


def decomposition(instruction, category):
    array = []
    if category == "Category-1":
        imm_11_5 = instruction[0:7]
        rs2 = instruction[7:12]
        rs1 = instruction[12:17]
        func3 = instruction[17:20]
        imm_4_0 = instruction[20:25]
        opcode = instruction[25:30]
        constant_11 = instruction[30:32]
        array.extend([imm_11_5, rs2, rs1, func3, imm_4_0, opcode, constant_11])
    
    elif category == "Category-2":
        func7 = instruction[0:7]
        rs2 = instruction[7:12]
        rs1 = instruction[12:17]
        func3 = instruction[17:20]
        rd = instruction[20:25]
        opcode = instruction[25:30]
        constant_01 = instruction[30:32]
        array.extend([func7, rs2, rs1, func3, rd, opcode, constant_01])

    elif category == "Category-3":
        imm_11_0 = instruction[0:12]
        rs1 = instruction[12:17]
        func3 = instruction[17:20]
        rd = instruction[20:25]
        opcode = instruction[25:30]
        constant_10 = instruction[30:32]
        array.extend([imm_11_0, rs1, func3, rd, opcode, constant_10])

    elif category == "Category-4":
        imm_19_0 = instruction[0:20]
        rd = instruction[20:25]
        opcode = instruction[25:30]
        constant_00 = instruction[30:32]
        array.extend([imm_19_0, rd, opcode, constant_00])

    return array


class ALU:
    def __init__(self,category):
        self.category = category
        self.registers = [0]*32
        self.storage = {}

    def execute():
        print("hwll")

def Category(binary_input):
    category = "Category-"
    last_two_bits = binary_input[-2:]  # Get the last two bits

    if last_two_bits == '11':
        category += "1"
    elif last_two_bits == '01':
        category += "2"
    elif last_two_bits == '10':
        category += "3"
    elif last_two_bits == '00':
        category += "4"
    
    return category




    