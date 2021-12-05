# sudoku-solver

A sudoku problem can be represented by a $9$ x $9$ tensor called $X$ where $X_{i,j}$ is an integer between $0$ and $9$. $X_{i,j} = 0$ is the case where the tile is empty.

To keep track of where we can add numbers, we will create a $9$ x $9$ x $9$ boolean tensor called $D$.  This is to be thought of as the domains of possibilites for each $X_{i,j}$, where $D_{i,j,k}$ is $1$ if it is possible to insert $k$ intp $X_{i,j}$ without breaking the rules of Sudoku, and $0$ otherwise.

Some facts to realize is that if we know a number on a tile conclusively, we can know that the entire tensor for $D_{i,j}$ should be filled with falses, because no value can be inserted in that space.  Conversly, if a tile is not known yet, then at least one of the entries in the associated domain should be true.  More susictly,

$$X_{i,j} \neq 0 \iff D_{i,j,k} = 0 \ \forall k$$

For more information on the rules of sudoku, google it, and play some games!