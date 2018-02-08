// 7: push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// 8: push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// 9: eq
@$$ASM.eq.9.start
0;JMP  // jump to start of this call
($$ASM.eq.9.true)  // this function gets skipped at first
   D=-1  // it just sets D=-1 (true)
   @$$ASM.eq.9.callback
   0;JMP  // jump back to call
($$ASM.eq.9.start)  // call starts here
   @SP
   M=M-1
   A=M
   D=M   // D=stack.pop()
   @SP
   M=M-1
   A=M
   D=M-D  // D=stack.pop()-D
   @$$ASM.eq.9.true
   D;JEQ  // jump to function if true
   D=0  // otherwise false
($$ASM.eq.9.callback)  // jump back here
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
M=D
@SP
M=M+1
// 11: push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// 12: eq
@$$ASM.eq.12.start
0;JMP  // jump to start of this call
($$ASM.eq.12.true)  // this function gets skipped at first
   D=-1  // it just sets D=-1 (true)
   @$$ASM.eq.12.callback
   0;JMP  // jump back to call
($$ASM.eq.12.start)  // call starts here
   @SP
   M=M-1
   A=M
   D=M   // D=stack.pop()
   @SP
   M=M-1
   A=M
   D=M-D  // D=stack.pop()-D
   @$$ASM.eq.12.true
   D;JEQ  // jump to function if true
   D=0  // otherwise false
($$ASM.eq.12.callback)  // jump back here
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
M=D
@SP
M=M+1
// 14: push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// 15: eq
@$$ASM.eq.15.start
0;JMP  // jump to start of this call
($$ASM.eq.15.true)  // this function gets skipped at first
   D=-1  // it just sets D=-1 (true)
   @$$ASM.eq.15.callback
   0;JMP  // jump back to call
($$ASM.eq.15.start)  // call starts here
   @SP
   M=M-1
   A=M
   D=M   // D=stack.pop()
   @SP
   M=M-1
   A=M
   D=M-D  // D=stack.pop()-D
   @$$ASM.eq.15.true
   D;JEQ  // jump to function if true
   D=0  // otherwise false
($$ASM.eq.15.callback)  // jump back here
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
M=D
@SP
M=M+1
// 17: push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// 18: lt
@$$ASM.lt.18.start
0;JMP  // jump to start of this call
($$ASM.lt.18.true)  // this function gets skipped at first
   D=-1  // it just sets D=-1 (true)
   @$$ASM.lt.18.callback
   0;JMP  // jump back to call
($$ASM.lt.18.start)  // call starts here
   @SP
   M=M-1
   A=M
   D=M   // D=stack.pop()
   @SP
   M=M-1
   A=M
   D=M-D  // D=stack.pop()-D
   @$$ASM.lt.18.true
   D;JLT  // jump to function if true
   D=0  // otherwise false
($$ASM.lt.18.callback)  // jump back here
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
M=D
@SP
M=M+1
// 20: push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// 21: lt
@$$ASM.lt.21.start
0;JMP  // jump to start of this call
($$ASM.lt.21.true)  // this function gets skipped at first
   D=-1  // it just sets D=-1 (true)
   @$$ASM.lt.21.callback
   0;JMP  // jump back to call
($$ASM.lt.21.start)  // call starts here
   @SP
   M=M-1
   A=M
   D=M   // D=stack.pop()
   @SP
   M=M-1
   A=M
   D=M-D  // D=stack.pop()-D
   @$$ASM.lt.21.true
   D;JLT  // jump to function if true
   D=0  // otherwise false
($$ASM.lt.21.callback)  // jump back here
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
M=D
@SP
M=M+1
// 23: push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// 24: lt
@$$ASM.lt.24.start
0;JMP  // jump to start of this call
($$ASM.lt.24.true)  // this function gets skipped at first
   D=-1  // it just sets D=-1 (true)
   @$$ASM.lt.24.callback
   0;JMP  // jump back to call
($$ASM.lt.24.start)  // call starts here
   @SP
   M=M-1
   A=M
   D=M   // D=stack.pop()
   @SP
   M=M-1
   A=M
   D=M-D  // D=stack.pop()-D
   @$$ASM.lt.24.true
   D;JLT  // jump to function if true
   D=0  // otherwise false
($$ASM.lt.24.callback)  // jump back here
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
M=D
@SP
M=M+1
// 26: push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// 27: gt
@$$ASM.gt.27.start
0;JMP  // jump to start of this call
($$ASM.gt.27.true)  // this function gets skipped at first
   D=-1  // it just sets D=-1 (true)
   @$$ASM.gt.27.callback
   0;JMP  // jump back to call
($$ASM.gt.27.start)  // call starts here
   @SP
   M=M-1
   A=M
   D=M   // D=stack.pop()
   @SP
   M=M-1
   A=M
   D=M-D  // D=stack.pop()-D
   @$$ASM.gt.27.true
   D;JGT  // jump to function if true
   D=0  // otherwise false
($$ASM.gt.27.callback)  // jump back here
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
M=D
@SP
M=M+1
// 29: push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// 30: gt
@$$ASM.gt.30.start
0;JMP  // jump to start of this call
($$ASM.gt.30.true)  // this function gets skipped at first
   D=-1  // it just sets D=-1 (true)
   @$$ASM.gt.30.callback
   0;JMP  // jump back to call
($$ASM.gt.30.start)  // call starts here
   @SP
   M=M-1
   A=M
   D=M   // D=stack.pop()
   @SP
   M=M-1
   A=M
   D=M-D  // D=stack.pop()-D
   @$$ASM.gt.30.true
   D;JGT  // jump to function if true
   D=0  // otherwise false
($$ASM.gt.30.callback)  // jump back here
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
M=D
@SP
M=M+1
// 32: push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// 33: gt
@$$ASM.gt.33.start
0;JMP  // jump to start of this call
($$ASM.gt.33.true)  // this function gets skipped at first
   D=-1  // it just sets D=-1 (true)
   @$$ASM.gt.33.callback
   0;JMP  // jump back to call
($$ASM.gt.33.start)  // call starts here
   @SP
   M=M-1
   A=M
   D=M   // D=stack.pop()
   @SP
   M=M-1
   A=M
   D=M-D  // D=stack.pop()-D
   @$$ASM.gt.33.true
   D;JGT  // jump to function if true
   D=0  // otherwise false
($$ASM.gt.33.callback)  // jump back here
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
M=D
@SP
M=M+1
// 35: push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// 36: push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
// 37: add
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
// 38: push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
// 39: sub
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
// 40: neg
@SP
M=M-1
A=M
M=-M
@SP
M=M+1
// 41: and
@SP
M=M-1
M=M-1
A=M
D=M
@SP
M=M+1
A=M
D=D&M
@SP
M=M-1
A=M
M=D
@SP
M=M+1
// 42: push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// 43: or
@SP
M=M-1
M=M-1
A=M
D=M
@SP
M=M+1
A=M
D=D|M
@SP
M=M-1
A=M
M=D
@SP
M=M+1
// 44: not
@SP
M=M-1
A=M
M=!M
@SP
M=M+1
