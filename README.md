# Sudoku-Solver
## Description
This algorithm uses constraint satisfaction techniques to solve sudoku puzzles as quickly as possible.
Input standard sudokus in a 9 by 9 NumPy array and this program will solve it or establish it as unsolvable.

## Algorithm Overview
The algorithm can be broken down into two main parts: the "Logical Solve" and the "AI Solve"

### Logical solve
The partial sudoku object has a variable for the sudoku its self, but also a dictionary that takes an integer from 0 to 80 as its key and returns a list of integers. The key represents a square on the sudoku board (starting top left, going right then to the next row ect) and the list represents the possible values that could go in this square.
When logical solve is run on a new sudoku, it goes through each given clue value and runs the "setValue" function. This removes that value as a possible option for every square in the same row, collumn or box (e.g. if a sudoku was given with a 3 in space (4, 5), 3 would be removes as a possible value from all boxes in collumn 4, row 5 and evey square in the middle box).
When a squares possible values are reduced down to 1 the setValue function is then called to set its value and narrow down possible values for other squares. If a sqaures possible values is narrowed down to 0 the sudoku is returned as impossible.
When all squares have 2 or more possible values the aiSolve function is run.

### AI Solve
This function first determines whether the state it is given is a solution and if it is its returned.
If not, it finds the 3x3 box with the least empty spaces (excluding boxes with no empty spaces). In this box it finds the value that can go in the least spaces but can go in at least 2. A new partial sudoku is then created for each space the value can go in and these sudokus are logically solved one by one with the guessed value put in place.
If many sudokus are in a partial state at once, the one with more guessed values will be prioritised, creating a depth first seach.
If all places in a box have been guessed and none of them return a correct sudoku the sudoku is deemed impossible and a 9x9 matrix of -1's is returned.
