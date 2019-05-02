// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/divide/Divide.asm

@output // If the result is not 0 it will be 1 or larger, so we initialize it
M=1
@prevout // This is the variable that keeps the output of the previous cycle of the divide label
M=0

// storing the value of RAM[13] in num1
@R13
D=M
@num1
M=D

// storing the value of RAM[14] in num2
@R14
D=M
@num2
M=D  

// checks whether the output should be zero.
@num2
D=M
@num1
D=M-D  // NUM1 - NUM2
@ZERO
D;JLT // NUM1 < NUM2

// checks whether the output should be 1
@num2
D=M<<
@num1
D=D-M 
@FINISH
D;JGT

// jumps to divide label if num2 > num1
(SHIFTLEFT2)
@num2
M=M<< // shifting left num2
D=M
@num1
D=D-M // NUM2 - NUM1
@DIVIDE
D;JGT // NUM1 < NUM2
@output
M=M<<
@FINISH // If NUM2 - NUM1 equals 0 the original NUM2 divides NUM1 by a multiple of 2
D;JEQ
@SHIFTLEFT2 // If shifted left NUM2 is still smallet than NUM1 continue shifting left
0;JMP

// Performs the binary divide operation
(DIVIDE)
@num2
M=M>> // shifting right NUM2 if we shifted left too much
@prevout
D=M
@output // Adds the outputs of the previous divide cycles to the total output
M=M+D
@num2
D=M
@num1
M=M-D // new NUM1
D=M
@R14
D=D-M // new NUM1 - ORIGINAL_NUM2
@FINISH // If the remainder is smaller than the original NUM2 we discard it
D;JLT
@ADDLASTONE // If the remainder is exactly the original NUM2 it means we can insert original NUM2 one more time into new NUM1 (the remainder), so we add 1 to the output and finish
D;JEQ
@R14
D=M
@num2
M=D
@output
D=M
@prevout // Updating this divide cycle output
M=D
@output
M=1
@SHIFTLEFT2 // if the remainder is larger than original NUM2 we continue the process
0;JMP

(ADDLASTONE)
@output
M=M+1

(FINISH) // WHEN FINISHED GO HERE
@output
D=M
@R15
M=D
@END
0;JMP


(ZERO) // If original NUM1 is smaller than original NUM2 the result is 0
@R15
M=0
@END
0;JMP

(END)
