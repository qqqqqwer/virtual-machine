import numpy as np
import functions as fun

class VM:
    def __init__(self, code, target):
        self.code = code
        self.target = target


vm_list = []
registers = [0]*16
marker = 0
file_eof = False
flag = False #nenaudojama

def read_binary(path):
    f = open(path, "rb")
    while True:
        code = f.read(1)
        target = f.read(1)

        if code == b"" or target == b"":
            break

        vm = VM(hex(ord(code)), hex(ord(target)))
        vm_list.append(vm)

def calculate_registers(target):
    xreg = target & 0x0F
    yreg = target & 0xF0
    return xreg, yreg

def select_function(code, rx, ry, r0, marker, file_eof, flag):
    if code == 0x01:
        fun.INC(rx)
    elif code == 0x02:
        fun.DEC(rx)
    elif code == 0x03:
        fun.MOV(rx, ry)
    elif code == 0x04:
        fun.MOVC(8, r0)
    elif code == 0x05:
        fun.LSL(rx)
    elif code == 0x06:
        fun.LSR(rx)
    elif code == 0x07:
        fun.JMP(marker)
    elif code == 0x08:
        fun.JZ(marker, flag)
    elif code == 0x09:
        fun.JNZ(marker, flag)
    elif code == 0x0A:
        fun.JFE(marker, file_eof)
    elif code == 0x0B:
        fun.RET()
    elif code == 0x0C:
        fun.ADD(rx, ry)
    elif code == 0x0D:
        fun.SUB(rx, ry)
    elif code == 0x0E:
        fun.XOR(rx, ry)
    elif code == 0x0F:
        fun.OR(rx, ry)
    elif code == 0x10:
        fun.IN(rx, file_eof)
    elif code == 0x11:
        fun.OUT(ry)


read_binary("decryptor.bin")
data = open("q1_encr.txt", "r")

for v in vm_list:
    print(v.code, v.target, sep=" ", end = " ")