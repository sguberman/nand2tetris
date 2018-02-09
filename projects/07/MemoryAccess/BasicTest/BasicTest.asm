// BasicTest

// 6: push constant 10
@10
D=A
@SP
A=M
M=D  // *SP=10
@SP
M=M+1  // SP++

// 7: pop local 0
@0
D=A
@LCL
D=D+M
@addr
M=D  // addr=LCL+0
@SP
M=M-1  // SP--
A=M
D=M
@addr
A=M
M=D  // *addr=*SP

// 8: push constant 21
@21
D=A
@SP
A=M
M=D  // *SP=21
@SP
M=M+1  // SP++

// 9: push constant 22
@22
D=A
@SP
A=M
M=D  // *SP=22
@SP
M=M+1  // SP++

// 10: pop argument 2
@2
D=A
@ARG
D=D+M
@addr
M=D  // addr=ARG+2
@SP
M=M-1  // SP--
A=M
D=M
@addr
A=M
M=D  // *addr=*SP

// 11: pop argument 1
@1
D=A
@ARG
D=D+M
@addr
M=D  // addr=ARG+1
@SP
M=M-1  // SP--
A=M
D=M
@addr
A=M
M=D  // *addr=*SP

// 12: push constant 36
@36
D=A
@SP
A=M
M=D  // *SP=36
@SP
M=M+1  // SP++

// 13: pop this 6
@6
D=A
@THIS
D=D+M
@addr
M=D  // addr=THIS+6
@SP
M=M-1  // SP--
A=M
D=M
@addr
A=M
M=D  // *addr=*SP

// 14: push constant 42
@42
D=A
@SP
A=M
M=D  // *SP=42
@SP
M=M+1  // SP++

// 15: push constant 45
@45
D=A
@SP
A=M
M=D  // *SP=45
@SP
M=M+1  // SP++

// 16: pop that 5
@5
D=A
@THAT
D=D+M
@addr
M=D  // addr=THAT+5
@SP
M=M-1  // SP--
A=M
D=M
@addr
A=M
M=D  // *addr=*SP

// 17: pop that 2
@2
D=A
@THAT
D=D+M
@addr
M=D  // addr=THAT+2
@SP
M=M-1  // SP--
A=M
D=M
@addr
A=M
M=D  // *addr=*SP

// 18: push constant 510
@510
D=A
@SP
A=M
M=D  // *SP=510
@SP
M=M+1  // SP++

// 19: pop temp 6
@6
D=A
@5
D=D+A
@addr
M=D  // addr=5+6
@SP
M=M-1  // SP--
A=M
D=M
@addr
A=M
M=D  // *addr=*SP

// 20: push local 0
@0
D=A
@LCL
D=D+M  // addr=LCL+0
A=D
D=M
@SP
A=M
M=D  // *SP=*addr
@SP
M=M+1  // SP++

// 21: push that 5
@5
D=A
@THAT
D=D+M  // addr=THAT+5
A=D
D=M
@SP
A=M
M=D  // *SP=*addr
@SP
M=M+1  // SP++

// 22: add
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

// 23: push argument 1
@1
D=A
@ARG
D=D+M  // addr=ARG+1
A=D
D=M
@SP
A=M
M=D  // *SP=*addr
@SP
M=M+1  // SP++

// 24: sub
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

// 25: push this 6
@6
D=A
@THIS
D=D+M  // addr=THIS+6
A=D
D=M
@SP
A=M
M=D  // *SP=*addr
@SP
M=M+1  // SP++

// 26: push this 6
@6
D=A
@THIS
D=D+M  // addr=THIS+6
A=D
D=M
@SP
A=M
M=D  // *SP=*addr
@SP
M=M+1  // SP++

// 27: add
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

// 28: sub
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

// 29: push temp 6
@6
D=A
@5
D=D+A  // addr=5+6
A=D
D=M
@SP
A=M
M=D  // *SP=*addr
@SP
M=M+1  // SP++

// 30: add
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
