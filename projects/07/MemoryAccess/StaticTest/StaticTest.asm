// 6: push constant 111
@111
D=A
@SP
A=M
M=D
@SP
M=M+1
// 7: push constant 333
@333
D=A
@SP
A=M
M=D
@SP
M=M+1
// 8: push constant 888
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
// 9: pop static 8
@SP
M=M-1
A=M
D=M
@StaticTest.8
M=D
// 10: pop static 3
@SP
M=M-1
A=M
D=M
@StaticTest.3
M=D
// 11: pop static 1
@SP
M=M-1
A=M
D=M
@StaticTest.1
M=D
// 12: push static 3
@StaticTest.3
D=M
@SP
A=M
M=D
@SP
M=M+1
// 13: push static 1
@StaticTest.1
D=M
@SP
A=M
M=D
@SP
M=M+1
// 14: sub
@SP
M=M-1
M=M-1
A=M
D=M
@SP
M=M+1
A=M
D=D-M
@SP
M=M-1
A=M
M=D
@SP
M=M+1
// 15: push static 8
@StaticTest.8
D=M
@SP
A=M
M=D
@SP
M=M+1
// 16: add
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
