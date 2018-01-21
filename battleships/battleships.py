#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Battleships/Bimaru solver

Run as:
python battleships.py puzzle.dat
See below for description of file format for puzzles

Jolyon Bloomfield, Jan 2018
"""
import sys
from battleshiplib import Inconsistent, run, combine_grids

print("**************************************************************")
print("*                     Battleships Solver                     *")
print("**************************************************************")


### OBTAIN PUZZLE FROM FILE ###

# The file format is as follows:
# Any line starting with a # is ignored
# row clues (comma separated, may contain ?)
# column clues (comma separated, may contain ?)
# number of each length of ship (comma separated, starts with smallest ship)
# initial information (optional, as "x, y, information")

# As an example:
"""
# Row clues
2, 1, 3, 0, 2, 3, 1, 3, 0, 5
# Column clues
3, 1, 2, 0, 2, 1, 2, 6, 1, 2
# Number of Ships (shortest first)
4, 3, 2, 1
# Initial information: x, y, information
# Positions start at (0, 0) in the top left corner, given as (x, y)
# w = water
# o = one-length boat
# # = boat (unknown piece)
# <, >, ^, v, boat ends
5, 0, o
1, 2, <
9, 4, o
1, 5, w
2, 9, o
6, 9, <
"""

# Get the command line argument
try:
    filename = sys.argv[1]
except:
    print("Specify the puzzle file to solve as a command line argument. Eg, puzzle1.dat")
    sys.exit()

# Get the data out of that file
data = []
try:
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if len(line) > 0 and line[0] != "#":
                data.append(line)
except:
    print("Unable to read", filename)
    sys.exit(1)

# Interpret the data
if len(data) < 3:
    print("File does not seem to describe a puzzle")
    sys.exit()
# Extract row clues
rowclues = data[0].split(",")
rowclues = map(lambda x: x.strip(), rowclues)
rowclues = [int(i) if i != "?" else None for i in rowclues]
# Extract column clues
colclues = data[1].split(",")
colclues = map(lambda x: x.strip(), colclues)
colclues = [int(i) if i != "?" else None for i in colclues]
# Extract number of ships
ships = data[2].split(",")
ships = map(lambda x: x.strip(), ships)
ships = list(map(int, ships))
# Extract initial information
initinfo = []
for i in data[3:]:
    tokens = i.split(",")
    tokens = list(map(lambda x: x.strip(), tokens))
    if len(tokens) != 3:
        print("Unable to interpret line:", i)
        sys.exit(1)
    x, y, value = tokens
    initinfo.append((int(x), int(y), value))


### SOLVE THE PUZZLE ###

try:
    results, guesses = run(rowclues, colclues, initinfo, ships, debug=False)
    print()
except Inconsistent:
    print("Unable to solve.")
else:
    # Print all solutions
    if len(results) == 0:
        print("Unable to find any solutions (used {} guesses).".format(guesses))
    elif len(results) == 1:
        print("Found a unique solution in {} guesses.".format(guesses))
        print()
        results[0].pretty_print()
    else:
        for idx, soln in enumerate(results):
            print("Solution #{}:".format(idx+1))
            soln.pretty_print()
            print()
        print("Found {} solutions in {} guesses.".format(len(results), guesses))
        print()

        # Now combine all solutions
        combinedgrid = results[0].grid
        for sol in results[1:]:
            combinedgrid = combinedgrid & sol.grid
        print("The cells that all solutions have in common are the following:")
        combine_grids(results).pretty_print()
