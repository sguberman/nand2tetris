import os
import sys

from collections import defaultdict


# VM Code -> Hack Pseudocode => Hack ASM Translations:

# push constant n
#   -> *SP=n, SP++
#   => @n, D=A, @SP, A=M, M=D, @SP, M=M+1

# pop segment i (segment: local->LCL, argument->ARG, this->THIS, that->THAT)
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

($$ASM.comparisonNNNN.callback)  // jump back here
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

    def push(self, segment, i, line_number=None):
        name = 'push {} {}'.format(segment, i)
        comment = self.comment_string(name, line_number)

        segments = defaultdict(str, {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
        })

        lcl_arg_this_that = ('@{}, D=A, @{}, D=D+M, A=D, D=M, @SP, A=M, '
                             'M=D, @SP, M=M+1').format(i, segments[segment])

        pointer = defaultdict(str, {'0': 'THIS', '1': 'THAT'})

        templates = {
            'constant': '@{}, D=A, @SP, A=M, M=D, @SP, M=M+1'.format(i),
            'local': lcl_arg_this_that,
            'argument': lcl_arg_this_that,
            'this': lcl_arg_this_that,
            'that': lcl_arg_this_that,
            'temp': ('@{}, D=A, @5, D=D+A, A=D, D=M, @SP, '
                     'A=M, M=D, @SP, M=M+1').format(i),
            'pointer': ('@{}, D=M, @SP, A=M, M=D, '
                        '@SP, M=M+1').format(pointer[i]),
        }

        assembly = templates[segment].split(', ')
        return [comment] + assembly

    def pop(self, segment, i, line_number=None):
        name = 'pop {} {}'.format(segment, i)
        comment = self.comment_string(name, line_number)

        segments = defaultdict(str, {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
        })

        lcl_arg_this_that = ('@{}, D=A, @{}, D=D+M, @addr, M=D, @SP, M=M-1, '
                             'A=M, D=M, @addr, A=M, M=D').format(i,
                             segments[segment])

        pointer = defaultdict(str, {'0': 'THIS', '1': 'THAT'})

        templates = {
            'local': lcl_arg_this_that,
            'argument': lcl_arg_this_that,
            'this': lcl_arg_this_that,
            'that': lcl_arg_this_that,
            'temp': ('@{}, D=A, @5, D=D+A, @addr, M=D, @SP, M=M-1, A=M, D=M, '
                     '@addr, A=M, M=D').format(i),
            'pointer': ('@SP, M=M-1, A=M, D=M, '
                        '@{}, M=D').format(pointer[i]),
        }

        assembly = templates[segment].split(', ')
        return [comment] + assembly

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
    def neg(cls, line_number=None):
        comment = cls.comment_string('neg', line_number)
        assembly = '@SP, M=M-1, A=M, M=-M, @SP, M=M+1'.split(', ')
        return [comment] + assembly

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
        return commands[command](*args, line_number)

    @classmethod
    def eq(cls, line_number=None):
        comment = cls.comment_string('eq', line_number)
        start_label = '$$ASM.eq.{}.start'.format(line_number)
        true_label = '$$ASM.eq.{}.true'.format(line_number)
        callback_label = '$$ASM.eq.{}.callback'.format(line_number)
        assembly = [
            '@' + start_label,
            '0;JMP  // jump to start of this call',

            '('+ true_label + ')  // this function gets skipped at first',
            '   D=-1  // it just sets D=-1 (true)',
            '   @' + callback_label,
            '   0;JMP  // jump back to call',

            '(' + start_label + ')  // call starts here',
            '   @SP',
            '   M=M-1',
            '   A=M',
            '   D=M   // D=stack.pop()',
            '   @SP',
            '   M=M-1',
            '   A=M',
            '   D=M-D  // D=stack.pop()-D',
            '   @' + true_label,
            '   D;JEQ  // jump to function if true',
            '   D=0  // otherwise false',

            '(' + callback_label + ')  // jump back here',
            '   @SP',
            '   A=M',
            '   M=D',
            '   @SP',
            '   M=M+1  // push D to stack',
        ]
        return [comment] + assembly

    @classmethod
    def gt(cls, line_number=None):
        comment = cls.comment_string('gt', line_number)
        start_label = '$$ASM.gt.{}.start'.format(line_number)
        true_label = '$$ASM.gt.{}.true'.format(line_number)
        callback_label = '$$ASM.gt.{}.callback'.format(line_number)
        assembly = [
            '@' + start_label,
            '0;JMP  // jump to start of this call',

            '('+ true_label + ')  // this function gets skipped at first',
            '   D=-1  // it just sets D=-1 (true)',
            '   @' + callback_label,
            '   0;JMP  // jump back to call',

            '(' + start_label + ')  // call starts here',
            '   @SP',
            '   M=M-1',
            '   A=M',
            '   D=M   // D=stack.pop()',
            '   @SP',
            '   M=M-1',
            '   A=M',
            '   D=M-D  // D=stack.pop()-D',
            '   @' + true_label,
            '   D;JGT  // jump to function if true',
            '   D=0  // otherwise false',

            '(' + callback_label + ')  // jump back here',
            '   @SP',
            '   A=M',
            '   M=D',
            '   @SP',
            '   M=M+1  // push D to stack',
        ]
        return [comment] + assembly

    @classmethod
    def lt(cls, line_number=None):
        comment = cls.comment_string('lt', line_number)
        start_label = '$$ASM.lt.{}.start'.format(line_number)
        true_label = '$$ASM.lt.{}.true'.format(line_number)
        callback_label = '$$ASM.lt.{}.callback'.format(line_number)
        assembly = [
            '@' + start_label,
            '0;JMP  // jump to start of this call',

            '('+ true_label + ')  // this function gets skipped at first',
            '   D=-1  // it just sets D=-1 (true)',
            '   @' + callback_label,
            '   0;JMP  // jump back to call',

            '(' + start_label + ')  // call starts here',
            '   @SP',
            '   M=M-1',
            '   A=M',
            '   D=M   // D=stack.pop()',
            '   @SP',
            '   M=M-1',
            '   A=M',
            '   D=M-D  // D=stack.pop()-D',
            '   @' + true_label,
            '   D;JLT  // jump to function if true',
            '   D=0  // otherwise false',

            '(' + callback_label + ')  // jump back here',
            '   @SP',
            '   A=M',
            '   M=D',
            '   @SP',
            '   M=M+1  // push D to stack',
        ]
        return [comment] + assembly

    @classmethod
    def and_(cls, line_number=None):
        comment = cls.comment_string('and', line_number)
        assembly = ('@SP, M=M-1, M=M-1, A=M, D=M, @SP, M=M+1, A=M, D=D&M, '
                    '@SP, M=M-1, A=M, M=D, @SP, M=M+1').split(', ')
        return [comment] + assembly

    @classmethod
    def or_(cls, line_number=None):
        comment = cls.comment_string('or', line_number)
        assembly = ('@SP, M=M-1, M=M-1, A=M, D=M, @SP, M=M+1, A=M, D=D|M, '
                    '@SP, M=M-1, A=M, M=D, @SP, M=M+1').split(', ')
        return [comment] + assembly

    @classmethod
    def not_(cls, line_number=None):
        comment = cls.comment_string('not', line_number)
        assembly = ('@SP, M=M-1, A=M, M=!M, @SP, M=M+1').split(', ')
        return [comment] + assembly

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

