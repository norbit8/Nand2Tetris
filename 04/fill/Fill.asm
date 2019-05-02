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

// Checks if one of the keys is pressed, if so it continues the program,
// Elsewise it keeps checking until a key is actually pressed.

// A variable that holds 0 or 1 depending on whether the screen
// is already black  or it is still white.
@j
M=0
(START)
@KBD
D=M
@j
A=M-1
@START
A;JEQ
@RECOLOR
D;JEQ

// Initilaizing the counter.
@j
M=1
@i
M=0
(LOOP)
// Checks if the loop should stop.
@i
D=M
@SCREEN
D=D+A // the actual index of the screen address that we currently in.
@KBD
D=A-D // index - keyboard address
@START
D;JEQ

// Fills the specific part of screen with black,
// and incrementing i.
@i
D=M
@SCREEN
D=D+A
A=D
M=-1
@i
M=M+1
@LOOP
0;JEQ

(RECOLOR)
// fills the screen with white.
@j
M=0
@i
D=M
@SCREEN
D=D+A // The actual index of the screen address that we currently in.
@SCREEN
D=D-A // index - screen address
D=D+1 // So the first 16 bits will be recolored as well.
@START
D;JEQ

// Fills the specific part of screen with white,
// and incrementing i.
@i
D=M
@SCREEN
D=D+A
A=D
M=0
@i
M=M-1
@RECOLOR
0;JEQ