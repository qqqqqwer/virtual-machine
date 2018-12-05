import numpy as np

#klase komandoms saugoti. Turi komandos koda ir skaiciu salia komandos
class VM:
    def __init__(self, code, target):
        self.code = code
        self.target = target

vm_list = [] #komandu masyvas
registers = [0]*16 #registrai
file_eof = False # failo pabaigos flagas
flag = False #nenaudojamas flagas 
is_machine_running = True #booleanas kuris pasako kada masina turi nutraukti darba

#nuskaitomas binary komandu failas i komandu masyba
def read_binary(path):
    f = open(path, "rb")
    while True:
        code = f.read(1)
        target = f.read(1)

        if code == b"" or target == b"":
            break

        vm = VM(int(hex(ord(code)), 16), int(hex(ord(target)), 16))
        vm_list.append(vm)

#apskaiciuojami rx ir ry registrai
def calculate_registers(target):
    xreg = target & 0x0F
    yreg = (target & 0xF0) >> 4
    return xreg, yreg


read_binary("decryptor.bin") #kvieciami binary skaitymo funckija
data = open("q1_encr.txt", "r") #atidaromas duomenu failas
marker = 0 #pozicija komandu masyve

#programa tol vykdo darba kol nera pakeistas is_machine_true booleanas. Ji pakeis RET komanda.
while is_machine_running:
    
    marker = int(marker) 

    code = vm_list[marker].code #komandos kodas
    target = np.int8(vm_list[marker].target) #skaicius salia komandos
    rx, ry = calculate_registers(target) #registrai
    
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
        registers[0] += target

    #LSL
    if code == 0x05:
        registers[rx] = registers[rx] << 1

    #LSR
    if code == 0x06:
        registers[rx] = registers[rx] >> 1

    #JMP (visose jump tipo komandose dalinam jumpo dydi is dvieju nes komandu masyvo elementas saugo 2 dalykus. 
    #Taigi su vienu suoliu mes pereinam per du dalykus. Todel reikia dalinti jumpo dydi is dvieju.)
    if code == 0x07:
        marker += target / 2
        continue

    #JZ
    if code == 0x08:
        if flag == True:
            marker += target / 2
            continue

    #JNZ
    if code == 0x09:
        if flag == False:
            marker += target / 2
            continue
    
    #JFE
    if code == 0x0A:
        if file_eof == True:
            marker += target / 2
            continue

    #RET
    if code == 0x0B:
        is_machine_running = False
    
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
        c = data.read(1) #nuskaitom viena simboli
        if file_eof == False: #jeigu failas nera failo pabaigos flago vykdom toliau esancius ifus
            if c == "": #jeigu simbolis tuscias failas basibaige
                file_eof = True #pakeiciam flaga
            else: #kitu atveju issaugom simbolio int reiskme atitinkamame registre
                registers[rx] = ord(c)
        
    #OUT
    if code == 0x11:
        print(chr(registers[rx]), end="")

    #Paeinam vienu i prieki kad vykdyti kita komanda. 
    #Isskyrus tuos atvejus kai yra jump komandos. Jump komandos po pozicijos pakeitimo naudoja continue keyworda kuris neleidzia prieiti sitos vietos
    marker += 1