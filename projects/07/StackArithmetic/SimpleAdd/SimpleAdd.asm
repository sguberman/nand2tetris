// SimpleAdd

// 6: push constant 7
@7
D=A
@SP
A=M
M=D  // *SP=7
@SP
M=M+1  // SP++

// 7: push constant 8
@8
D=A
@SP
A=M
M=D  // *SP=8
@SP
M=M+1  // SP++

// 8: add
@SP
M=M-1  // SP--
M=M-1  // SP--
A=M
D=M  // D=*SP
@SP
M=M+1  // SP++
A=M
D=D+M  // D=D+*SP
@SP
M=M-1  // SP--
A=M
M=D  // *SP=D
@SP
M=M+1  // SP++
