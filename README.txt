ConnectZ Project:

Author: Robert Flowerday
Email: rob.flowerday@hotmail.co.uk

tests.py holds a number of unit tests that can have been used to check 
         each function and class used in connectz.py as well as the 
         process as a whole.
	 In order to run these tests successfully, you must run 
		python tests.py 
	 from the directory below the TestFiles directory that holds the  

the TestFiles directory holds a number of test .txt files that are used 
	within the tests.py unit tests.

Summary of solution:

How I approached the Problem:
1. Problem understanding: 
	Thoroughly read the brief and taking on board
	the problem to solve
		build a python script to determine the end result of a generalised version of 
		connect 4 where the number of rows and columns, aswell as the number of counters to line up can be chosen
	the inputs available
		plain text documents
	the contraints in place
		3 days to complete
		must take input from the commapnd line
		must output to the command line
		must work with 1 standalone python file
		must be able to run efficiently with very large input files
	the outputs required
		see Ouput Definitions at the bottom of this file
	what the audience / collaborators value in the code
		correct outputs are produced
		good commenting / documentation
		sensible variable and function names
		efficient code

2. I made a plan for the large steps to complete
	Steps:
	- determine user input
	- Load the file into python
	- Format the file so that it can be manipulated appropriately
	- seperate each game parameter and the set of moves
	- validate that the game is legal
	- determine the row component of each move and validate that moves are legal
	- simulate playing the game through, checking for termination points (e.g. a player winning the game) on each turn
	- if a win occured determine whether the game attempted to continue
	- if no win was occured determine if the game was a draw, or was incomplte
	- display the output to the user

 	Where possible seperated the above sections into logical sections in the code so that each function could be tested, 
     	the code is easier to read and so that the implementation of each logical component could change and be optimised 
	without affecting other code sections.

3. I determined the data structures and logical seperations to use for different elements of the program
	This largely included lists, a dictionary, functions and a class and wrote a form of psudocode to 
	indicate the neccessary inputs, outputs and interactions between each section of code.

4. I tested each function, class and logical seperation I created in the code as I went along so that should any part of the 
	code be broken throughout, it would be easy to find where the issue was occuring.

some optimisations in the code:
  - using list comprehensions rather than for loops
  - checking for win states after each move, only where possible and only from the current position rather than anywhere in the frame

What I would like to improve:
  - There are several optimisations that could be made in my code, for ecxample:
	- I check if each counter placement leads to a win, in all directions and for both players after every placement
	  It would be possible to only avoid some of these checks using knoledge of counters in other locations and past moves / checks
	- I would like to implement a search ahead routine that checks at appropriate points whether it is still possible to win the game
	- I would like to implement a wider range of test inputs
	- The use of the program could be expanded in many ways, one of which could be to calculate the best next move for either player from a given state

Output Definitions
Code 	Reason 			Description
0 	Draw 			This happens when every possible space in the frame was filled with
					a counter, but neither player achieved a line of the required length.
1 	Win for player 1 	The first player achieved a line of the required length.
2 	Win for player 2 	The second player achieved a line of the required length.
3 	Incomplete 		The file conforms to the format and contains only legal moves, but
					the game is neither won nor drawn by either player and there are
					remaining available moves in the frame. Note that a file with only a
					dimensions line constitues an incomplete game.
4 	Illegal continue 	All moves are valid in all other respects but the game has already
					been won on a previous turn so continued play is considered an illegal move.
5 	Illegal row 		The file conforms to the format and all moves are for legal columns
					but the move is for a column that is already full due to previous
					moves.
6 	Illegal column 		The file conforms to the format but contains a move for a column
					that is out side the dimensions of the board. i.e. the column selected
					is greater than X
7 	Illegal game 		The file conforms to the format but the dimensions describe a game
					that can never be won.
8 	Invalid file 		The file is opened but does not conform the format.
9 	File error 		The file can not be found, opened or read for some reason
