#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Battleships/Bimaru solver logic library

Jolyon Bloomfield, Jan 2018
"""
import numpy as np
from colorama import init, Fore, Style
from framework import PuzzleState, PuzzleSolver, Inconsistent, Solved
init()

if __name__ == "__main__":
    print("This is a library. It is not intended to be executed stand-alone.")

# Some constants
UNKNOWN = 0
SHIP = 1
WATER = 2

class PuzzleInfo(object):
    """Stores information about the puzzle, including grid size and clues"""
    def __init__(self, rowclues, colclues, ships):
        """
        rowclues and colclues are the clues for each row and column
          The grid size is extracted from the clues
          Clues should be the number of ship segments in that row/col, or None if
          no clue is known
        ships contains the number of ships we are searching for of each length
          ships[0] = # of length 1 ships
          ships[1] = # of length 2 ships
          etc.
        """
        self.width = len(colclues)
        self.height = len(rowclues)
        self.rowclues = rowclues
        self.colclues = colclues
        self.ships = ships

class Grid(PuzzleState):
    """Holds the state of the puzzle"""

    def __init__(self, info):
        """
        Initialize a blank state, given the puzzle information
        """
        self.info = info
        self.grid = np.zeros([info.width, info.height], dtype=np.int8)
        # Grid is indexed as (x, y) = (col, row), with (0,0) in the top left corner
        # Note that this is TRANSPOSED compared to the way that numpy prints arrays
        # 0 = unknown
        # 1 = ship
        # 2 = water

    def clone(self):
        """Clones this state, returning a new one"""
        newgrid = Grid(self.info)
        np.copyto(newgrid.grid, self.grid)
        return newgrid

    def __str__(self):
        """Produce a string representation of the state (typically, to be printed)"""
        rows = ["" for _ in range(self.info.height + 3)]

        # Start by making the border
        rows[1] = "    ┌" + "-" * (self.info.width * 2 - 1) + "┐"
        for i in range(2, len(rows) - 1):
            rows[i] = "|" + " " * (self.info.width * 2 - 1) + "| "
        rows[-1] = "    └" + "-" * (self.info.width * 2 - 1) + "┘"

        # Now, add in the clues
        for idx, num in enumerate(self.info.rowclues):
            if num is None:
                rows[idx + 2] = '  ? ' + rows[idx + 2]
            else:
                rows[idx + 2] = '{:3d}'.format(num) + " " + rows[idx + 2]
        rows[0] = "    "
        for idx, num in enumerate(self.info.colclues):
            if num is None:
                rows[0] += " ?"
            else:
                rows[0] += " " + str(num)

        def set_char(x, y, char):
            row = y + 2
            col = 5 + 2*x
            rows[row] = rows[row][0:col] + char + rows[row][col + 1:]

        # Now put in the solution
        for y in range(self.info.height):
            for x in range(self.info.width):
                cell = self.grid[x, y]
                if cell == WATER:
                    set_char(x, y, "~")
                elif cell == SHIP:
                    # Ships need more logic
                    if cell_is(x, y-1, SHIP, self) and cell_is(x, y+1, WATER, self):
                        set_char(x, y, "V")
                    elif cell_is(x, y+1, SHIP, self) and cell_is(x, y-1, WATER, self):
                        set_char(x, y, "Λ")
                    elif cell_is(x+1, y, SHIP, self) and cell_is(x-1, y, WATER, self):
                        set_char(x, y, "<")
                    elif cell_is(x-1, y, SHIP, self) and cell_is(x+1, y, WATER, self):
                        set_char(x, y, ">")
                    elif cell_is(x-1, y, WATER, self) and cell_is(x+1, y, WATER, self) and cell_is(x, y+1, WATER, self) and cell_is(x, y-1, WATER, self):
                        set_char(x, y, "@")
                    else:
                        set_char(x, y, "#")

        return "\n".join(rows)

    def pretty_print(self):
        """Prints the state to the screen in color"""
        for char in str(self):
            if char == "~":
                print(Fore.BLUE + "~" + Fore.RESET, end="")
            elif char in "<>@#ΛV":
                print(Fore.RED + Style.BRIGHT + char + Style.RESET_ALL, end="")
            else:
                print(char, end="")
        print()

    def make_hash(self):
        """Make a hash of the puzzle state"""
        return hash(self.grid.tostring())

class BattleShips(PuzzleSolver):
    """Solver class for Battleships"""

    def logic(self):
        """
        Perform logical operations on the current state to solve the puzzle
        as much as possible.

        Raises Solved if solved
        Raises Inconsistent if inconsistent

        Otherwise, returns a tuple (guesslist, requirednum) which contains a list of
        guesses to make, and the number of these guesses that must simultaneously apply.
        """
        # Continuously loop - we must exit by returning or raising an exception
        while True:
            # Start by doing simple checks to find rows/cols that can be filled in
            simple_logic(self)

            # Check for consistency
            validate(self.state)

            # Now, go and count all ships
            goodships, badships, ships = find_ships(self.state)

            # Are there any ships with lengths longer than maximum?
            maxlength = len(self.state.info.ships)
            if len(goodships) > maxlength:
                raise Inconsistent()

            # Check on how many boats we're missing
            remaining = [self.state.info.ships[i] - goodships[i] for i in range(maxlength)]
            if any(i < 0 for i in remaining):
                # Problems!
                raise Inconsistent()
            if all(i == 0 for i in remaining):
                # We have a solution - grid is valid, and all boats accounted for
                # Fill in any unknowns with water
                water_fill(self.state)
                raise Solved()

            # If all one-length ships are accounted for, fill in all holes with water
            if remaining[0] == 0:
                holes = find_holes(self.state)
                if len(holes) > 0:
                    for x, y in holes:
                        set_water(x, y, self.state)
                    # Go back to simple logic
                    continue

            # Find the longest length that is not yet satisfied
            for i in range(maxlength-1, -1, -1):
                if remaining[i] > 0:
                    maxlength = i + 1
                    break

            # Are there too many badships of this length?
            if badships[maxlength - 1] > remaining[maxlength - 1]:
                raise Inconsistent()

            # Close all badships of this length
            if badships[maxlength - 1] > 0:
                for pos, length, horiz, good in ships:
                    if length == maxlength and good == False:
                        set_full_ship((pos, length, horiz), self.state)
                # Give simple logic another go
                continue

            # We now have zero badships of this length, but we're still missing ships.
            # Is our parent guessing on the same length?
            if self.depth > 0 and self.parent.guesslen == maxlength:
                # Looks like they are! We can lift their possibilities!
                parentposs = self.parent.guesslist[self.parent.guess + 1:]
                # We have to weed out anything that doesn't work though
                possibilities = [i for i in parentposs if allowed_placement(i, self.state)]
            else:
                # Go and construct a list of possibilities from scratch
                possibilities = find_positions(self.state, maxlength)

            # Check that there are sufficient possibilities to cover the remaining slots
            if len(possibilities) < remaining[maxlength - 1]:
                raise Inconsistent()

            # If the number of possibilities is equal to the number of ships left,
            # apply them all and continue (Inconsistent will be caught in framework)
            if len(possibilities) == remaining[maxlength - 1]:
                for i in possibilities:
                    self.apply_guess(i)
                continue

            # Set the length of ship that we're guessing, so that any children can read it
            self.guesslen = maxlength

            # And get out, so we can start guessing!
            return possibilities, remaining[maxlength - 1]

    def apply_guess(self, guess):
        """
        Apply the given guess.
        Raise Inconsistent if the guess is inconsistent.
        """
        set_full_ship(guess, self.state)

    def afterguess(self, guess):
        """
        After setting a length 1 ship, set it to water and perform logic again
        """
        pos, length, horiz = guess
        if length == 1:
            x, y = pos
            set_water(x, y, self.state)  # This should not raise an exception...
            return True
        return False

def run(rowclues, colclues, initinfo, ships, debug=False):
    """
    Run everything, given the row and column clues, initial board, and ship list.
    Returns a list of solutions found, and the number of guesses taken.
    """
    info = PuzzleInfo(rowclues, colclues, ships)
    initState = Grid(info)
    initialize(initState, initinfo)
    print("Initial state:")
    initState.pretty_print()
    solver = BattleShips(initState, debug=debug)
    solver.solve()
    return solver.solutionlist, BattleShips.StateNum - 1

def initialize(grid, info):
    """
    Takes in an initialized grid, and applies initial information.
    Raises Inconsistent if an inconsistency is found.
    """
    # Check board size
    if grid.info.height < 1 or grid.info.width < 1:
        print("Invalid board size.")
        raise Inconsistent

    # Apply initial info
    try:
        for (x, y, infotype) in info:
            if infotype == "w":
                # Add in a single water cell
                set_water(x, y, grid)
            elif infotype == "o":
                # Add in a single ship cell, and surround with water
                set_full_ship(((x, y), 1, True), grid)
            elif infotype == "#":
                # Add in a single ship cell, and surround with water on diagonals
                set_ship(x, y, grid)
            elif infotype == "<":
                # Add in two ship cells, and surround with water appropriately
                set_ship(x, y, grid)
                set_ship(x + 1, y, grid)
                set_water(x - 1, y, grid)
            elif infotype == ">":
                # Add in two ship cells, and surround with water appropriately
                set_ship(x, y, grid)
                set_ship(x - 1, y, grid)
                set_water(x + 1, y, grid)
            elif infotype == "v":
                # Add in two ship cells, and surround with water appropriately
                set_ship(x, y, grid)
                set_ship(x, y - 1, grid)
                set_water(x, y + 1, grid)
            elif infotype == "^":
                # Add in two ship cells, and surround with water appropriately
                set_ship(x, y, grid)
                set_ship(x, y + 1, grid)
                set_water(x, y - 1, grid)
            else:
                print("Error in initial data. Information '" + str(infotype) + "' unrecognised.")
                raise Inconsistent
    except Inconsistent:
        print("Initial data is inconsistent. No solution possible.")
        raise

    # Perform consistency checks
    # Compute number of ship segments
    ships = grid.info.ships
    shipcount = 0
    for i in range(len(ships)):
        shipcount += (i+1) * ships[i]

    # Check if the row clues are all present (no None entries)
    rowcount = 0
    for i in grid.info.rowclues:
        if i is None:
            break
        rowcount += i
    else:
        # Make sure the row count and the ship count are in agreement
        if rowcount != shipcount:
            print("Number of entries on rows not equal to total number of ships.")
            raise Inconsistent

    # Check if the column clues are all present (no None entries)
    colcount = 0
    for i in grid.info.colclues:
        if i is None:
            break
        colcount += i
    else:
        # Make sure the column count and the ship count are in agreement
        if colcount != shipcount:
            print("Number of entries on columns not equal to total number of ships.")
            raise Inconsistent

    # Validate the present board
    try:
        validate(grid)
    except Inconsistent:
        print("Initial state is invalid.")
        raise

def combine_grids(states):
    """
    Takes in a number of states (typically solutions), and finds what they all
    have in common. Returns a new Grid object.
    """
    result = states[0].clone()
    for i in states[1:]:
        result.grid &= i.grid
    return result

def cell_is(x, y, setting, grid):
    """Checks if a cell is a specific setting"""
    # Check for off the board first (considered water)
    if x < 0 or x >= grid.info.width:
        return setting == WATER
    if y < 0 or y >= grid.info.height:
        return setting == WATER
    # Otherwise, check the grid
    return grid.grid[x, y] == setting

def set_water(x, y, grid):
    """
    Sets the (x, y) position in the grid to be water (ignore if off the board)
    Returns True if the state changed
    """
    if x < 0 or y < 0:
        return False
    if x >= grid.info.width or y >= grid.info.height:
        return False
    if grid.grid[x, y] == SHIP:
        raise Inconsistent()
    elif grid.grid[x, y] == WATER:
        return False
    else:
        grid.grid[x, y] = WATER
        return True

def set_ship(x, y, grid):
    """
    Sets the (x, y) position in the grid to be a ship
    This is the only routine that should be setting any ship pieces
    Returns True if something changed
    """
    if x < 0 or y < 0:
        raise Inconsistent()
    if x >= grid.info.width or y >= grid.info.height:
        raise Inconsistent()
    if grid.grid[x, y] == WATER:
        raise Inconsistent()

    if grid.grid[x, y] == UNKNOWN:
        grid.grid[x, y] = SHIP
        # Now mark diagonals with water
        set_water(x+1, y+1, grid)
        set_water(x-1, y+1, grid)
        set_water(x+1, y-1, grid)
        set_water(x-1, y-1, grid)
        return True
    else:
        return False

def set_full_ship(placement, grid):
    """
    Write a complete ship to the grid
    Returns True if anything changed
    """
    pos, length, horiz = placement
    x, y = pos
    changed = False
    if length == 1:
        changed = changed | set_ship(x, y, grid)
        changed = changed | set_water(x, y - 1, grid)
        changed = changed | set_water(x, y + 1, grid)
        changed = changed | set_water(x + 1, y, grid)
        changed = changed | set_water(x - 1, y, grid)
    elif horiz:
        # Horizontal
        for i in range(length):
            changed = changed | set_ship(x + i, y, grid)
        changed = changed | set_water(x - 1, y, grid)
        changed = changed | set_water(x + length, y, grid)
    else:
        # Vertical
        for i in range(length):
            changed = changed | set_ship(x, y + i, grid)
        changed = changed | set_water(x, y - 1, grid)
        changed = changed | set_water(x, y + length, grid)
    return changed

def water_fill(grid):
    """
    Fills all unknown squares with water
    Returns True if anything changed
    """
    changed = False
    for x in range(grid.info.width):
        for y in range(grid.info.height):
            if grid.grid[x, y] == UNKNOWN:
                changed = True
                grid.grid[x, y] = WATER
    return changed

def countrow(row, setting):
    """Counts the number of a given setting in a row"""
    return np.count_nonzero(row==setting)

def validate(grid):
    """Make sure that the given grid is valid"""
    # Check to make sure the rows and columns are valid
    def valid_row(row, clue):
        if clue is None: return
        unknownCount = countrow(row, UNKNOWN)
        shipCount = countrow(row, SHIP)
        if shipCount + unknownCount < clue or shipCount > clue:
            raise Inconsistent()

    for x in range(grid.info.width):
        valid_row(grid.grid[x], grid.info.colclues[x])
    for y in range(grid.info.height):
        valid_row(grid.grid[:,y], grid.info.rowclues[y])

    # Check that the board doesn't have ships that are touching
    # Checking diagonals is sufficient
    for x in range(grid.info.width):
        for y in range(grid.info.height):
            if grid.grid[x, y] == SHIP:
                # Check diagonals that are below.
                # Above diagonals will have already triggered.
                if cell_is(x + 1, y + 1, SHIP, grid) or cell_is(x - 1, y + 1, SHIP, grid):
                    raise Inconsistent()

def find_holes(grid):
    """Returns a list of cells that are surrounded by water"""
    holes = []
    for y in range(grid.info.height):
        for x in range(grid.info.width):
            # Is this empty?
            if grid.grid[x, y] == UNKNOWN:
                # Check to see if there are any unknowns adjacent
                if cell_is(x-1, y, WATER, grid) and \
                   cell_is(x+1, y, WATER, grid) and \
                   cell_is(x, y+1, WATER, grid) and \
                   cell_is(x, y-1, WATER, grid):
                    holes.append((x, y))

    return holes

def simple_logic(puzzle):
    """Performs simple counting logic to see if each row and column can be filled"""
    rows = puzzle.state.info.height
    cols = puzzle.state.info.width

    # List of rows and columns that aren't fully solved
    rowlist = [True for i in range(rows)]
    collist = [True for i in range(cols)]

    changed = True
    while changed:
        changed = False

        # Run through all the columns
        for x in range(cols):
            # If already fully solved, move onto the next column
            if not collist[x]:
                continue

            # If the clue is unknown, there's nothing we can do
            clue = puzzle.state.info.colclues[x]
            if clue is None:
                collist[x] = False
                continue

            line = puzzle.state.grid[x]
            unknownCount = countrow(line, UNKNOWN)
            if unknownCount == 0:
                collist[x] = False
                continue

            shipCount = countrow(line, SHIP)
            if shipCount == clue:
                # Set the rest to water
                collist[x] = False
                changed = True
                for y in range(rows):
                    if line[y] == 0:
                        set_water(x, y, puzzle.state)
                continue

            waterCount = countrow(line, WATER)
            if waterCount + clue == len(line):
                # Set the rest to ships
                collist[x] = False
                changed = True
                for y in range(rows):
                    if line[y] == 0:
                        set_ship(x, y, puzzle.state)
                continue

        # Run through all the rows
        for y in range(rows):
            # If already fully solved, move onto the next row
            if not rowlist[y]:
                continue

            # If the clue is unknown, there's nothing we can do
            clue = puzzle.state.info.rowclues[y]
            if clue is None:
                rowlist[y] = False
                continue

            line = puzzle.state.grid[:,y]
            unknownCount = countrow(line, UNKNOWN)
            if unknownCount == 0:
                rowlist[y] = False
                continue

            shipCount = countrow(line, SHIP)
            if shipCount == clue:
                # Set the rest to water
                rowlist[y] = False
                changed = True
                for x in range(cols):
                    if line[x] == 0:
                        set_water(x, y, puzzle.state)
                continue

            waterCount = countrow(line, WATER)
            if waterCount + clue == len(line):
                # Set the rest to ships
                rowlist[y] = False
                changed = True
                for x in range(cols):
                    if line[x] == 0:
                        set_ship(x, y, puzzle.state)
                continue

def find_allowed(length, line, clue):
    """
    Finds allowed positions for a ship on a line
    Such positions must include the placement of a new ship tile
    """
    # Check the length isn't too long for the line
    if clue is not None and clue < length:
        return []
    # Check that there are still empty cells available
    unknowns = countrow(line, UNKNOWN)
    if unknowns == 0:
        return []

    result = []
    ships = countrow(line, SHIP)
    # Run through all possible start positions, and see if they're valid
    for start in range(0, len(line) - length + 1):
        # Check to make sure we're not making a longer ship than we want.
        if start > 0 and line[start - 1] == SHIP:
            continue
        if start + length < len(line) and line[start + length] == SHIP:
            continue
        # Is there water in the segment?
        segment = line[start:start + length]
        if WATER in segment:
            continue
        # How many unknowns are in the segment?
        unknowns = np.count_nonzero(segment == 0)
        if unknowns == 0:
            continue
        # Check to make sure we haven't put too many ships on this line.
        if clue is not None and ships + unknowns > clue:
            continue
        # Looks feasible. Add it to the list
        result.append(start)
    return result

def allowed_placement(placement, grid):
    """
    Check that we're allowed to place a ship at the given placement on the grid.
    Only return True if this placement actually places another ship piece.
    """
    tempgrid = grid.clone()
    try:
        # Check that the ship can be placed here
        changed = set_full_ship(placement, tempgrid)
        # Check that putting the ship here actually changes something
        if not changed:
            return False
        # Check that the resulting grid is valid
        validate(tempgrid)
        return True
    except Inconsistent:
        return False

def find_positions(grid, length):
    """
    Finds possible positions for a ship of a given length on the grid
    Only report positions that place a new ship segment
    """
    position_list = []

    # Search columns first
    for x in range(grid.info.width):
        mylist = find_allowed(length, grid.grid[x], grid.info.colclues[x])
        # We have a list of possible starting positions.
        # Make sure they're actually valid places to put a ship.
        for y in mylist:
            pos = ((x, y), length, False)
            if allowed_placement(pos, grid):
                position_list.append(pos)

    # Length 1 ships only need to have one of columns or rows searched
    if length > 1:
        # Search rows next
        for y in range(grid.info.height):
            mylist = find_allowed(length, grid.grid[:, y], grid.info.rowclues[y])
            # We have a list of possible starting positions that don't break the row.
            # Check which ones are actually valid.
            for x in mylist:
                pos = ((x, y), length, True)
                if allowed_placement(pos, grid):
                    position_list.append(pos)

    return position_list

def find_ships(grid):
    """
    Identify the position of all ships (both complete and incomplete) on the grid
    Assumes a valid grid

    Good ships are ones that are surrounded by water (length is known)
    Bad ships are ship segments whose final length is unknown
    """
    working = np.zeros_like(grid.grid)
    numships = 0

    # Run through the grid and number all ships
    for x in range(grid.info.width):
        for y in range(grid.info.height):
            if grid.grid[x, y] == SHIP:
                # Check to see if it's next to a known ship
                if x > 0 and working[x - 1, y] != 0:
                    working[x, y] = working[x - 1, y]
                    continue
                if y > 0 and working[x, y - 1] != 0:
                    working[x, y] = working[x, y - 1]
                    continue
                # Not next to a marked ship, so make a new ship
                numships += 1
                working[x, y] = numships

    # Find the lengths and positions of each ship, as well as if it's surrounded by water
    shiplengths = [0 for _ in range(numships)]
    shippos = [None for _ in range(numships)]  # top left corner of ship
    goodship = [True for _ in range(numships)]
    for x in range(grid.info.width):
        for y in range(grid.info.height):
            if working[x, y] > 0:
                if shiplengths[working[x, y] - 1] == 0:
                    shippos[working[x, y] - 1] = (x, y)
                shiplengths[working[x, y] - 1] += 1
                # Check to see if there are any unknowns adjacent
                if cell_is(x-1, y, UNKNOWN, grid) or \
                   cell_is(x+1, y, UNKNOWN, grid) or \
                   cell_is(x, y+1, UNKNOWN, grid) or \
                   cell_is(x, y-1, UNKNOWN, grid):
                    goodship[working[x, y] - 1] = False
    if numships > 0:
        longestship = max(shiplengths)
    else:
        longestship = 0

    shiphoriz = [True for _ in range(numships)]
    longestship = max(longestship, len(grid.info.ships))
    reportgood = [0 for i in range(longestship)]
    reportbad = [0 for i in range(longestship)]
    for i in range(numships):
        # Figure out the ship direction
        x, y = shippos[i]
        if cell_is(x, y+1, SHIP, grid):
            shiphoriz[i] = False
        # Add to the number of appropriate ship lengths
        if goodship[i]:
            reportgood[shiplengths[i] - 1] += 1
        else:
            reportbad[shiplengths[i] - 1] += 1

    # Make an inventory of each ship: ((x, y), length, horiz, surrounded)
    ships = [
             (shippos[i], shiplengths[i], shiphoriz[i], goodship[i])
             for i in range(numships)
            ]

    # Return all information
    return [reportgood, reportbad, ships]
