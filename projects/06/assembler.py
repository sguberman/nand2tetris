import os
import sys


class SymbolTable:

    def __init__(self):
        self.d = {
            'SP':       0,
            'LCL':      1,
            'ARG':      2,
            'THIS':     3,
            'THAT':     4,
            'SCREEN':   16384,
            'KBD':      24576,
        }
        
        for i in range(16):
            label = 'R{}'.format(i)
            self.d[label] = i
        
        self.address = 15

    def new_address(self, label):
        self.address += 1
        self.set(label, self.address)
        return self.address

    def set(self, label, address):
        self.d[label] = address

    def get(self, label):
        try:
            return self.d[label]
        except KeyError:
            return self.new_address(label)


class Assembler:

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

    @staticmethod
    def skip_comments_and_whitespace(fileobj):
        for line in fileobj:
            instruction = line.split('//')[0].strip()
            if not instruction:
                continue
            yield instruction
    
    @staticmethod
    def parse_labels(instructions):
        symbols = SymbolTable()
        line_counter = 0
        program = []
        for instruction in instructions:
            if instruction.startswith('('):
                symbols.set(instruction[1:-1], line_counter)
            else:
                line_counter += 1
                program.append(instruction)
        return program, symbols
    
    @classmethod
    def first_pass(cls, fileobj):
        instructions = cls.skip_comments_and_whitespace(fileobj)
        return cls.parse_labels(instructions)
    
    @classmethod
    def translate(cls, program, symbols):
        for command in program:
            if command.startswith('@'):
                symbol = command[1:]
                try:
                    address = int(symbol)
                except ValueError:
                    address = symbols.get(symbol)
                yield cls.a_command(address)
            else:
                *dest, rhs = command.split('=')
                comp, *jump = rhs.split(';')
                yield cls.c_command(comp, dest, jump)

    @staticmethod
    def a_command(number):
        return '0{:015b}'.format(number)

    @classmethod
    def c_command(cls, comp, dest=None, jump=None):
        dest = '' if not dest else dest[0]
        jump = '' if not jump else jump[0]
        return '111{}{}{}'.format(cls.COMP[comp], cls.DEST[dest], cls.JUMP[jump])
    
    @classmethod
    def assemble(cls, infile):
        outfile = os.path.splitext(infile)[0] + '.hack'
        with open(infile, 'r') as i, open(outfile, 'w') as o:
            for line in cls.translate(*cls.first_pass(i)):
                o.write(line + '\n')


if __name__ == '__main__':
    Assembler.assemble(sys.argv[1])

