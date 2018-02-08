import os
import sys

from collections import defaultdict
from string import Template


# VM Code -> Hack Pseudocode => Hack ASM Translations:

# push constant i
#   -> *SP=i, SP++
#   => @i, D=A, @SP, A=M, M=D, @SP, M=M+1
push_constant = Template(  # i, line, line_number
"""
// ${line_number}: $line
@$i
D=A
@SP
A=M
M=D  // *SP=$i
@SP
M=M+1  // SP++
"""
)

# push segment i (segment: local->LCL, argument->ARG, this->THIS, that->THAT)
#   -> addr=segment+i, *SP=*addr, SP++
#   => @i, D=A, @segment, D=D+M, A=D, D=M, @SP, A=M, M=D, @SP, M=M+1
push_latt = Template(  # i, segment, line, line_number
"""
// ${line_number}: $line
@$i
D=A
@$segment
D=D+M  // addr=${segment}+$i
A=D
D=M
@SP
A=M
M=D  // *SP=*addr
@SP
M=M+1  // SP++
"""
)

# pop segment i
#   -> addr=segment+i, SP--, *addr=*SP
#   => @i, D=A, @segment, D=D+M, @addr, M=D,
#   => @SP, M=M-1, A=M, D=M, @addr, A=M, M=D
pop_latt = Template(  # i, segment, line, line_number
"""
// ${line_number}: $line
@$i
D=A
@$segment
D=D+M
@addr
M=D  // addr=${segment}+$i
@SP
M=M-1  // SP--
A=M
D=M
@addr
A=M
M=D  // *addr=*SP
"""
)

# push static i (file Foo.vm)
#   -> *SP=Foo.i, SP++
#   => @Foo.i, D=M, @SP, A=M, M=D, @SP, M=M+1
push_static = Template(  # i, filename, line, line_number
"""
// ${line_number}: $line
@${filename}.static.$i
D=M
@SP
A=M
M=D  // *SP=${filename}.static.$i
@SP
M=M+1  // SP++
"""
)

# pop static i (file Foo.vm)
#   -> SP--, Foo.i=*SP
#   => @SP, M=M-1, A=M, D=M, @Foo.i, M=D
pop_static = Template(  # i, filename, line, line_number
"""
// ${line_number}: $line
@SP
M=M-1  // SP--
A=M
D=M
@${filename}.static.$i
M=D  // ${filename}.static.${i}=*SP
"""
)

# push temp i (base addr 5)
#   -> addr=5+i, *SP=*addr, SP++
#   => @i, D=A, @5, D=D+A, A=D, D=M, @SP, A=M, M=D, @SP, M=M+1
push_temp = Template(  # i, line, line_number
"""
// ${line_number}: $line
@$i
D=A
@5
D=D+A  // addr=5+$i
A=D
D=M
@SP
A=M
M=D  // *SP=*addr
@SP
M=M+1  // SP++
"""
)

# pop temp i (base addr 5)
#   -> addr=5+i, SP--, *addr=*SP
#   => @i, D=A, @5, D=D+A, @addr, M=D, @SP, M=M-1, A=M, D=M, @addr, A=M, M=D
pop_temp = Template(  # i, line, line_number
"""
// ${line_number}: $line
@$i
D=A
@5
D=D+A
@addr
M=D  // addr=5+$i
@SP
M=M-1  // SP--
A=M
D=M
@addr
A=M
M=D  // *addr=*SP
"""
)

# push pointer 0/1
#   -> *SP=THIS/THAT, SP++
#   => @THIS/THAT, D=M, @SP, A=M, M=D, @SP, M=M+1
push_pointer = Template(  # this_that, line, line_number
"""
// ${line_number}: $line
@$this_that
D=M
@SP
A=M
M=D  // *SP=$this_that
@SP
M=M+1  // SP++
"""
)

# pop pointer 0/1
#   -> SP--, THIS/THAT=*SP
#   => @SP, M=M-1, A=M, D=M, @THIS/THAT, M=D
pop_pointer = Template(  # this_that, line, line_number
"""
// ${line_number}: $line
@SP
M=M-1  // SP--
A=M
D=M
@$this_that
M=D  // ${this_that}=*SP
"""
)

# add/sub
#   -> SP--, SP--, D=*SP, SP++, D=D+/-*SP, SP--, *SP=D, SP++
#   => @SP, M=M-1, M=M-1, A=M, D=M, @SP, M=M+1, A=M, D=D+/-M,
#   => @SP, M=M-1, A=M, M=D, @SP, M=M+1
add_sub = Template(  # plus_minus, line, line_number
"""
// ${line_number}: $line
@SP
M=M-1  // SP--
M=M-1  // SP--
A=M
D=M  // D=*SP
@SP
M=M+1  // SP++
A=M
D=D{$plus_minus}M  // D=D{$plus_minus}*SP
@SP
M=M-1  // SP--
A=M
M=D  // *SP=D
@SP
M=M+1  // SP++
"""
)

# neg
#   -> SP--, *SP=-*SP, SP++
#   => @SP, M=M-1, A=M, M=-M, @SP, M=M+1
neg = Template(  # line, line_number
"""
// ${line_number}: $line
@SP
M=M-1  // SP--
A=M
M=-M  // *SP=-*SP
@SP
M=M+1  // SP--
"""
)

# eq/gt/lt
#   -> take difference of first two on stack and keep in D register
#   -> jump if D eq/gt/lt 0 to set D=-1 (true) otherwise set D=0 (false)
#   -> push D to top of stack
#   -> labels get populated with a unique number (line_number) during translation
eq_gt_lt = Template(  # jeq_jgt_jlt, line, line_number
"""
// ${line_number}: $line
@$$ASM.COMPARE.${line_number}.START
0;JMP  // jump to start of this call

($$ASM.COMPARE.${line_number}.TRUE)  // this branch gets skipped at first
    D=-1  // it just sets D=-1 (true)
    @$$ASM.COMPARE.${line_number}.END
    0;JMP  // jump back to call

($$ASM.COMPARE.${line_number}.START)  // call starts here
    @SP
    M=M-1
    A=M
    D=M   // pop -> D
    @SP
    M=M-1
    A=M
    D=M-D  // pop-D -> D
    @$$ASM.COMPARE.${line_number}.TRUE
    D;$jeq_jgt_jlt  // jump to function if true
    D=0  // otherwise false

($$ASM.COMPARE.${line_number}.END)  // jump back here
    @SP
    A=M
    M=D
    @SP
    M=M+1  // push D to stack
"""
)

# and/or
#   -> SP--, SP--, D=*SP, SP++, D=D&/|*SP, SP--, *SP=D, SP++
#   => @SP, M=M-1, M=M-1, A=M, D=M, @SP, M=M+1, A=M, D=D&/|M,
#   => @SP, M=M-1, A=M, M=D, @SP, M=M+1
and_or = Template(  # amper_pipe, line, line_number
"""
// ${line_number}: $line
@SP
M=M-1  // SP--
M=M-1  // SP--
A=M
D=M  // D=*SP
@SP
M=M+1  // SP++
A=M
D=D${amper_pipe}M  // D=D${amper_pipe}*SP
@SP
M=M-1  // SP--
A=M
M=D  // *SP=D
@SP
M=M+1  // SP++
"""
)

# not
#   -> SP--, *SP=!*SP, SP++
#   => @SP, M=M-1, A=M, M=!M, @SP, M=M+1
not_ = Template(  # line, line_number
"""
// ${line_number}: $line
@SP
M=M-1  // SP--
A=M
M=!M  // *SP=!*SP
@SP
M=M+1  // SP++
"""
)


class VMTranslator:

    def __init__(self, filename):
        self.filename = filename
        self.classname = os.path.splitext(os.path.basename(filename))[0]

    @staticmethod
    def extract_instructions(fileobj):
        for line_number, line in enumerate(fileobj):
            instruction = line.split('//')[0].strip()
            if not instruction:
                continue
            yield instruction, line_number

    def parse(self, line, line_number=None):
        commands = {
            'push': self.push,
            'pop': self.pop,
            'add': self.add,
            'sub': self.sub,
            'neg': self.neg,
            'eq': self.eq,
            'gt': self.gt,
            'lt': self.lt,
            'and': self.and_,
            'or': self.or_,
            'not': self.not_,
        }
        command, *args = line.split()
        return commands[command](*args, line, line_number)

    def translate(self):
        infile = self.filename
        outfile = os.path.splitext(infile)[0] + '.asm'
        with open(infile, 'r') as i, open(outfile, 'w') as o:
            instructions = self.extract_instructions(i)
            for instruction in instructions:
                o.write(self.parse(*instruction))


if __name__ == '__main__':
    translator = VMTranslator(sys.argv[1])
    translator.translate()

