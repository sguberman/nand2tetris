import os
import sys


# VM Code -> Hack Pseudocode => Hack ASM Translations:

# push constant n
#   -> *SP=n, SP++
#   => @n, D=A, @SP, A=M, M=D, @SP, M=M+1

# pop segment i (segment: local->LCL, argument->ARG, object->THIS, array->THAT)
#   -> addr=segment+i, SP--, *addr=*SP
#   => @i, D=A, @segment, D=D+M, @addr, M=D,
#   => @SP, M=M-1, A=M, D=M, @addr, A=M, M=D

# push segment i
#   -> addr=segment+i, *SP=*addr, SP++
#   => @i, D=A, @segment, D=D+M, A=D, D=M, @SP, A=M, M=D, @SP, M=M+1

# pop static i (file Foo.vm)
#   -> SP--, Foo.i=*SP
#   => @SP, M=M-1, A=M, D=M, @Foo.i, M=D

# push static i (file Foo.vm)
#   -> *SP=Foo.i, SP++
#   => @Foo.i, D=M, @SP, A=M, M=D, @SP, M=M+1

# pop temp i (base addr 5)
#   -> addr=5+i, SP--, *addr=*SP
#   => @i, D=A, @5, D=D+A, @addr, M=D, @SP, M=M-1, A=M, D=M, @addr, A=M, M=D

# push temp i (base addr 5)
#   -> addr=5+i, *SP=*addr, SP++
#   => @i, D=A, @5, D=D+A, A=D, D=M, @SP, A=M, M=D, @SP, M=M+1

# pop pointer 0/1
#   -> SP--, THIS/THAT=*SP
#   => @SP, M=M-1, A=M, D=M, @THIS/THAT, M=D

# push pointer 0/1
#   -> *SP=THIS/THAT, SP++
#   => @THIS/THAT, D=M, @SP, A=M, M=D, @SP, M=M+1

# add/sub
#   -> SP--, SP--, D=*SP, SP++, D=D+/-*SP, SP--, *SP=D, SP++
#   => @SP, M=M-1, M=M-1, A=M, D=M, @SP, M=M+1, A=M, D=D+/-M,
#   => @SP, M=M-1, A=M, M=D, @SP, M=M+1

# neg
#   -> SP--, *SP=-*SP, SP++
#   => @SP, M=M-1, A=M, M=-M, @SP, M=M+1

# eq/gt/lt
#   -> take difference of first two on stack and keep in D register
#   -> jump if D eq/gt/lt 0 to set D=-1 (true) otherwise set D=0 (false)
#   -> push D to top of stack
#   -> labels get populated with a unique number (NNNN) during translation
#   =>
"""
@$$ASM.comparisonNNNN.start
0;JMP  // jump to start of this call

($$ASM.comparisonNNNN.true)  // this function gets skipped at first
    D=-1  // it just sets D=-1 (true)
    @$$ASM.comparisonNNNN.callback
    0;JMP  // jump back to call

($$ASM.comparisonNNNN.start)  // call starts here
    @SP
    M=M-1
    A=M
    D=M   // D=stack.pop()
    @SP
    M=M-1
    A=M
    D=M-D  // D=stack.pop()-D
    @$$ASM.comparisonNNNN.true
    D;JEQ/JGT/JLT  // jump to function if true
    D=0  // otherwise false

(@$$ASM.comparisonNNNN.callback)  // jump back here
    @SP
    A=M
    M=D
    @SP
    M=M+1  // push D to stack
"""

# and/or
#   -> SP--, SP--, D=SP*, SP++, D=D&/|SP*, SP--, SP*=D, SP++
#   => @SP, M=M-1, M=M-1, A=M, D=M, @SP, M=M+1, A=M, D=D&/|M,
#   => @SP, M=M-1, A=M, M=D, @SP, M=M+1

# not
#   -> SP--, *SP=!*SP, SP++
#   => @SP, M=M-1, A=M, M=!M, @SP, M=M+1


class VMTranslator:

    def __init__(self, filename):
        self.filename = filename

    @staticmethod
    def skip_comments_and_whitespace(fileobj):
        for line_number, line in enumerate(fileobj):
            instruction = line.split('//')[0].strip()
            if not instruction:
                continue
            yield instruction, line_number

    @staticmethod
    def comment_string(name, line_number=None):
        leader = '//'
        if line_number is None:
            numtext = ' '
        else:
            numtext = ' {}: '.format(line_number)
        return '{}{}{}'.format(leader, numtext, name)

    @classmethod
    def push(cls, segment, i, line_number=None):
        name = 'push {} {}'.format(segment, i)
        comment = cls.comment_string(name, line_number)
        assembly = '@{}, D=A, @SP, A=M, M=D, @SP, M=M+1'.format(i).split(', ')
        return [comment] + assembly

    @classmethod
    def pop(cls, segment, i, line_number=None):
        raise NotImplementedError

    @classmethod
    def add(cls, line_number=None):
        comment = cls.comment_string('add', line_number)
        assembly = ('@SP, M=M-1, M=M-1, A=M, D=M, @SP, M=M+1, A=M, D=D+M, '
                    '@SP, M=M-1, A=M, M=D, @SP, M=M+1').split(', ')
        return [comment] + assembly

    @classmethod
    def sub(cls, line_number=None):
        comment = cls.comment_string('sub', line_number)
        assembly = ('@SP, M=M-1, M=M-1, A=M, D=M, @SP, M=M+1, A=M, D=D-M, '
                    '@SP, M=M-1, A=M, M=D, @SP, M=M+1').split(', ')
        return [comment] + assembly

    @classmethod
    def parse(cls, line, line_number=None):
        commands = {
            'push': cls.push,
            'add': cls.add,
        }
        command, *args = line.split()
        return commands[command](*args, line_number)

    def translate(self):
        infile = self.filename
        outfile = os.path.splitext(infile)[0] + '.asm'
        with open(infile, 'r') as i, open(outfile, 'w') as o:
            instructions = self.skip_comments_and_whitespace(i)
            for instruction in instructions:
                for step in self.parse(*instruction):
                    o.write(step + '\n')


if __name__ == '__main__':
    translator = VMTranslator(sys.argv[1])
    translator.translate()

