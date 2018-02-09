// StaticTest

// 6: push constant 111
@111
D=A
@SP
A=M
M=D  // *SP=111
@SP
M=M+1  // SP++

// 7: push constant 333
@333
D=A
@SP
A=M
M=D  // *SP=333
@SP
M=M+1  // SP++

// 8: push constant 888
@888
D=A
@SP
A=M
M=D  // *SP=888
@SP
M=M+1  // SP++

// 9: pop static 8
@SP
M=M-1  // SP--
A=M
D=M
@StaticTest.static.8
M=D  // StaticTest.static.8=*SP

// 10: pop static 3
@SP
M=M-1  // SP--
A=M
D=M
@StaticTest.static.3
M=D  // StaticTest.static.3=*SP

// 11: pop static 1
@SP
M=M-1  // SP--
A=M
D=M
@StaticTest.static.1
M=D  // StaticTest.static.1=*SP

// 12: push static 3
@StaticTest.static.3
D=M
@SP
A=M
M=D  // *SP=StaticTest.static.3
@SP
M=M+1  // SP++

// 13: push static 1
@StaticTest.static.1
D=M
@SP
A=M
M=D  // *SP=StaticTest.static.1
@SP
M=M+1  // SP++

// 14: sub
@SP
M=M-1  // SP--
M=M-1  // SP--
A=M
D=M  // D=*SP
@SP
M=M+1  // SP++
A=M
D=D-M  // D=D-*SP
@SP
M=M-1  // SP--
A=M
M=D  // *SP=D
@SP
M=M+1  // SP++

// 15: push static 8
@StaticTest.static.8
D=M
@SP
A=M
M=D  // *SP=StaticTest.static.8
@SP
M=M+1  // SP++

// 16: add
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
