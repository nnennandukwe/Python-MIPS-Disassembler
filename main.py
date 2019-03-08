

# MIPS DISASSEMBLER 

# Input will be 32-bit instructions that a compiler or assembler produces
# program figures out what the original source instructions were that created those 32-bit machine instructions
# and outputs them.

enc = "utf-8"

import sys

from formats.r_format import RFormat
from formats.i_format import IFormat

def main():
	with open('ins', 'r') as f:
		for line in f:
			sep = list(line) # separate each hex digit into list element
			s = int(line, 16) # convert str to short int

			if int(sep[2],16) == 0: # opcode check for r-format

				r = RFormat() # initialize new r-format object

				r.ins = s # set instruction
				r.opcode = (s & r.R_MASKS["opcode"]) >> (32-6)
				r.src1 = (s & r.R_MASKS["s1"]) >> 21
				r.src2 = (s & r.R_MASKS["s2"]) >> 16
				r.dest = (s & r.R_MASKS["dest"]) >> 11
				r.shamt = (s & r.R_MASKS["shamt"]) >> 6

				func = (s & r.R_MASKS["func"]) # preliminary func

				# find correct matching function
				for option in r.func_options.keys():
					if func == option:
						# set function in instruction object
						r.func = r.func_options[func]

				# format and print out full instruction
				print(r.full_ins())

			else:
				
				i = IFormat() # initialize new i-format object

				i.ins = s # set instruction
				i.opcode = (s & i.I_MASKS["opcode"]) >> (32-6)
				i.src1 = (s & i.I_MASKS["s1"]) >> 21
				i.dest_src = (s & i.I_MASKS["ds"]) >> 16
				i.offset = (s & i.I_MASKS["off"])

				# find correct matching operation
				for op in i.ops.keys():
					if i.opcode == op:
						# set string equivalent instruction (e.g. "lw", "sw")
						i.op = i.ops[i.opcode]

				# check for branch operations
				if (i.op == i.ops[0x4]) or (i.op == i.ops[0x5]): # beq or bne
					print(i.full_ins(branch=True)) # print with branch formatting
				
				# sign offset if instruction is lw or sw
				elif (i.op == i.ops[0x23]) or (i.op == i.ops[0x2b]):
					i.offset = i.signed_offset()
					# format and print out full instruction
					print(i.full_ins())


if __name__=='__main__':
	main()
