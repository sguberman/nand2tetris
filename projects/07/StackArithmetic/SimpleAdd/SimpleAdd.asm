// 6: push constant 7
@7
D=A
@SP
A=M
M=D
@SP
M=M+1
// 7: push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// 8: add
@SP
M=M-1
M=M-1
A=M
D=M
@SP
M=M+1
A=M
D=D+M
@SP
M=M-1
A=M
M=D
@SP
M=M+1
