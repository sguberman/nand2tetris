// FibonacciSeries

// 10: push argument 1
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

// 11: pop pointer 1
@SP
M=M-1  // SP--
A=M
D=M
@THAT
M=D  // THAT=*SP

// 13: push constant 0
@0
D=A
@SP
A=M
M=D  // *SP=0
@SP
M=M+1  // SP++

// 14: pop that 0
@0
D=A
@THAT
D=D+M
@addr
M=D  // addr=THAT+0
@SP
M=M-1  // SP--
A=M
D=M
@addr
A=M
M=D  // *addr=*SP

// 15: push constant 1
@1
D=A
@SP
A=M
M=D  // *SP=1
@SP
M=M+1  // SP++

// 16: pop that 1
@1
D=A
@THAT
D=D+M
@addr
M=D  // addr=THAT+1
@SP
M=M-1  // SP--
A=M
D=M
@addr
A=M
M=D  // *addr=*SP

// 18: push argument 0
@0
D=A
@ARG
D=D+M  // addr=ARG+0
A=D
D=M
@SP
A=M
M=D  // *SP=*addr
@SP
M=M+1  // SP++

// 19: push constant 2
@2
D=A
@SP
A=M
M=D  // *SP=2
@SP
M=M+1  // SP++

// 20: sub
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

// 21: pop argument 0
@0
D=A
@ARG
D=D+M
@addr
M=D  // addr=ARG+0
@SP
M=M-1  // SP--
A=M
D=M
@addr
A=M
M=D  // *addr=*SP

// 23: label MAIN_LOOP_START
(FibonacciSeries.None$MAIN_LOOP_START)

// 25: push argument 0
@0
D=A
@ARG
D=D+M  // addr=ARG+0
A=D
D=M
@SP
A=M
M=D  // *SP=*addr
@SP
M=M+1  // SP++

// 26: if-goto COMPUTE_ELEMENT
@SP
M=M-1
A=M
D=M
@FibonacciSeries.None$COMPUTE_ELEMENT
D;JNE

// 27: goto END_PROGRAM
@FibonacciSeries.None$END_PROGRAM
0;JMP

// 29: label COMPUTE_ELEMENT
(FibonacciSeries.None$COMPUTE_ELEMENT)

// 31: push that 0
@0
D=A
@THAT
D=D+M  // addr=THAT+0
A=D
D=M
@SP
A=M
M=D  // *SP=*addr
@SP
M=M+1  // SP++

// 32: push that 1
@1
D=A
@THAT
D=D+M  // addr=THAT+1
A=D
D=M
@SP
A=M
M=D  // *SP=*addr
@SP
M=M+1  // SP++

// 33: add
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

// 34: pop that 2
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

// 36: push pointer 1
@THAT
D=M
@SP
A=M
M=D  // *SP=THAT
@SP
M=M+1  // SP++

// 37: push constant 1
@1
D=A
@SP
A=M
M=D  // *SP=1
@SP
M=M+1  // SP++

// 38: add
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

// 39: pop pointer 1
@SP
M=M-1  // SP--
A=M
D=M
@THAT
M=D  // THAT=*SP

// 41: push argument 0
@0
D=A
@ARG
D=D+M  // addr=ARG+0
A=D
D=M
@SP
A=M
M=D  // *SP=*addr
@SP
M=M+1  // SP++

// 42: push constant 1
@1
D=A
@SP
A=M
M=D  // *SP=1
@SP
M=M+1  // SP++

// 43: sub
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

// 44: pop argument 0
@0
D=A
@ARG
D=D+M
@addr
M=D  // addr=ARG+0
@SP
M=M-1  // SP--
A=M
D=M
@addr
A=M
M=D  // *addr=*SP

// 46: goto MAIN_LOOP_START
@FibonacciSeries.None$MAIN_LOOP_START
0;JMP

// 48: label END_PROGRAM
(FibonacciSeries.None$END_PROGRAM)
