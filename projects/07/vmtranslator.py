# VM Code -> Hack Pseudocode => Hack ASM Translations:

# push constant n
#   -> *SP=n, SP++
#   => @n, D=A, @SP, A=M, M=D, @SP, M=M+1

# pop segment i (segment: local->LCL, argument->ARG, object->THIS, array->THAT)
#   -> addr=segment+i, SP--, *addr=*SP
#   => @i, D=A, @segment, D=D+M, @addr, M=D, @SP, M=M-1, A=M, D=M, @addr, A=M, M=D

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
#   => @SP, M=M-1, M=M-1, A=M, D=M, @SP, M=M+1, A=M, D=D+/-M, @SP, M=M-1, A=M, M=D, @SP, M=M+1

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
#   => @SP, M=M-1, M=M-1, A=M, D=M, @SP, M=M+1, A=M, D=D&/|M, @SP, M=M-1, A=M, M=D, @SP, M=M+1

# not
#   -> SP--, *SP=!*SP, SP++
#   => @SP, M=M-1, A=M, M=!M, @SP, M=M+1

