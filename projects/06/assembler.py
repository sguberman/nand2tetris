import sys


COMP = {  # C-Instruction Table
    '0':    '0101010',
    '1':    '0111111',
    '-1':   '0111010',
    'D':    '0001100',
    'A':    '0110000',  'M':    '111000',
    '!D':   '0001101',
    '!A':   '0110001',  '!A':   '1110001',
    '-D':   '0001111',
    '-A':   '0110011',  '-A':   '1110011',
    'D+1':  '0011111',
    'A+1':  '0110111',  'M+1':  '1110111',
    'D-1':  '0001110',
    'A-1':  '0110010',  'M-1':  '1110010',
    'D+A':  '0000010',  'D+M':  '1000010',
    'D-A':  '0010011',  'D-M':  '1010011',
    'A-D':  '0000111',  'M-D':  '1000111',
    'D&A':  '0000000',  'D&M':  '1000000',
    'D|A':  '0010101',  'D|M':  '1010101',
}

DEST = {  # Destination Table
    '':     '000',
    'M':    '001',
    'D':    '010',
    'MD':   '011',
    'A':    '100',
    'AM':   '101',
    'AD':   '110',
    'AMD':  '111',
}

JUMP = {  # Jump Table
    '':     '000',
    'JGT':  '001',
    'JEQ':  '010',
    'JGE':  '011',
    'JLT':  '100',
    'JNE':  '101',
    'JLE':  '110',
    'JMP':  '111',
}

def parser(filename):
    with open(filename) as f:
        for line in f:
            instruction = line.split('//')[0].strip()
            if not instruction:
                continue
            if instruction.startswith('@'):
                yield ('A_COMMAND', instruction[1:])
            elif instruction.startswith('('):
                yield ('L_COMMAND', instruction[1:-1])
            else:
                *dest, rhs = instruction.split('=')
                comp, *jump = rhs.split(';')
                yield ('C_COMMAND', *dest, comp, *jump)


if __name__ == '__main__':
    filename = sys.argv[1]
    with open('output', 'w') as o:
        for line in parser(filename):
            o.write(str(line) + '\n')

