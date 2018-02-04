// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// Pseudocode
//
// (START)
//     times = R0
//     sum = 0
//
// (LOOP)
//     times--
//     if times < 0:
//         goto RETURN
//     sum += R1
//     goto LOOP
//
// (RETURN)
//     R2 = sum
//
// (END)
//     goto END

(START)
    @R0
    D=M
    @times
    M=D         // times = R0
    @sum
    M=0         // sum = 0

(LOOP)
    @times
    M=M-1       // times--
    D=M
    @RETURN
    D;JLT       // if times < 0 goto RETURN 
    @R1
    D=M
    @sum
    M=D+M       // sum += R1
    @LOOP
    0;JMP       // goto LOOP

(RETURN)
    @sum
    D=M
    @R2
    M=D     // R2 = sum

(END)
    @END
    0;JMP

