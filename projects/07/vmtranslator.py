# Translations:

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
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@ASM$CMP.true
D;JEQ/JGT/JLT
D=0
(ASM$CMP.callback)
@SP
A=M
M=D
@SP
M=M+1
@ASM$CMP.end
0:JMP
(ASM$CMP.true)
D=-1
@ASM$CMP.callback
0;JMP
(ASM$CMP.end)



# gt
# lt

# and/or
#   -> SP--, SP--, D=SP*, SP++, D=D&/|SP*, SP--, SP*=D, SP++
#   => @SP, M=M-1, M=M-1, A=M, D=M, @SP, M=M+1, A=M, D=D&/|M, @SP, M=M-1, A=M, M=D, @SP, M=M+1

# not
#   -> SP--, *SP=!*SP, SP++
#   => @SP, M=M-1, A=M, M=!M, @SP, M=M+1
