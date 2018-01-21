Battleships (Bimaru)
====================

This is a battleships solver. It can find multiple solutions, and can also handle unknown clues.

Puzzles are described to the solver in a text file, which is passed in via the command line.

The approach is to use very simple logic ("Can I completely fill in this line?"), and then to start guessing. In guessing, the solver identifies as many ships as it can, and finds the longest ship that has not been definitively placed. It then enumerates all possible positions for that ship. For each possible position, it guesses that position, and then recurses, starting again with simple logic.

For 10x10 grids with unique solutions, this method typically suceeds in under a second. If there are a plethora of solutions, then it can take a while to exhaust all possibilities, but I've never seen it take more than a minute.
