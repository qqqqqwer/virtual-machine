def INC(rx):
    rx+= 1
def DEC(rx):
    rx+= -1
def MOV(rx, ry):
    rx = ry
def MOVC(const, r0):
    r0 = const
def LSL(rx):
    rx[len(rx) - 1] = 0 
    for i in range(len(rx) - 2, 0):
        rx[i - 1] = rx[i]
def LSR(rx):
    rx[0] = 0
    for i in range(1, len()):
        rx[i + 1] = rx[i]
def JMP(addr):
    addr += 8
def JZ(addr, condition):
    if condition == True:
        addr += 8
def JNZ(addr, condition):
    if condition == False:
        addr += 8
def JFE(addr, condition):
    if (condition == True):
        addr += 8
def RET():
    None
def ADD(rx, ry):
    rx = rx + ry
def SUB(rx, ry):
    rx = rx - ry
def XOR(rx, ry):
    rx = rx^ry
def OR(rx, ry):
    rx = rx | ry
def IN(f, flag):
    None
def OUT(rx):
    None