#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sudoku brute force solver via dancing links exact cover algorithm

A sudoku has four constraints, represented by the columns of the matrix
--- Each cell has one number (81 columns, 9 rows and 9 columns)
--- Each row has each number once (81 columns, 9 rows and 9 numbers)
--- Each column has each number once (81 columns, 9 columns and 9 numbers)
--- Each box has each number once (81 columns, 9 boxes and 9 numbers)
We thus need 4*81 = 324 columns

Each row consists of four 1's: one for each constraint it satisfies
Eg, the number 1 in a given row and column contributes to a number in that cell,
a number in that row, a number in that column, and a number in that box

Run as:
python sudoku.py puzzle

puzzle can be an 81 character string describing the puzzle
or it can be a file:
* Ignore lines beginning with #
* Reads in all characters on other lines
* Ignores spaces and newlines
* Anything not 1-9 is treated as "unknown"
* Must only have 81 entries

Jolyon Bloomfield, January 2018
"""
import sys
from links import DLX

def add_cell(row, col, num, links):
    """
    Add rows to links for a given row and column in the puzzle
    If num = 0, add all 9 rows for all possibilities in this cell
    If num is a number, add just the single row

    rows and columns are numbered from 0 to 8
    boxes are numbered from 0 to 8, with 123 across the top
    """

    def get_constraints(row, col, num):
        """
        Compute the four constraint columns given the information for the cell
        num runs from 0 to 8
        """
        # Compute box number
        box = (col // 3) + (row // 3) * 3
        # Compute columns
        pos_col = row * 9 + col
        row_col = 81 + row * 9 + num
        col_col = 162 + col * 9 + num
        box_col = 243 + box * 9 + num
        # Put them all together
        return (pos_col, row_col, col_col, box_col)

    if num == 0:
        for i in range(9):
            name = str(row) + str(col) + ": " + str(i + 1)
            links.add_row(get_constraints(row, col, i), name)
    else:
        name = str(row) + str(col) + ": " + str(num)
        links.add_row(get_constraints(row, col, num-1), name)

def solve(problem):
    """
    Solve the given sudoku problem, provided as a list of 81 numbers
    with 0 indicating an unknown
    """
    # Initialize the problem
    links = DLX(4*81)
    row = 0
    col = 0
    for i in problem:
        add_cell(row, col, int(i), links)
        col += 1
        if col == 9:
            col = 0
            row += 1

    # Run the algorithm
    results = links.run()

    # Convert the results back into a list of 81 numbers
    solns = []
    for result in results:
        soln = "0" * 81
        for cell in result:
            row = int(cell[0])
            col = int(cell[1])
            num = cell[4]
            entry = row * 9 + col
            soln = soln[:entry] + num + soln[entry + 1:]
        solns.append(soln)

    return solns

def pretty_print(problem):
    """Draws a pretty sudoku grid for the given problem"""
    # Construct the blank grid
    top     = "\u2554===\u2564===\u2564===\u2557".replace("=", "\u2550")
    bottom  = "\u255a===\u2567===\u2567===\u255d".replace("=", "\u2550")
    line =    "\u255f---\u253c---\u253c---\u2562".replace("-", "\u2500")
    data =    "\u2551   \u2502   \u2502   \u2551"
    output = [data] * 9

    def place_number(x, y, i):
        outputx = x + 1
        if x > 2:
            outputx += 1
        if x > 5:
            outputx += 1
        current = output[y]
        output[y] = current[:outputx] + i + current[outputx+1:]

    # Place the numbers into the grid
    x = 0
    y = 0
    for char in problem:
        if char != "0":
            place_number(x, y, char)
        x += 1
        if x > 8:
            x = 0
            y += 1

    # Now combine it all
    fulloutput = []
    fulloutput.append(top)
    for i in range(0, 9):
        fulloutput.append(output[i])
        if (i + 1) % 9 == 0:
            fulloutput.append(bottom)
        elif (i + 1) % 3 == 0:
            fulloutput.append(line)

    print("\n".join(fulloutput))

def full_print(grid):
    """Prints a full sudoku grid"""
    # Construct the blank grid
    line =    "\u255f---\u253c---\u253c---\u256b---\u253c---\u253c---\u256b---\u253c---\u253c---\u2562".replace("-", "\u2500")
    top     = "\u2554===\u2564===\u2564===\u2566===\u2564===\u2564===\u2566===\u2564===\u2564===\u2557".replace("=", "\u2550")
    between = "\u2560===\u256a===\u256a===\u256c===\u256a===\u256a===\u256c===\u256a===\u256a===\u2563".replace("=", "\u2550")
    bottom  = "\u255a===\u2567===\u2567===\u2569===\u2567===\u2567===\u2569===\u2567===\u2567===\u255d".replace("=", "\u2550")

    output = [" " * 27] * 27

    def place_num(x, y, i):
        outputx = x * 3 + ((int(i) - 1) % 3)
        outputy = y * 3 + ((int(i) - 1) // 3)
        current = output[outputy]
        output[outputy] = current[:outputx] + i + current[outputx + 1:]
    def place_middle(x, y, i):
        outputx = x * 3
        outputy = y * 3 + 1
        current = output[outputy]
        output[outputy] = current[:outputx] + " " + i + " " + current[outputx + 3:]

    # Now put the numbers into it
    for x in range(9):
        for y in range(9):
            # Check if this cell is solved
            if len(grid[x][y]) == 1:
                place_middle(x, y, grid[x][y])
            else:
                for i in grid[x][y]:
                    place_num(x, y, i)

    # Add spaces and pipes into the lines
    for i, txt in enumerate(output):
        lists = [txt[i:i+3] for i in range(0, len(txt), 3)]
        output[i] = "\u2551" + "\u2502".join(lists[0:3]) + "\u2551" + \
                    "\u2502".join(lists[3:6]) + "\u2551" + \
                    "\u2502".join(lists[6:9]) + "\u2551"

    # Now combine it all
    fulloutput = []
    fulloutput.append(top)
    for i in range(0, 27):
        fulloutput.append(output[i])
        if i == 26:
            break
        if (i + 1) % 9 == 0:
            fulloutput.append(between)
        elif (i + 1) % 3 == 0:
            fulloutput.append(line)
    fulloutput.append(bottom)

    print("\n".join(fulloutput))

def parse_input(text):
    """Converts input text into 81-character format"""
    # Start by turning multiple lines into a single line
    working = ""
    if isinstance(text, list):
        for line in text:
            line = line.strip()
            if len(line) > 0 and not line.startswith("#"):
                working += line
    else:
        working = text.strip()
    # Convert to numerical data
    result = ""
    for char in working:
        if char in "123456789":
            result += char
        elif char == " " or char == "\n" :
            # Ignore spaces and newlines
            pass
        else:
            result += "0"
    # Check for applicability
    if len(result) != 81:
        raise ValueError("Unable to interpret input data")
    return result

def load_file(filename):
    """
    Loads data from a file, or if filename is 81 characters long,
    interprets that as the puzzle
    """
    if len(filename) == 81:
        result = parse_input(filename)
    else:
        try:
            with open(filename) as f:
                data = f.readlines()
        except:
            raise IOError("Unable to load data from file")
        result = parse_input(data)

    return result

# Arto Inkala puzzle!
defaultpuzzle = "800000000003600000070090200050007000000045700000100030001000068008500010090000400"

print("Sudoku Solver")

# Did we have a filename in?
if len(sys.argv) > 1:
    # Load the file
    try:
        puzzle = load_file(filename = sys.argv[1])
    except (ValueError, IOError) as e:
        print(e.args[0])
        sys.exit()
else:
    puzzle = defaultpuzzle

print("Input puzzle:")
pretty_print(puzzle)
print()

results = solve(puzzle)

if len(results) == 1:
    print("Found a unique solution:")
    pretty_print(results[0])
elif len(results) == 0:
    print("Unable to find a solution")
else:
    print("Found {} solutions:".format(len(results)))
    for idx, soln in enumerate(results):
        print("Solution #{}".format(idx + 1))
        pretty_print(soln)
        print()

    print("Full grid from combining all solutions:")
    fullgrid = [[results[0][x + y * 9] for y in range(9)] for x in range(9)]
    for soln in results[1:]:
        for x in range(9):
            for y in range(9):
                if soln[x + y * 9] not in fullgrid[x][y]:
                    fullgrid[x][y] += soln[x + y * 9]
    full_print(fullgrid)
