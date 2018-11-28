class VM:
    def __init__(self, code, target):
        self.code = code
        self.target = target

vm_list = []
registers = [0]*16
file_eof = False
flag = False #nenaudojama
is_machine_running = True

def read_binary(path):
    f = open(path, "rb")
    while True:
        code = f.read(1)
        target = f.read(1)

        if code == b"" or target == b"":
            break

        vm = VM(int(hex(ord(code)), 16), int(hex(ord(target)), 16))
        vm_list.append(vm)

def calculate_registers(target):
    xreg = target & 0x0F
    yreg = (target & 0xF0) >> 4
    return xreg, yreg

read_binary("decryptor.bin")
data = open("q1_encr.txt", "r")
marker = 0
while is_machine_running:
    
    marker = marker % 16

    code = vm_list[marker].code
    target = vm_list[marker].target

    rx, ry = calculate_registers(target)
    
    #INC
    if code == 0x01:
        registers[rx] += 1

    #DEC
    if code == 0x02:
        registers[rx] -= 1

    #MOV
    if code == 0x03:
        registers[rx] = registers[ry]

    #MOVC
    if code == 0x04:
        registers[rx] += 0

    #LSL
    if code == 0x05:
        registers[rx] = registers[rx] >> 1

    #LSR
    if code == 0x06:
        registers[rx] = registers[rx] << 1

    #JMP
    if code == 0x07:
        marker += 4
        continue

    #JZ
    if code == 0x08:
        if flag == True:
            marker += 4
            continue

    #JNZ
    if code == 0x09:
        if flag == False:
            marker += 4
            continue
    
    #JFE
    if code == 0x0A:
        if file_eof == True:
            marker += 4
            continue

    #RET
    if code == 0x0B:
        is_machine_running = False
        continue
    
    #ADD
    if code == 0x0C:
        registers[rx] = registers[rx] + registers[ry]
    
    #SUB
    if code == 0x0D:
        registers[rx] = registers[rx] - registers[ry]

    #XOR
    if code == 0x0E:
        registers[rx] = registers[rx] ^ registers[ry]
    
    #OR
    if code == 0x0F:
        registers[rx] = registers[rx] | registers[ry]

    #IN 
    if code == 0x10:
        c = data.read(1) #should try adding if this doesn't work
        if not c:
            file_eof = True
        else:
            registers[rx] += ord(c)
        
    #OUT
    if code == 0x11:
        print(chr(registers[rx]), end="")

    marker += 1

    print(registers, sep=" ", end="\n")