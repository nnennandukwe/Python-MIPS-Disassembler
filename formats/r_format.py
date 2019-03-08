

class RFormat():

    R_MASKS = {
        "opcode":0b11111100000000000000000000000000,
        "s1"    :0b00000011111000000000000000000000,
        "s2"    :0b00000000000111110000000000000000,
        "dest"  :0b00000000000000001111100000000000,
        "shamt" :0b00000000000000000000011111000000,
        "func" 	:0b00000000000000000000000000111111,
    }

    def __init__(
        self,
        ins=None,
        opcode=None,
        func=None,
        src1=None,
        src2=None,
        shamt=None,
        dest=None,
    ):
    
        self.opcode = opcode
        self.ins = ins # pure instruction
        self.func = func # str e.g. "sub" or "add"
        self.src1 = src1
        self.src2 = src2
        self.dest = dest
        self.shamt = shamt

        self.func_options = {
            0x22:"sub",
            0x20:"add",
            0x24:"and",
            0x25:"or",
        }

    def as_hex(self):
        return hex(self.ins)


    def format(self):
        return (
            f"{self.func} ${self.dest}, "
            f"${self.src1}, ${self.src2}"
        )


    def full_ins(self):
        return f'{self.as_hex()}  {self.format()}'
