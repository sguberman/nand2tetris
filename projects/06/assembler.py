import os
import sys


COMP = {  # C-Instruction Table
    '0':    '0101010',
    '1':    '0111111',
    '-1':   '0111010',
    'D':    '0001100',
    'A':    '0110000',  'M':    '1110000',
    '!D':   '0001101',
    '!A':   '0110001',  '!M':   '1110001',
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


def ignore_comments_and_whitespace(fileobj):
    for line in fileobj:
        instruction = line.split('//')[0].strip()
        if not instruction:
            continue
        yield instruction


def replace_symbols(instructions):
    for instruction in instructions:
        yield instruction


def translate(instructions):
    for instruction in instructions:
        if instruction.startswith('@'):
            yield a_command(instruction[1:])
        else:
            *dest, rhs = instruction.split('=')
            comp, *jump = rhs.split(';')
            yield c_command(comp, dest, jump)


def a_command(number):
    return '0{:015b}'.format(int(number))


def c_command(comp, dest=None, jump=None):
    dest = '' if not dest else dest[0]
    jump = '' if not jump else jump[0]
    return '111{}{}{}'.format(COMP[comp], DEST[dest], JUMP[jump])


if __name__ == '__main__':
    assemblyfile = sys.argv[1]
    hackfile = os.path.splitext(assemblyfile)[0] + '.hack'
    with open(hackfile, 'w') as h, open(assemblyfile, 'r') as a:
        instructions_only = replace_symbols(ignore_comments_and_whitespace(a))
        for instruction in translate(instructions_only):
            h.write(instruction + '\n')

