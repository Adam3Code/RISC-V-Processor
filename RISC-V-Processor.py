#TODO:1) Finish up implement all thhe instructions: 
#TODO 2) Ensure that is the correct immediate values: 
#TODO 3) Make instructions compute values 
#TODO 4) Make two files when running script 
#TODO 5) Run tests
#TODO 6) Right comments and optimize code

#Global Variables
registers = {f"x{i}": 0 for i in range(32)}
storage_capacity = 1024
data_storage = {}
storage_index = 0
opcode_1 = {'00000': "beq", '00001': "bne", '00010': "blt", '00011': "sw"}
opcode_2 = {'00000': "add", '00001': "sub", "00010": "and", "00011": "or"}
opcode_3 = {'00000': "addi", '00001': "andi", "00010": "ori", "00011": "sll", "00100": 'sra', "00101": 'lw'}
opcode_4 = {'00000': "jal", '11111': "break"}
current_pc = 256
next_pc = 256
file = "sample.txt"
flag = False

#Loading data:

def Load_Data(Instruction_List):
    opcode_break = '11111'

    load_data_index = 0
    byte_size = 4
    pc = 256
    #Folllowing codes is used to find when the break happens
    for i in range(len(Instruction_List)):
        category = Category(Instruction_List[i])
        if category =="Category-4":
            if((Instruction_List[i])[25:30]==opcode_break):
                load_data_index = i+1
                break
    global data_storage 
    address = 0
    for idx, binary_data in enumerate(Instruction_List[load_data_index:]):
        address = (idx+load_data_index)*byte_size+pc
        data_storage[address] = unsigned_bin__to_int(binary_data)



#Optimization: Polymorphism 
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
        self.constant_10 = "" #Maybe remove?
        # Category 4
        self.imm_19_0 = ""
        self.constant_00 = ""
        self.imm_14_0 = ""

    def setCategory1(self, imm_11_5, rs2, rs1, func3, imm_4_0, opcode, constant_11):
        #beq,bne,blt,sw
        self.im_11_5 = imm_11_5
        self.rs2 = rs2
        self.rs1 = rs1
        self.func3 = func3
        self.imm_4_0 = imm_4_0
        self.opcode = opcode
        self.constant_11 = constant_11
        self.imm_14_0 = self.im_11_5+self.imm_4_0

    def setCategory2(self, func7, rs2, rs1, func3, rd, opcode, constant_01):
        #add,sub,and,or
        self.func7 = func7
        self.rs2 = rs2
        self.rs1 = rs1
        self.func3 = func3
        self.rd = rd
        self.opcode = opcode
        self.constant01 = constant_01

    def setCategory3(self, imm_11_0, rs1, func3, rd, opcode, constant_10):
        #addi,andi,ori,sll,sra,lw
        self.imm_11_0 = imm_11_0
        self.rs1 = rs1
        self.func3 = func3
        self.rd = rd
        self.opcode = opcode
        self.constant10 = constant_10

    def setCategory4(self, imm_19_0, rd, opcode, constant_00):
        #jal,break
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
    def get_current_instruction_string(self):
        return self.curr_ins_str
    
##Class ALU
class ALU:
    def __init__(self, instruction: Instruction,compute:bool,pc):
        self.compute = compute
        self.instruction = instruction
        self.flag = flag
        self.pc = pc 

    def setCompute(self,compute:bool):
        self.compute = compute 
    def setFlag(self,flag:bool):
        self.flag = flag
    def setCurrentPC(self,pc):
        self.pc=pc

    def execute(self):
        opcode_name = self.instruction.opcode_name
        method = getattr(self, opcode_name, None)

        if method:
            return method()
        elif opcode_name == 'break':
            return self.break_()
        else:
            print(self.instruction.opcode_name)

    def jal(self):
        rd = f"x{int(self.instruction.rd, 2)}"
        offset = unsigned_bin__to_int(self.instruction.imm_19_0) 
        self.instruction.set_curr_ins_str(f"{self.pc}\tjal {rd}, #{offset}")
        if self.compute:
            registers[rd] = self.pc + 4
            self.pc += offset*2
            print(f'jal pc {self.pc-offset*2}->{self.pc}')
        
    def beq(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rs2 = f"x{int(self.instruction.rs2, 2)}"
        offset = unsigned_bin__to_int(self.instruction.imm_14_0)  # Signed offset
        rs1_value = registers.get(rs1)
        rs2_value = registers.get(rs2)
        self.instruction.set_curr_ins_str(f"{self.pc}\tbeq {rs1}, {rs2}, #{offset}")
        if self.compute:
            if rs1_value == rs2_value:
                self.pc += offset*2
                print(f"beq pc: {self.pc-offset*2} ->{self.pc} and is true")
            else:
                self.pc += 4 
                print(f"beq pc:{self.pc-4} -> {self.pc} and is false")
            

    def blt(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rs2 = f"x{int(self.instruction.rs2, 2)}"
        offset = unsigned_bin__to_int(self.instruction.imm_14_0)  # Signed offset
        rs1_value = registers.get(rs1)
        rs2_value = registers.get(rs2)
        self.instruction.set_curr_ins_str(f"{self.pc}\tblt {rs1}, {rs2}, #{offset}")
        
        if self.compute:
            if rs1_value < rs2_value:
                self.pc += offset*2
                print(f"blt {self.pc-offset*2} ->{self.pc} and is true ")
            else:
                self.pc += 4  # Only move to the next instruction if no branch is taken
                print(f"blt false {self.pc-4} ->{self.pc} and is false ")
    def add(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rs2 = f"x{int(self.instruction.rs2, 2)}"
        rd = f"x{int(self.instruction.rd, 2)}"
        self.instruction.set_curr_ins_str(f"{self.pc}\tadd {rd}, {rs1}, {rs2}")
        
        if (self.compute):
            rs1_value = registers.get(rs1, 0)
            rs2_value = registers.get(rs2, 0)
            result = rs1_value + rs2_value
            registers[rd] = result
            self.pc = self.pc+4
            print(f"add pc: {self.pc-4}->{self.pc}")

    def sub(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rs2 = f"x{int(self.instruction.rs2, 2)}"
        rd = f"x{int(self.instruction.rd, 2)}"
        rs1_value = registers.get(rs1, 0)
        rs2_value = registers.get(rs2, 0)
        self.instruction.set_curr_ins_str(f"{self.pc}\tsub {rd}, {rs1}, {rs2}")
        if self.compute:
            result = rs1_value - rs2_value
            registers[rd] = result
            self.pc = self.pc +4
            print(f"sub pc: {self.pc-4}->{self.pc}")
        

    def addi(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rd = f"x{int(self.instruction.rd, 2)}"
        rs1_value = registers.get(rs1, 0)
        imm_value = int(self.instruction.imm_11_0, 2)
        print("before",self.pc)
        self.instruction.set_curr_ins_str(f"{self.pc}\taddi {rd}, {rs1}, #{imm_value}")
        if self.compute:
            registers[rd] = rs1_value+imm_value
            self.pc = self.pc+4
            print(f'addi pc {self.pc-4} -> {self.pc} and new reg {rd} is {registers.get(rd)}')

    def andi(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rd = f"x{int(self.instruction.rd, 2)}"
        rs1_value = registers.get(rs1, 0)
        imm_value = int(self.instruction.imm_11_0, 2)
        self.instruction.set_curr_ins_str(f"{self.pc}\tandi {rd}, {rs1}, {imm_value}")
        if self.compute:
            registers[rd]=rs1_value&imm_value
            self.pc = self.pc+4
            print(f'and - pc: {self.pc-4}-> {self.pc} and new register is {registers.get(rd)}')

   

    def ori(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rd = f"x{int(self.instruction.rd, 2)}"
        rs1_value = registers.get(rs1, 0)
        imm_value = int(self.instruction.imm_11_0, 2) # might have to sign extension on this
        result = rs1_value | imm_value
        self.instruction.set_curr_ins_str(f"{self.pc}\tori {rd}, {rs1}, {imm_value}")
        if self.compute:
            self.pc = self.pc+4
            registers[rd] = result
            print(f'ori - pc: {self.pc-4}-> {self.pc} and new register is {registers.get(rd)}')
     

    def sll(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rd = f"x{int(self.instruction.rd, 2)}"
        rs1_value = registers.get(rs1, 0)
        imm__11_0 = unsigned_bin__to_int(self.instruction.imm_11_0)
        result = rs1_value << imm__11_0
        self.instruction.set_curr_ins_str(f"{self.pc}\tsll {rd}, {rs1}, #{imm__11_0}")
        if self.compute:
            registers[rd] = result
            self.pc = self.pc+4
        print(f'sll - pc: {self.pc-4}-> {self.pc} and new register {rd} is {registers.get(rd)}')
            


    def sra(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rs2 = f"x{int(self.instruction.rs2, 2)}"
        rd = f"x{int(self.instruction.rd, 2)}"
        rs1_value = registers.get(rs1, 0)
        rs2_value = registers.get(rs2, 0)
        self.instruction.set_curr_ins_str(f"{self.pc}\tsra {rd}, {rs1}, {rs2}")
        if self.compute:
            result = rs1_value >> rs2_value
            registers[rd] = result
            self.pc = self.pc+4
  

    def lw(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rd = f"x{int(self.instruction.rd, 2)}"
        imm_11_0 = unsigned_bin__to_int(self.instruction.imm_11_0)
        address = registers.get(rs1, 0) + imm_11_0
        self.instruction.set_curr_ins_str(f"{self.pc}\tlw, {imm_11_0}({rs1})")
        if self.compute:
            
            result = data_storage[address]
            registers[rd] = result
            self.pc = self.pc+4
            print(f'lw - pc: {self.pc-4}-> {self.pc} and new register {rd} is {registers.get(rd)}')
            

    def sw(self):
        rs1 = f"x{int(self.instruction.rs1, 2)}"
        rs2 = f"x{int(self.instruction.rs2, 2)}"
        rs1_value = registers.get(rs1, 0)
        rs2_value = registers.get(rs2, 0)
        imm_14_0 = unsigned_bin__to_int(self.instruction.imm_14_0)
        offset = imm_14_0
        self.instruction.set_curr_ins_str(f"{self.pc}\tsw {rs1}, {imm_14_0}({rs2})")
        if self.compute:
            data_storage[(rs2_value+imm_14_0)]=rs1_value
            self.pc = self.pc +4

    def break_(self):
        self.instruction.set_curr_ins_str(f"{self.pc}\tbreak")
        self.flag = True 
        self.instruction.setOpcodeName("")

"-------------Helper functions-------------------"
#Read input
def read_input(file_txt):
    with open(file_txt, 'r') as f:
        instructions = [line.strip() for line in f.readlines()]
    return instructions
#Binary using 2's complement
def unsigned_bin__to_int(binary_string):
    binary_list = [int(i) for i in list(binary_string)] 
    res = -binary_list[0] * (2 ** (len(binary_list) - 1)) 
    for i in range(1, len(binary_list)):
        res += binary_list[i] * (2 ** (len(binary_list) - i - 1)) 
    return res
#Merge this with Instruction Object 
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


def Category(binary_input):
    category_map = {
        '11': '1',
        '01': '2',
        '10': '3',
        '00': '4'
    }
    return f"Category-{category_map.get(binary_input[-2:], 'Unknown')}"


# Load Instructions
instructions = read_input(file)
instruction_obj = Instruction()
alu = ALU(instruction_obj, False, current_pc)

log_disassembly = []
log_simulation = []

# Load Data after break instruction
Load_Data(instructions)

# 1. Disassembly Phase
alu.setCurrentPC(256) 
print(instructions[0])

for i, instruction in enumerate(instructions):
    if not alu.flag:  
        decomposition(instruction_obj, instruction)
        alu.execute()
        log_disassembly.append(f'{alu.pc} {instruction} {instruction_obj.get_current_instruction_string()}')
    else:
        log_disassembly.append(f'{alu.pc} {instruction} {unsigned_bin__to_int(instruction)}')
    print(alu.pc,instruction_obj.opcode_name)
    alu.pc +=4

# Disassembly phase
with open("sample_disassembly.txt", "w") as f:
    for entry in log_disassembly:
        f.write(entry + "\n")

#Simulation Phase
alu.setCurrentPC(256)
alu.setFlag(False)
alu.setCompute(True)
registers = {f"x{i}": 0 for i in range(32)}
cycle =1

while True: 
    index = int((alu.pc - 256) / 4)
    decomposition(instruction_obj, instructions[index])
    alu.execute()
    print("cycle", cycle)
    
    # Header output
    sim_output = []
    sim_output.append('-' * 20)  # Divider line
    sim_output.append(f"Cycle {cycle}:\t{instruction_obj.get_current_instruction_string()}")
    
    # Register output
    sim_output.append("Registers")
    for i in range(0, 32, 8):
        register_line = f"x{i:02}:\t" + "\t".join(str(registers[f"x{j}"]) for j in range(i, i + 8))
        sim_output.append(register_line)
    sim_output.append("Data")
    data_addresses = sorted(data_storage.keys())
    for idx in range(0, len(data_addresses), 8):
        addresses_to_print = data_addresses[idx:idx + 8]
        address_line = f"{addresses_to_print[0]}:\t" + "\t".join(
            str(data_storage.get(addr, 0)) for addr in addresses_to_print
        )
        sim_output.append(address_line)
    
    # Add to log
    log_simulation.extend(sim_output)
    if alu.flag:
        break
    
    cycle += 1

# Write to file
with open("sample_simulation.txt", "w") as f:
    for entry in log_simulation:
        f.write(entry + "\n")
