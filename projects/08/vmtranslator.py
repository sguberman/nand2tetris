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
D=D${plus_minus}M  // D=D${plus_minus}*SP
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
eq_gt_lt = Template(  # jeq_jgt_jlt, name, line, line_number
"""
// ${line_number}: $line
@$$ASM.COMPARE.${name}.${line_number}.START
0;JMP  // jump to start of this call

($$ASM.COMPARE.${name}.${line_number}.TRUE)  // skipped at first
    D=-1  // it just sets D=-1 (true)
    @$$ASM.COMPARE.${name}.${line_number}.END
    0;JMP  // jump back to call

($$ASM.COMPARE.${name}.${line_number}.START)  // call starts here
    @SP
    M=M-1
    A=M
    D=M   // pop -> D
    @SP
    M=M-1
    A=M
    D=M-D  // pop-D -> D
    @$$ASM.COMPARE.${name}.${line_number}.TRUE
    D;$jeq_jgt_jlt  // jump to function if true
    D=0  // otherwise false

($$ASM.COMPARE.${name}.${line_number}.END)  // jump back here
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

# label name
#   => (function$name)
label = Template(  # name, line, line_number
"""
// ${line_number}: $line
(${name})
"""
)

# goto name
#   => @function.$name, 0;JMP
goto = Template(  # name, line, line_number
"""
// ${line_number}: $line
@${name}
0;JMP
"""
)

# if-goto name
#   -> D=stack.pop(), A=name, jump iff D!=0
#   => @SP, M=M-1, A=M, D=M, @function.$name, D;JNE
if_goto = Template(  # name, line, line_number
"""
// ${line_number}: $line
@SP
M=M-1
A=M
D=M
@${name}
D;JNE
"""
)


class VMTranslator:

    arithmetic = {  # name: (template, kwargs)
        'add': (add_sub, {'plus_minus': '+'}),
        'sub': (add_sub, {'plus_minus': '-'}),
        'neg': (neg, {}),
        'eq':  (eq_gt_lt, {'jeq_jgt_jlt': 'JEQ'}),
        'gt':  (eq_gt_lt, {'jeq_jgt_jlt': 'JGT'}),
        'lt':  (eq_gt_lt, {'jeq_jgt_jlt': 'JLT'}),
        'and': (and_or, {'amper_pipe': '&'}),
        'or':  (and_or, {'amper_pipe': '|'}),
        'not': (not_, {}),
    }

    stack = {
        'push': {
            'constant': push_constant,
            'local': push_latt,
            'argument': push_latt,
            'this': push_latt,
            'that': push_latt,
            'static': push_static,
            'temp': push_temp,
            'pointer': push_pointer,
        },
        'pop': {
            'local': pop_latt,
            'argument': pop_latt,
            'this': pop_latt,
            'that': pop_latt,
            'static': pop_static,
            'temp': pop_temp,
            'pointer': pop_pointer,
        },
   }

    segments = defaultdict(str, {
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT',
    })

    pointers = defaultdict(str, {'0': 'THIS', '1': 'THAT'})

    branch = {
        'label': label,
        'goto': goto,
        'if-goto': if_goto,
    }

    def __init__(self, filename='None.vm'):
        self.classname = os.path.splitext(os.path.basename(filename))[0]
        self.funcname = '{}.None'.format(self.classname)

    @staticmethod
    def extract_instructions(fileobj):
        for line_number, line in enumerate(fileobj):
            instruction = line.split('//')[0].strip()
            if not instruction:
                continue
            yield instruction, line_number

    def parse(self, line, line_number=None):
        command, *args = line.split()
        if command in ('push', 'pop'):
            return self._stack(command, *args, line, line_number)
        elif command in ('label', 'goto', 'if-goto'):
            return self._branch(command, *args, line, line_number)
        else:
            return self._arithmetic(command, line, line_number)

    def _arithmetic(self, command, line, line_number):
        template, kwargs = self.arithmetic[command]
        kwargs.update(line=line, line_number=line_number, name=self.funcname)
        return template.substitute(kwargs)

    def _stack(self, command, segment, i, line, line_number):
        template = self.stack[command][segment]
        kwargs = {
            'segment': self.segments[segment],
            'filename': self.classname,
            'this_that': self.pointers[i],
            'i': i,
            'line': line,
            'line_number': line_number,
        }
        return template.substitute(kwargs)

    def _branch(self, command, name, line, line_number):
        template = self.branch[command]
        kwargs = {
            'name': '{}${}'.format(self.funcname, name),
            'line': line,
            'line_number': line_number,
        }
        return template.substitute(kwargs)

    @classmethod
    def translate(cls, filepath):
        try:
            vmfiles = [os.path.abspath(fn) for fn in os.listdir(filepath)
                       if fn.endswith('.vm')]  # TODO: fix bug here
        except NotADirectoryError:
            vmfiles = [filepath]
        outfile = os.path.splitext(filepath)[0] + '.asm'
        with open(outfile, 'w') as o:
            # TODO: sys initialization
            for fp in vmfiles:
                vmt = cls(fp)
                with open(fp, 'r') as f:
                    o.write('// {}\n'.format(vmt.classname))
                    # TODO: class initialization
                    for instruction in cls.extract_instructions(f):
                        o.write(vmt.parse(*instruction))


if __name__ == '__main__':
    file_or_dir = os.path.abspath(sys.argv[1])
    VMTranslator.translate(file_or_dir)

