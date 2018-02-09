// StackTest

// 7: push constant 17
@17
D=A
@SP
A=M
M=D  // *SP=17
@SP
M=M+1  // SP++

// 8: push constant 17
@17
D=A
@SP
A=M
M=D  // *SP=17
@SP
M=M+1  // SP++

// 9: eq
@$ASM.COMPARE.9.START
0;JMP  // jump to start of this call

($ASM.COMPARE.9.TRUE)  // this branch gets skipped at first
    D=-1  // it just sets D=-1 (true)
    @$ASM.COMPARE.9.END
    0;JMP  // jump back to call

($ASM.COMPARE.9.START)  // call starts here
    @SP
    M=M-1
    A=M
    D=M   // pop -> D
    @SP
    M=M-1
    A=M
    D=M-D  // pop-D -> D
    @$ASM.COMPARE.9.TRUE
    D;JEQ  // jump to function if true
    D=0  // otherwise false

($ASM.COMPARE.9.END)  // jump back here
    @SP
    A=M
    M=D
    @SP
    M=M+1  // push D to stack

// 10: push constant 17
@17
D=A
@SP
A=M
M=D  // *SP=17
@SP
M=M+1  // SP++

// 11: push constant 16
@16
D=A
@SP
A=M
M=D  // *SP=16
@SP
M=M+1  // SP++

// 12: eq
@$ASM.COMPARE.12.START
0;JMP  // jump to start of this call

($ASM.COMPARE.12.TRUE)  // this branch gets skipped at first
    D=-1  // it just sets D=-1 (true)
    @$ASM.COMPARE.12.END
    0;JMP  // jump back to call

($ASM.COMPARE.12.START)  // call starts here
    @SP
    M=M-1
    A=M
    D=M   // pop -> D
    @SP
    M=M-1
    A=M
    D=M-D  // pop-D -> D
    @$ASM.COMPARE.12.TRUE
    D;JEQ  // jump to function if true
    D=0  // otherwise false

($ASM.COMPARE.12.END)  // jump back here
    @SP
    A=M
    M=D
    @SP
    M=M+1  // push D to stack

// 13: push constant 16
@16
D=A
@SP
A=M
M=D  // *SP=16
@SP
M=M+1  // SP++

// 14: push constant 17
@17
D=A
@SP
A=M
M=D  // *SP=17
@SP
M=M+1  // SP++

// 15: eq
@$ASM.COMPARE.15.START
0;JMP  // jump to start of this call

($ASM.COMPARE.15.TRUE)  // this branch gets skipped at first
    D=-1  // it just sets D=-1 (true)
    @$ASM.COMPARE.15.END
    0;JMP  // jump back to call

($ASM.COMPARE.15.START)  // call starts here
    @SP
    M=M-1
    A=M
    D=M   // pop -> D
    @SP
    M=M-1
    A=M
    D=M-D  // pop-D -> D
    @$ASM.COMPARE.15.TRUE
    D;JEQ  // jump to function if true
    D=0  // otherwise false

($ASM.COMPARE.15.END)  // jump back here
    @SP
    A=M
    M=D
    @SP
    M=M+1  // push D to stack

// 16: push constant 892
@892
D=A
@SP
A=M
M=D  // *SP=892
@SP
M=M+1  // SP++

// 17: push constant 891
@891
D=A
@SP
A=M
M=D  // *SP=891
@SP
M=M+1  // SP++

// 18: lt
@$ASM.COMPARE.18.START
0;JMP  // jump to start of this call

($ASM.COMPARE.18.TRUE)  // this branch gets skipped at first
    D=-1  // it just sets D=-1 (true)
    @$ASM.COMPARE.18.END
    0;JMP  // jump back to call

($ASM.COMPARE.18.START)  // call starts here
    @SP
    M=M-1
    A=M
    D=M   // pop -> D
    @SP
    M=M-1
    A=M
    D=M-D  // pop-D -> D
    @$ASM.COMPARE.18.TRUE
    D;JLT  // jump to function if true
    D=0  // otherwise false

($ASM.COMPARE.18.END)  // jump back here
    @SP
    A=M
    M=D
    @SP
    M=M+1  // push D to stack

// 19: push constant 891
@891
D=A
@SP
A=M
M=D  // *SP=891
@SP
M=M+1  // SP++

// 20: push constant 892
@892
D=A
@SP
A=M
M=D  // *SP=892
@SP
M=M+1  // SP++

// 21: lt
@$ASM.COMPARE.21.START
0;JMP  // jump to start of this call

($ASM.COMPARE.21.TRUE)  // this branch gets skipped at first
    D=-1  // it just sets D=-1 (true)
    @$ASM.COMPARE.21.END
    0;JMP  // jump back to call

($ASM.COMPARE.21.START)  // call starts here
    @SP
    M=M-1
    A=M
    D=M   // pop -> D
    @SP
    M=M-1
    A=M
    D=M-D  // pop-D -> D
    @$ASM.COMPARE.21.TRUE
    D;JLT  // jump to function if true
    D=0  // otherwise false

($ASM.COMPARE.21.END)  // jump back here
    @SP
    A=M
    M=D
    @SP
    M=M+1  // push D to stack

// 22: push constant 891
@891
D=A
@SP
A=M
M=D  // *SP=891
@SP
M=M+1  // SP++

// 23: push constant 891
@891
D=A
@SP
A=M
M=D  // *SP=891
@SP
M=M+1  // SP++

// 24: lt
@$ASM.COMPARE.24.START
0;JMP  // jump to start of this call

($ASM.COMPARE.24.TRUE)  // this branch gets skipped at first
    D=-1  // it just sets D=-1 (true)
    @$ASM.COMPARE.24.END
    0;JMP  // jump back to call

($ASM.COMPARE.24.START)  // call starts here
    @SP
    M=M-1
    A=M
    D=M   // pop -> D
    @SP
    M=M-1
    A=M
    D=M-D  // pop-D -> D
    @$ASM.COMPARE.24.TRUE
    D;JLT  // jump to function if true
    D=0  // otherwise false

($ASM.COMPARE.24.END)  // jump back here
    @SP
    A=M
    M=D
    @SP
    M=M+1  // push D to stack

// 25: push constant 32767
@32767
D=A
@SP
A=M
M=D  // *SP=32767
@SP
M=M+1  // SP++

// 26: push constant 32766
@32766
D=A
@SP
A=M
M=D  // *SP=32766
@SP
M=M+1  // SP++

// 27: gt
@$ASM.COMPARE.27.START
0;JMP  // jump to start of this call

($ASM.COMPARE.27.TRUE)  // this branch gets skipped at first
    D=-1  // it just sets D=-1 (true)
    @$ASM.COMPARE.27.END
    0;JMP  // jump back to call

($ASM.COMPARE.27.START)  // call starts here
    @SP
    M=M-1
    A=M
    D=M   // pop -> D
    @SP
    M=M-1
    A=M
    D=M-D  // pop-D -> D
    @$ASM.COMPARE.27.TRUE
    D;JGT  // jump to function if true
    D=0  // otherwise false

($ASM.COMPARE.27.END)  // jump back here
    @SP
    A=M
    M=D
    @SP
    M=M+1  // push D to stack

// 28: push constant 32766
@32766
D=A
@SP
A=M
M=D  // *SP=32766
@SP
M=M+1  // SP++

// 29: push constant 32767
@32767
D=A
@SP
A=M
M=D  // *SP=32767
@SP
M=M+1  // SP++

// 30: gt
@$ASM.COMPARE.30.START
0;JMP  // jump to start of this call

($ASM.COMPARE.30.TRUE)  // this branch gets skipped at first
    D=-1  // it just sets D=-1 (true)
    @$ASM.COMPARE.30.END
    0;JMP  // jump back to call

($ASM.COMPARE.30.START)  // call starts here
    @SP
    M=M-1
    A=M
    D=M   // pop -> D
    @SP
    M=M-1
    A=M
    D=M-D  // pop-D -> D
    @$ASM.COMPARE.30.TRUE
    D;JGT  // jump to function if true
    D=0  // otherwise false

($ASM.COMPARE.30.END)  // jump back here
    @SP
    A=M
    M=D
    @SP
    M=M+1  // push D to stack

// 31: push constant 32766
@32766
D=A
@SP
A=M
M=D  // *SP=32766
@SP
M=M+1  // SP++

// 32: push constant 32766
@32766
D=A
@SP
A=M
M=D  // *SP=32766
@SP
M=M+1  // SP++

// 33: gt
@$ASM.COMPARE.33.START
0;JMP  // jump to start of this call

($ASM.COMPARE.33.TRUE)  // this branch gets skipped at first
    D=-1  // it just sets D=-1 (true)
    @$ASM.COMPARE.33.END
    0;JMP  // jump back to call

($ASM.COMPARE.33.START)  // call starts here
    @SP
    M=M-1
    A=M
    D=M   // pop -> D
    @SP
    M=M-1
    A=M
    D=M-D  // pop-D -> D
    @$ASM.COMPARE.33.TRUE
    D;JGT  // jump to function if true
    D=0  // otherwise false

($ASM.COMPARE.33.END)  // jump back here
    @SP
    A=M
    M=D
    @SP
    M=M+1  // push D to stack

// 34: push constant 57
@57
D=A
@SP
A=M
M=D  // *SP=57
@SP
M=M+1  // SP++

// 35: push constant 31
@31
D=A
@SP
A=M
M=D  // *SP=31
@SP
M=M+1  // SP++

// 36: push constant 53
@53
D=A
@SP
A=M
M=D  // *SP=53
@SP
M=M+1  // SP++

// 37: add
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

// 38: push constant 112
@112
D=A
@SP
A=M
M=D  // *SP=112
@SP
M=M+1  // SP++

// 39: sub
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

// 40: neg
@SP
M=M-1  // SP--
A=M
M=-M  // *SP=-*SP
@SP
M=M+1  // SP--

// 41: and
@SP
M=M-1  // SP--
M=M-1  // SP--
A=M
D=M  // D=*SP
@SP
M=M+1  // SP++
A=M
D=D&M  // D=D&*SP
@SP
M=M-1  // SP--
A=M
M=D  // *SP=D
@SP
M=M+1  // SP++

// 42: push constant 82
@82
D=A
@SP
A=M
M=D  // *SP=82
@SP
M=M+1  // SP++

// 43: or
@SP
M=M-1  // SP--
M=M-1  // SP--
A=M
D=M  // D=*SP
@SP
M=M+1  // SP++
A=M
D=D|M  // D=D|*SP
@SP
M=M-1  // SP--
A=M
M=D  // *SP=D
@SP
M=M+1  // SP++

// 44: not
@SP
M=M-1  // SP--
A=M
M=!M  // *SP=!*SP
@SP
M=M+1  // SP++
