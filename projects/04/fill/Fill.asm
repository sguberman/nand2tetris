// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(MAINLOOP)
    @KBD
    D=M         // D=key
    @BLACK
    D;JNE       // if D!=0 goto BLACK
    @WHITE
    D;JEQ       // if D==0 goto WHITE

(BLACK)
    @color
    M=-1        // 1111111111111111
    @FILL
    0;JMP       // goto FILL

(WHITE)
    @color
    M=0         // 0000000000000000
    @FILL
    0;JMP       // goto FILL

(FILL)
    @SCREEN
    D=A
    @loc
    M=D         // reset fill location
    (FILLLOOP)
        @loc
        D=M
        @131072   // total sequential bits in screen map
        D=D-A
        @MAINLOOP
        D;JGT   // if loc-131072>0 goto MAINLOOP
        @color
        D=M     // D=color
        @loc
        A=M     // access screen memory @loc
        M=D     // screen = color
        @16
        D=A
        @loc
        M=D+M  // increment loc by 16
        @FILLLOOP
        0;JMP   // goto FILLLOOP

