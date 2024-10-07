
#TODO:1) Finish up implement all thhe instructions: 
#TODO 2) Ensure that is the correct immediate values: 
#TODO 3) Make instructions compute values 
#TODO 4) Make two files when running script 
#TODO 5) Run tests
#TODO 6) Right comments and optimize code

registers = {f"x{i}": 0 for i in range(32)}

data_storage = [0]*1024
opcode_1 = {'00000': "beq", '00001': "bne", '00010': "blt", '00011': "sw"}
opcode_2 = {'00000': "add", '00001': "sub", "00010": "and", "00011": "or"}
opcode_3 = {'00000': "addi", '00001': "andi", "00010": "ori", "00011": "sll", "00100": 'sra', "00101": 'lw'}
opcode_4 = {'00000': "jal", '11111': "break"}

current_pc = 256
flag = False

class Instruction:
    def __init__(self):
        self.category = ""
        self.opcode_name = ""
        self.curr_ins_str =""
        # Category 1
        self.opcode = ""
        self.im_11_5 = ""
        self.rs2 = ""
        self.rs1 = ""
        self.func3 = ""
        self.imm_4_0 = ""
        self.constant = ""
        # Category 2
        self.func7 = ""
        self.rd = ""
        self.constant01 = ""
        # Category 3
        self.imm_11_0 = ""
        self.constant10 = ""
        self.imm_19_0 = ""
        self.constant_10 = ""
        # Category 4
        self.imm_19_0 = ""
        self.constant_00 = ""
        self.imm_14_0 = ""

    def setCategory1(self, imm_11_5, rs2, rs1, func3, imm_4_0, opcode, constant_11):
        self.im_11_5 = imm_11_5
        self.rs2 = rs2
        self.rs1 = rs1
        self.func3 = func3
        self.imm_4_0 = imm_4_0
        self.opcode = opcode
        self.constant_11 = constant_11
        self.imm_14_0 = self.im_11_5+self.imm_4_0

    def setCategory2(self, func7, rs2, rs1, func3, rd, opcode, constant_01):
        self.func7 = func7
        self.rs2 = rs2
        self.rs1 = rs1
        self.func3 = func3
        self.rd = rd
        self.opcode = opcode
        self.constant01 = constant_01

    def setCategory3(self, imm_11_0, rs1, func3, rd, opcode, constant_10):
        self.imm_11_0 = imm_11_0
        self.rs1 = rs1
        self.func3 = func3
        self.rd = rd
        self.opcode = opcode
        self.constant10 = constant_10

    def setCategory4(self, imm_19_0, rd, opcode, constant_00):
        self.imm_19_0 = imm_19_0
        self.rd = rd
        self.opcode = opcode
        self.constant_00 = constant_00

    def getopcode(self):
        return self.opcode

    def setopcode(self, opcode):
        self.opcode = opcode

    def setCategory(self, category):
        self.category = category

    def getCategory(self):
        return self.category

    def setOpcodeName(self, opcode_name):
        self.opcode_name = opcode_name
    def set_curr_ins_str(self,instructon_string):
        self.curr_ins_str = instructon_string
    

    
def unsigned_bin__to_int(binary_string):
    binary_list = [int(i) for i in list(binary_string)] 
    res = -binary_list[0] * (2 ** (len(binary_list) - 1)) 
    for i in range(1, len(binary_list)):
        res += binary_list[i] * (2 ** (len(binary_list) - i - 1)) 
    return res


def decomposition(instruction_obj, instruction_binary_line):
    category = Category(instruction_binary_line)
    instruction_obj.setCategory(category)
    
    if category == "Category-1":
        imm_11_5 = instruction_binary_line[0:7]
        rs2 = instruction_binary_line[7:12]
        rs1 = instruction_binary_line[12:17]
        func3 = instruction_binary_line[17:20]
        imm_4_0 = instruction_binary_line[20:25]
        opcode = instruction_binary_line[25:30]
        constant_11 = instruction_binary_line[30:32]
        instruction_obj.setCategory1(imm_11_5, rs2, rs1, func3, imm_4_0, opcode, constant_11)
        instruction_obj.setOpcodeName(opcode_1.get(opcode, "Unknown"))

    elif category == "Category-2":
        func7 = instruction_binary_line[0:7]
        rs2 = instruction_binary_line[7:12]
        rs1 = instruction_binary_line[12:17]
       
        func3 = instruction_binary_line[17:20]
        rd = instruction_binary_line[20:25]
        opcode = instruction_binary_line[25:30]
        constant_01 = instruction_binary_line[30:32]
        instruction_obj.setCategory2(func7, rs2, rs1, func3, rd, opcode, constant_01)
        instruction_obj.setOpcodeName(opcode_2.get(opcode, "Unknown"))

    elif category == "Category-3":
        imm_11_0 = instruction_binary_line[0:12]
        rs1 = instruction_binary_line[12:17]
        func3 = instruction_binary_line[17:20]
        rd = instruction_binary_line[20:25]
        opcode = instruction_binary_line[25:30]
        constant_10 = instruction_binary_line[30:32]
        instruction_obj.setCategory3(imm_11_0, rs1, func3, rd, opcode, constant_10)
        instruction_obj.setOpcodeName(opcode_3.get(opcode, "Unknown"))

    elif category == "Category-4":
        imm_19_0 = instruction_binary_line[0:20]
        rd = instruction_binary_line[20:25]
        opcode = instruction_binary_line[25:30]
        constant_00 = instruction_binary_line[30:32]
        instruction_obj.setCategory4(imm_19_0, rd, opcode, constant_00)
        instruction_obj.setOpcodeName(opcode_4.get(opcode, "Unknown"))



##Class ALU
class ALU:
    def __init__(self, instruction: Instruction):
        self.instruction = instruction
        self.flag = flag 

    def execute(self):
        opcode_name = self.instruction.opcode_name
        # Dispatch to the correct method based on the opcode name
        method = getattr(self, opcode_name, None)

        if method:
            return method()
        elif opcode_name == 'break':
            return self.break_()
        else:
            print("mistake")

    def add(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rs2 = f"x{int(self.instruction.rs2, 2)}"
        rd = f"x{int(self.instruction.rd, 2)}"
        rs1_value = registers.get(rs1, 0)
        rs2_value = registers.get(rs2, 0)
        result = rs1_value + rs2_value
        registers[rd] = result
        self.instruction.set_curr_ins_str(f"{current_pc} add {rd}, {rs1}, {rs2}")
        print(self.instruction.curr_ins_str)
        return result

    def sub(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rs2 = f"x{int(self.instruction.rs2, 2)}"
        rd = f"x{int(self.instruction.rd, 2)}"
        rs1_value = registers.get(rs1, 0)
        rs2_value = registers.get(rs2, 0)
        result = rs1_value - rs2_value
        registers[rd] = result
        self.instruction.set_curr_ins_str(f"{current_pc} sub {rd}, {rs1}, {rs2}")
        print(self.instruction.curr_ins_str)
        return result

    def beq(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rs2 = f"x{int(self.instruction.rs2, 2)}"
        rs1_value = registers.get(rs1, 0)
        rs2_value = registers.get(rs2, 0)
        condition = rs1_value == rs2_value
        self.instruction.set_curr_ins_str(f"{current_pc} beq {rs1}, {rs2}")
        print(self.instruction.curr_ins_str)

    def addi(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rd = f"x{int(self.instruction.rd, 2)}"
        rs1_value = registers.get(rs1, 0)
        imm_value = int(self.instruction.imm_11_0, 2)
        result = rs1_value + imm_value
        registers[rd] = result
        self.instruction.set_curr_ins_str(f"{current_pc} addi {rd}, {rs1}, {imm_value}")
        print(self.instruction.curr_ins_str)
        return result

    def andi(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rd = f"x{int(self.instruction.rd, 2)}"
        rs1_value = registers.get(rs1, 0)
        imm_value = int(self.instruction.imm_11_0, 2)
        result = rs1_value & imm_value
        registers[rd] = result
        self.instruction.set_curr_ins_str(f"{current_pc} andi {rd}, {rs1}, {imm_value}")
        print(self.instruction.curr_ins_str)
        return result

    def ori(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rd = f"x{int(self.instruction.rd, 2)}"
        rs1_value = registers.get(rs1, 0)
        imm_value = int(self.instruction.imm_11_0, 2)
        result = rs1_value | imm_value
        registers[rd] = result
        self.instruction.set_curr_ins_str(f"{current_pc} ori {rd}, {rs1}, {imm_value}")
        print(self.instruction.curr_ins_str)
        return result

    def sll(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rs2 = f"x{int(self.instruction.rs2, 2)}"
        rd = f"x{int(self.instruction.rd, 2)}"
        rs1_value = registers.get(rs1, 0)
        rs2_value = registers.get(rs2, 0)
        result = rs1_value << rs2_value
        registers[rd] = result
        self.instruction.set_curr_ins_str(f"{current_pc} sll {rd}, {rs1}, {rs2}")
        print(self.instruction.curr_ins_str)
        return result

    def sra(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rs2 = f"x{int(self.instruction.rs2, 2)}"
        rd = f"x{int(self.instruction.rd, 2)}"
        rs1_value = registers.get(rs1, 0)
        rs2_value = registers.get(rs2, 0)
        result = rs1_value >> rs2_value
        registers[rd] = result
        self.instruction.set_curr_ins_str(f"{current_pc} sra {rd}, {rs1}, {rs2}")
        print(self.instruction.curr_ins_str)
        return result

    def lw(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rd = f"x{int(self.instruction.rd, 2)}"
        address = registers.get(rs1, 0) + int(self.instruction.imm_11_0, 2)
        if address < len(data_storage):
            result = data_storage[address]
            registers[rd] = result
            self.instruction.set_curr_ins_str(f"{current_pc} lw {rd}, {address}({rs1})")
            print(self.instruction.curr_ins_str)
            return result
        else:
            print(f"Error: Memory address {address} out of bounds.")
            return None

    def sw(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rs2 = f"x{int(self.instruction.rs2, 2)}"
        address = registers.get(rs1, 0) + int(self.instruction.im_11_5, 2)
        rs2_value = registers.get(rs2, 0)
        if address < len(data_storage):
            data_storage[address] = rs2_value
            self.instruction.set_curr_ins_str(f"{current_pc} sw {rs2}, {address}({rs1})")
            print(self.instruction.curr_ins_str)
            return rs2_value
        else:
            print(f"Error: Memory address {address} out of bounds.")
            return None

    def jal(self):
        rd = f"x{int(self.instruction.rd, 2)}"
        imm_19_0 = f"{unsigned_bin__to_int(self.instruction.imm_19_0)}"
        self.instruction.set_curr_ins_str(f"{current_pc} jal {rd}, #{imm_19_0}")
        print(self.instruction.curr_ins_str)

    def break_(self):
        self.instruction.set_curr_ins_str(f"{current_pc} break")
        print(self.instruction.curr_ins_str)
        self.flag = True  
    def blt(self):
            rs1 = f"x{int(self.instruction.rs1, 2)}"
            rs2 = f"x{int(self.instruction.rs2, 2)}"
            rs1_value = registers.get(rs1, 0)
            rs2_value = registers.get(rs2, 0)
            
            offset = unsigned_bin__to_int(self.instruction.imm_14_0)
            
            self.instruction.set_curr_ins_str(f"{current_pc} blt {rs1}, {rs2}, #{offset}")
            print(self.instruction.curr_ins_str)
            


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


file = "sample.txt"


def read_input(file_txt):
    with open(file_txt, 'r') as f:
        instructions = [line.strip() for line in f.readlines()]
    return instructions


instructions = read_input(file)

current_instruction = Instruction()

alu = ALU(current_instruction)



i=0
while i<len(instructions):
    decomposition(current_instruction, instructions[i])
    alu.execute()
    if alu.flag:
        break
    i +=1

    current_pc +=4
