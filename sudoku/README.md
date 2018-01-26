Sudoku
======

Ah, the one puzzle that everybody is going to recognize. This solver uses a brute force method based on the dancing links algorithm:

* https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/sudoku.paper.html
* https://arxiv.org/abs/cs/0011047

The solver rather efficiently finds all solutions to a given puzzle, and prints them in nice grids. If there are multiple solutions, it constructs an intersection of all of the solutions and presents that too.

Run it as `python sudoku.py puzzle`, where puzzle may either be an 81-character puzzle, or a filename containing a puzzle. Two example files are given: `example` and `multi`. A default puzzle is solved if no puzzle is provided; this is Arto Inkala's "hardest sudoku puzzle in the world".

If you're more interested in logic, the best resource for sudoku logical techniques is http://www.sudokuwiki.org/. The most interesting solver I've seen along these lines can be seen at http://ideone.com/DL1LSl (but only solves the simple things before going to recursion).
