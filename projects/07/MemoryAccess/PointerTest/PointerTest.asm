// PointerTest

// 7: push constant 3030
@3030
D=A
@SP
A=M
M=D  // *SP=3030
@SP
M=M+1  // SP++

// 8: pop pointer 0
@SP
M=M-1  // SP--
A=M
D=M
@THIS
M=D  // THIS=*SP

// 9: push constant 3040
@3040
D=A
@SP
A=M
M=D  // *SP=3040
@SP
M=M+1  // SP++

// 10: pop pointer 1
@SP
M=M-1  // SP--
A=M
D=M
@THAT
M=D  // THAT=*SP

// 11: push constant 32
@32
D=A
@SP
A=M
M=D  // *SP=32
@SP
M=M+1  // SP++

// 12: pop this 2
@2
D=A
@THIS
D=D+M
@addr
M=D  // addr=THIS+2
@SP
M=M-1  // SP--
A=M
D=M
@addr
A=M
M=D  // *addr=*SP

// 13: push constant 46
@46
D=A
@SP
A=M
M=D  // *SP=46
@SP
M=M+1  // SP++

// 14: pop that 6
@6
D=A
@THAT
D=D+M
@addr
M=D  // addr=THAT+6
@SP
M=M-1  // SP--
A=M
D=M
@addr
A=M
M=D  // *addr=*SP

// 15: push pointer 0
@THIS
D=M
@SP
A=M
M=D  // *SP=THIS
@SP
M=M+1  // SP++

// 16: push pointer 1
@THAT
D=M
@SP
A=M
M=D  // *SP=THAT
@SP
M=M+1  // SP++

// 17: add
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

// 18: push this 2
@2
D=A
@THIS
D=D+M  // addr=THIS+2
A=D
D=M
@SP
A=M
M=D  // *SP=*addr
@SP
M=M+1  // SP++

// 19: sub
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

// 20: push that 6
@6
D=A
@THAT
D=D+M  // addr=THAT+6
A=D
D=M
@SP
A=M
M=D  // *SP=*addr
@SP
M=M+1  // SP++

// 21: add
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
