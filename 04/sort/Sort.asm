// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Sorts the array starting at the address in R14 with length as specified in R15.
// The sort is in descending order.
// (R14 and R15 refer to RAM[14] and RAM[15] respectively.)

@2 // Checks whether the list has less than two elements, if it has it is already sorted and therefore goes straight to the end
D=A
@R15
D=D-M
@END
D;JGT

@R14 // Initializing the temporary maximal element in the array to the first element
A=M
D=M
@tempMax
M=D

@R14 // Initializing the current element we are comparing to the temporary maximum stored in tempMax
A=M+1
D=M
@currElement
M=D
D=A

@cmpCounter //Initializes the number of times we completed the inner loop - meaning the number of maximal elements already sorted.
M=0

@counter // Initializing the counter which determines how many compares we have done within the inner loop - how many inner loop iterations we have completed.
M=0

@R14 //Initializes the location within the array that we currently want to set.
D=M
@spotToSet
M=D

@currPointer // Initializing a pointer which tells us what is the address of the current element we are comparing to the temporary maximum stored in tempMax
M=D+1

@R15 // Places the length of the array within the variable arrayLen.
D=M
@arrayLen
M=D

@R15 // Initializes the length of the current sub array we are sorting after choosing the previous maximal element.
D=M
@lenSubArray
M=D
@INNERLOOP
0;JEQ

(OUTERLOOP)
@counter // Every time we choose a maximal element within a sub array and complete all iterations within the inner loop we initialize the counter.
M=0

@lenSubArray // After we complete an inner loop and choose the maximal element in the sub array we would like to choose the next maximal element amongst the elements still left unsorted.
M=M-1
D=M
@END
D-1;JEQ // If no more elements left the list is sorted and we go to the end.

@spotToSet // Elsewise we update the rest of the control variables in order to continue sorting.
M=M+1
D=M
@currPointer
M=D+1
@spotToSet
A=M
D=M
@tempMax
M=D
@spotToSet
A=M+1
D=M
@currElement
M=D

(INNERLOOP) // The inner loop is the where we choose the maximal element amongst the sub array which has not yet benn sorted previously.

@tempMax // Determining whether the sign of the temporary maximal element is negative or non-negative
D=M
@TEMPMAXNOTNEG
D;JGE
@TEMPMAXNEG
0;JEQ

(TEMPMAXNOTNEG) // Assigning 1 to the variable i if the temporary maximal elemant is non-negative
@i
M=1
@CURRHEADER
0;JEQ

(TEMPMAXNEG) // Assigning 0 to the variable i if the temporary maximal elemant is negative, and assigning it's absolute value to tempMax
@i
M=0
@tempMax
D=0
M=D-M

(CURRHEADER) //Determining whether the sign of the current element we are comparing to the temporary maximum element is negative or non-negative
@currElement
D=M
@CURRELEMENTNOTNEG
D;JGE
@CURRELEMENTNEG
0;JEQ

(CURRELEMENTNOTNEG) // Assigning 1 to the variable j if the the current element we are comparing to the temporary maximum is non-negative
@j
M=1
@COMPARE
0;JEQ

(CURRELEMENTNEG) // Assigning 1 to the variable j if the the current element we are comparing to the temporary maximum is non-negative, and assigning it's absolute value to currElement
@j
M=0
@currElement
D=0
M=D-M

(COMPARE) //checks signs of both numbers in order to decide what treatment they should recieve.
@i
D=M
@j
D=D&M
@BOTHNOTNEG
D;JGT

@i
D=M
@ITERATIONEND	//The temporary maximum is non-negative while the current element we are comparing to is negative, so the temp max is still tempMax,
D;JGT		 //so we leave it as is and perform another iteration and compare to the next element in the array

@j
D=M
@RETWITHSWAP //The temporary maximum is negative while the current element we are comparing to is non-negative, so the temp max has to be changed
D;JGT

@BOTHNEG
0;JEQ

(BOTHNOTNEG)//Both temporary maximum and current element we are comparing to are non-negative
@tempMax
D=M
@currElement
D=D-M
@ITERATIONEND
D;JGE
@RETWITHSWAP
0;JEQ

(BOTHNEG)//Both temporary maximum and current element we are comparing to are negative

@tempMax
D=M
@currElement
D=D-M
@RETWITHSWAP
D;JGE
@RETNOSWAP
0;JEQ

(RETWITHSWAP) // Here we return the tempMax and currElement to their previous signs before we swap them in the SWAP label for the currElement is larger 
@i
D=M
@SECONDSIGNSWAP
D;JGT
D=0
@tempMax
M=D-M

(SECONDSIGNSWAP)
@j
D=M
@SWAP
D;JGT
D=0
@currElement
M=D-M

(SWAP) // As said above here we set the currElement as the new maximum because it is larger.
@tempMax
D=M
@currPointer
A=M
M=D
@currElement
D=M
@spotToSet
A=M
M=D
@tempMax
M=D
@ITERATIONEND
0;JEQ

(RETNOSWAP) //Here we return the tempMax and currElement to their previous signs without swaping them, because the tempMax is larger 
@i
D=M
@SECONDSIGNNOSWAP
D;JGT
D=0
@tempMax
M=D-M

(SECONDSIGNNOSWAP)
@j
D=M
@ITERATIONEND
D;JGT
D=0
@currElement
M=D-M

(ITERATIONEND) // After completing the comparison and determining the new tempMax amongst the elements not sorted yet, we update the control variables and check if there are still
		// elements to be compared to within the current sub array. If no more elements we exit the inner loop to the outer loop and start the operation of choosing the maximmal
		// element of the next sub array.
@counter
M=M+1
D=M+1
@lenSubArray
D=M-D
@OUTERLOOP
D;JEQ
@currPointer
M=M+1
A=M
D=M
@currElement
M=D
@INNERLOOP
0;JEQ

(END) // We reach this point if we finished sorting the list
