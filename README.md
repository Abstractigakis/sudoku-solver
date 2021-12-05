# sudoku-solver

## Problem Statement

For the rules of sudoku, google it, and play some games!

The objective is to create an algorithm that can effeciently solve any valid sudoku puzzle.

To complete this, we will use the backtracking algorithm, a bruteforce depth-first-search.

## Defenitions

A sudoku problem can be represented by a $9$ x $9$ tensor called $X$ where $X_{i,j}$ is an integer between $0$ and $9$. $X_{i,j} = 0$ is the case where the tile is empty.

To keep track of where we can add numbers, we will create a $9$ x $9$ x $9$ boolean tensor called $D$.  This is to be thought of as the domains of possibilites for each $X_{i,j}$, where $D_{i,j,k}$ is $1$ if it is possible to insert $k$ intp $X_{i,j}$ without breaking the rules of Sudoku, and $0$ otherwise.

Some facts to realize is that if we know a number on a tile conclusively, we can know that the entire tensor for $D_{i,j}$ should be filled with falses, because no value can be inserted in that space.  Conversly, if a tile is not known yet, then at least one of the entries in the associated domain should be true.  More susictly,

$$X_{i,j} \neq 0 \iff D_{i,j,k} = 0 \ \forall k$$

Also Notice that given a gamestate $X$ we can uniquley compute the Domains $D$

## Dealing with concurrency

With all of the concurrency requiremnets, it seems clear that functional programming is better suited.  We will need a better formulation of the process in place.

Consider that we have $n$ Sudoku Puzzles we want to solve at the same time via back tracking.  Call these $P_{1}$ ... $P_{n}$. We should think of these as completly isolated processes, as each puzzle does not any about the other.  

To solve each puzzle $P$ we run the back tracking algorithm, but we want to do this concurrently as well, i.e., for a given puzzle state $X$, there are a maximum $9^3$ options to attempt.  Call each possible Attempt for a given gamestate $A_{X_{i,j,k}}$: i.e. for the current puzzle gamestate $X$, the attempt where we place the number $k$ in tile $i,j$.  This produces a new game state to work on recursively.

Notice again, we want to leverage concurrency here.  I.e. if there are $m$ possible values that $k$ can take, we want try them all in parellel.  In theory this sounds great, but it may lead to combinatorial explosion, since after only $l$ numbers inserted we will have up to $l x 9^3$ process running.  

Never the less, we want to design the algorithm so that concurrent attempts can occur without issue.  When we are doing `naive back tracking` we want to be able to provide a `max_attempts` param, so that we dont run for ever.  This would mean each potential process that runs would have to increment a counter.

To do this properly with python, we will instantieat the `SudokuSolver` class, which will be responsible for storing these counters and such.  Essentially, almost all methods on the class will be static to maintain our functional approach (the `SudokuSolver` does not need to store the puzzle state, as we will be passing puzzles by value and not reference), but gives us a nice namespace for the what would otherwise be global variables.
