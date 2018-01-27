#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Word Search Solver

Usage:
python wordsearch.py file

wordsearch.txt is a sample file

Minimum word length is set in the code

Jolyon Bloomfield, January 2018
"""
import sys
from wordslib import find_words

print("Wordsearch")
if len(sys.argv) != 2:
    print("Usage:")
    print("python wordsearch.py filename")
    print("Example file: wordsearch.txt")
    sys.exit()

try:
    with open(sys.argv[1]) as f:
        puzzle = f.readlines()
except:
    print("Error reading in {}".format(sys.argv[1]))
    sys.exit()

gridx = len(puzzle[0])
gridy = len(puzzle)
minlength = 4

# Horizontal search
print("Horizontal words:")
for i in range(gridy):
    line = puzzle[i]
    results = find_words(line, minlength) + find_words(line[::-1], minlength)
    if results:
        print("Row {}".format(i + 1))
        print(results)

# Vertical search
print("\nVertical words:")
for i in range(gridx):
    line = "".join([puzzle[row][i] for row in range(gridy)])
    results = find_words(line, minlength) + find_words(line[::-1], minlength)
    if results:
        print("Column {}".format(i + 1))
        print(results)

# Diagonal search - down and right from top row
print("\nDiagonal words (down and right, count starts from bottom left corner):")
for i in range(gridy - 1, 0, -1):
    line = "".join([puzzle[i + col][col] for col in range(min(gridy - i, gridx))])
    results = find_words(line, minlength) + find_words(line[::-1], minlength)
    if results:
        print("Diagonal {}".format(gridy - i))
        print(results)
for i in range(gridx):
    line = "".join([puzzle[row][i + row] for row in range(min(gridx - i, gridy))])
    results = find_words(line, minlength) + find_words(line[::-1], minlength)
    if results:
        print("Diagonal {}".format(gridy + i))
        print(results)

# Diagonal search - down and left from top row
print("\nDiagonal words (down and left, count starts from top left corner):")
for i in range(gridx):
    line = "".join([puzzle[row][i - row] for row in range(min(i + 1, gridy))])
    results = find_words(line, minlength) + find_words(line[::-1], minlength)
    if results:
        print("Diagonal {}".format(i + 1))
        print(results)
for i in range(1, gridy):
    line = "".join([puzzle[i + col][gridx - col - 1] for col in range(min(gridy - i, gridx))])
    results = find_words(line, minlength) + find_words(line[::-1], minlength)
    if results:
        print("Diagonal {}".format(gridx + i))
        print(results)
