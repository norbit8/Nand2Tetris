// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

@sum // SUM WILL BE TRANSFERRED INTO RAM[2] WHEN THE PROGRAM WILL FINISH.
M=0  // INITIALIZING THE SUM.
@R2 // INITILIZING R2 TO BE 0 AS REQUESTED
M=0 // ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
@R0 // Inserting RAM[0] value into the variable r0
D=M
@r0
M=D
@IPOS
D;JGT // JUMPS TO IPOS IF D>0
@INEG
D;JLT // JUMPS TO INEG IF D<0
@ZERO
D;JEQ // JUMPS TO ZERO IF D==0

(R1HEAD)
@R1 // Inserting RAM[1] value into the variable r1
D=M
@r1
M=D
@JPOS 
D;JGT // JUMPS TO JPOS IF D>0
@JNEG
D;JLT // JUMPS TO JNEG IF D<0
@ZERO
D;JEQ // JUMPS TO ZERO IF D==0

(IPOS) // CHANGING THE VALUE OF i TO REPRESENT THE SIGN OF R0.
@i
M=1
@R1HEAD
0;JEQ

(INEG) // CHANGING THE VALUE OF i TO REPRESENT THE SIGN OF R0, AND CHANGING r0 VALUE TO POSITIVE.
@i
M=0
@r0
D=0
M=D-M
@R1HEAD
0;JEQ

(JPOS) // CHANGING THE VALUE OF j TO REPRESENT THE SIGN OF R1.
@j
M=1
@CHECKIFSWITCH
1;JMP

(JNEG) // CHANGING THE VALUE OF j TO REPRESENT THE SIGN OF R1, AND CHANGING r1 VALUE TO POSITIVE.
@j
M=0
@r1
D=0
M=D-M
@CHECKIFSWITCH
1;JMP

(SWITCHER)
@r0
D=M
@temp // temp = r0
M=D
@r1
D=M
@r0
M=D
@temp
D=M
@r1
M=D
@CHECKS
0;JMP

(CHECKIFSWITCH)
// SWITCHING THE GREATER VALUE TO BE IN r0
@r0
D=M
@r1
D=D-M
@SWITCHER
D;JLT  // checks if r0-r1<0 <=> r0<r1

(CHECKS)
@r0
D=M
@sum
M=M+D
@r1
M=M-1
D=M
@CHECKS // GO BACK TO 'CHECKS' LABEL <=> LOOP SHOULD NOT TERMINATE <=> R1!=0.
D;JGT
@i
D=M
@j
D=D-M
@DEADEND // SUM SHOULD BE POSITIVE. 
D;JEQ    // SO WE JUMP TO THE END.
@MAKENEGATIVE // SUM SHOULD BE NEGATIVE.
0;JMP         // SO WE JUMP TO CHANGE IT IN 'MAKENEGATIVE' LABEL BELOW.

(MAKENEGATIVE)
D=0
@sum
M=D-M
@DEADEND
0;JMP

(ZERO)
@R2
M=0
@1000 // TERMINATE
0;JMP // ^^^^^^^^^

(DEADEND)
@sum
D=M
@R2
M=D
@1000 // TERMINATE
0;JMP // ^^^^^^^^^
