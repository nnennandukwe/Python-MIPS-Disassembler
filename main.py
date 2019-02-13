# MIPS DISASSEMBLER 

# Input will be 32-bit instructions that a compiler or assembler produces
# program figures out what the original source instructions were that creatd those 32-bit machine instructions
# and outputs them.

# All Instructions that Must be able to be disassembld are:
# add, sub, and, or, slt, lw, sw, beq, bne
enc = "utf-8"
import sys
from helpers import R_MASKS, I_MASKS

# disassemble(32-bit int instruction) -> Instruction (string)

def zk(zahl): # 16 bit immedieates, calculate 2-compliment
	msb = zahl >> 15 # most significant bit, indicates if negative or positiv
	if(msb==0):
		return zahl
	else:
		return -2**16 + ((zahl << 1) >> 1)


def disassemble(instruction, pc):
	command = ""
	a = instruction
	opcode = (a & 0b11111100000000000000000000000000) >> (32-6) #get opcode

    if opcode == 0: # Rtype instruction
		fcode = a & R_MASKS["funct"] # get functioncode
        rs = registers[(a & R_MASKS["rs"]) >> 21]
        rt = registers[(a & R_MASKS["rt"]) >> 16]
        rd = registers[(a & R_MASKS["rd"]) >> 11]
        if(fcode==0 or fcode==2 or fcode==3): # shift instructions
            shamd = (a & R_MASKS["shamd"]) >> 6
            return fcodes[fcode] + " " + rd + "," + rt + "," + str(shamd)
        else:
            return fcodes[fcode] + " " + rd + "," + rs + "," + rt

	elif (opcode == 1):
		rt = (a & 0b00000000000111110000000000000000) >> 16
		rs = registers[(a & 0b00000011111000000000000000000000) >> 21]
		imm = (a & I_MASKS["imm"])
		if(rt==0): # depends on rt
			return "bltz " + rs + "," + str(hex(imm))
		elif(rt==1):
			return "bgez " + rs + "," + str(hex(imm))

	elif (opcode == 32 or opcode == 35 or opcode == 40 or opcode== 43): # lw lb sb sw
		rt = registers[(a & 0b00000000000111110000000000000000) >> 16]
		rs = registers[(a & 0b00000011111000000000000000000000) >> 21]
		imm = (a & I_MASKS["imm"])
		if(imm>=0x8000):
			return  opcodes[opcode] + " " + rt + "," + str(hex(imm)) + "(" + rs + ")"
		else:
			return opcodes[opcode] + " " + rt + "," + str(zk(imm)) + "(" + rs + ")"

	else:
		rs  = registers[(a & I_MASKS["rs"]) >> 21]
		rt  = registers[(a & I_MASKS["rt"]) >> 16]
		imm = (a & I_MASKS["imm"]) # 4*off + 4
		if(opcode==4 or opcode==5 or opcode ==6 or opcode==7):# if we got branches, the offset has to be called
			return opcodes[opcode]  + " " + rt + "," + rs + "," + str(hex(imm*4+4+pc))
		return opcodes[opcode] + " " + rt + "," + rs + "," + str(zk(imm))


def main():
    with open('instructions', 'r') as f:
        for line in f:
            print(line)
            n = line.split(' ')
            x = n[1].split('0x')[1]
            m = n[0].split('0x')[1]
            print(n[0] + " " + disassemble(int(x,16),int(m,16)))

if __name__=='__main__':
    main()
