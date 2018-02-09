// BasicLoop

// 8: push constant 0
@0
D=A
@SP
A=M
M=D  // *SP=0
@SP
M=M+1  // SP++

// 9: pop local 0
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

// 10: label LOOP_START
(BasicLoop.main$LOOP_START)

// 11: push argument 0
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

// 12: push local 0
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

// 13: add
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

// 14: pop local 0
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

// 15: push argument 0
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

// 16: push constant 1
@1
D=A
@SP
A=M
M=D  // *SP=1
@SP
M=M+1  // SP++

// 17: sub
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

// 18: pop argument 0
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

// 19: push argument 0
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

// 20: if-goto LOOP_START
@SP
M=M-1
A=M
D=M
@BasicLoop.main$LOOP_START
D;JNE

// 21: push local 0
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
