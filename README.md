# Sudoku Sovler

## Problem Statement

For the rules of sudoku, google it, and play some games! A sudoku problem can be represented by a $9$ x $9$ tensor called $X$ where $X_{i,j}$ is an integer between $0$ and $9$. $X_{i,j} = 0$ is the case where the tile is empty.  To keep track of where we can add numbers, we will create a $9$ x $9$ x $9$ boolean tensor called $D$.  This is to be thought of as the domains of possibilites for each $X_{i,j}$, where $D_{i,j,k}$ is $1$ if it is possible to insert $k$ intp $X_{i,j}$ without breaking the rules of Sudoku, and $0$ otherwise. Some facts to realize is that if we know a number on a tile conclusively, we can know that the entire tensor for $D_{i,j}$ should be filled with falses, because no value can be inserted in that space.  Conversly, if a tile is not known yet, then at least one of the entries in the associated domain should be true.  More susinctly,
$$X_{i,j} \neq 0 \iff D_{i,j,k} = 0 \ \forall k$$
Also Notice that given a gamestate $X$ we can uniquley compute the Domains $D$

## Strategies

We will create 3 diffeerent strategies (and possibly more) to solve the sudoku puzzles, each with greater degrees of effecincy.  NOTE: when we say effeciency, we are referring to the number of attempts the puzzle sover must make, where an attempt is a square that it tries to fill.  THe goa is to minimize the number of attempts.

First we will try a naive brute force approach, where we just guess number in a depth first search until we solve the problem.  Then we will implement forward checking, in where when we try and insert a number into the puzzle, we chekc to see if this makes any other square on the board impossible before proceeding.  Finally, we will look at a better method for selecting tiles, rather than selecting the tile that is the next in the list, we will look for the variable with the least contraints, and aim to fill this first.  we will then try the same thing with the most constrained tile, and compare resutls.

## Design Choices

For the sake of this algorithm we will be implementing all of our logic into a single class `SudokuSolve` where the puzzle and domains are stored as mutable objects. We will be passing everything as reference. This has the trade off of being very memory effecint, but does not easily lend itslef to concurrent solutions, i.e. forking the gamestate and trying to insert 2 nunmbers in parrelell.  This would require a more functional approach.  Perhaps in the future, we can rebuild with a better systems language like rust or C++, and adopt a more functional, memory hungry paradigm.
