#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Framework for solving puzzles with guessing

Works by defining a puzzle state class, which stores state information,
and a puzzle solver class, which contains logic methods. Both classes
are abstract classes, but contain all of the information needed to make
a guess and continue solving. Only the storage definitions and logic
methods need to be written.

Two exceptions are defined: Inconsistent should be raised whenever the
logic methods find an inconsistent state. Solved should be raised whenever
the logic methods find a solved state. The PuzzleSolver class handles
both exceptions.

Jolyon Bloomfield, January 2018
"""
import abc

class Inconsistent(Exception):
    """Error raised when a state is found to be inconsistent"""

class Solved(Exception):
    """Error raised when a state is solved"""

class PuzzleState(abc.ABC):
    """Abstract base class that stores the present state of the puzzle"""

    @abc.abstractmethod
    def __init__(self, info):
        """
        Initialize a blank state, given the puzzle information.
        We recommend saving info.
        """
        self.info = info

    @abc.abstractmethod
    def clone(self):
        """Clones this state, returning a new copy"""

    @abc.abstractmethod
    def __str__(self):
        """Produce a string representation of the state (typically to be printed)"""

    @abc.abstractmethod
    def make_hash(self):
        """Make a hash of the puzzle state"""

class PuzzleSolver(abc.ABC):
    """Abstract base class that defines the logic to solve a puzzle"""

    # Stores the number of PuzzleSolvers created
    StateNum = 0

    def __init__(self, initstate, debug=False, max_depth=50,
                 solutionlist=None, hashes=None, parent=None, depth=0):
        """
        Initialize the puzzle solver with an initial state.
        - initstate is a PuzzleState object, describing the initial state
        - debug is a debug flag that prints decision information as the puzzle is solved
        - max_depth is the recursion limit

        All other flags are for internal use.
        - solutionlist is a list that solutions are stored in
        - hashes is an internal table of hashed states the solver has seen
        - parent links to the parent PuzzleSolver, so that any helper information can be
            inherited
        - depth indicates how deep we are in the recursion
        """
        self.state = initstate
        self.info = initstate.info
        self.parent = parent
        self.depth = depth
        self.max_depth = max_depth
        self.debug = debug

        # Store the solution list
        if solutionlist is None:
            self.solutionlist = []
        else:
            self.solutionlist = solutionlist

        # Hashes of states, used to ensure that we don't duplicate effort
        if hashes is None:
            self.hashes = set()
        else:
            self.hashes = hashes

        # Store the ID and increment StateNum
        self.id = PuzzleSolver.StateNum
        PuzzleSolver.StateNum += 1

    def solve(self):
        """Attempts to solve the puzzle"""

        # Do presolving (first time only)
        if self.depth == 0:
            self.debugout("Doing presolve")
            try:
                self.presolve()
            except Inconsistent:
                return
            except Solved:
                self.debugout("Solution found in presolving!")
                self.solutionlist.append(self.state)
                return

        while True:
            # Start by doing logic
            self.debugout("Depth {}: Doing logic".format(self.depth))
            try:
                # If logic doesn't raise an exception, then it returns
                # a list of guesses to try next
                self.guesslist, self.requiredguesses = self.logic()
            except Inconsistent:
                # Inconsistent
                return
            except Solved:
                # Found a solution!
                solhash = self.state.make_hash()
                if solhash not in self.hashes:
                    self.debugout("Depth {}: Solution found!".format(self.depth))
                    self.solutionlist.append(self.state)
                    self.hashes.add(solhash)
                else:
                    self.debugout("Depth {}: Duplicate solution found".format(self.depth))
                return

            # Check to see if we've already explored this path
            currenthash = self.state.make_hash()
            if currenthash in self.hashes:
                self.debugout("Depth {}: Already tried this path".format(self.depth))
                return
            self.hashes.add(currenthash)

            # Logic has failed us, we need to guess
            # Are we at our depth limit?
            if self.depth == self.max_depth:
                self.debugout("Hit depth limit")
                return

            self.debugout("Depth {}: Status before making a guess list".format(self.depth))
            self.debugout(str(self.state))
            self.debugout("Depth {}: Made a guess list:".format(self.depth), self.guesslist)

            # Run each guess in turn
            for idx, guess in enumerate(self.guesslist):
                if idx + self.requiredguesses == len(self.guesslist):
                    # Because the minimum number of applied guesses is up, all of the
                    # remaining guesses in the list need to apply together
                    # Go and apply them all, then revert to logic.
                    self.debugout("Depth {}: Applying last {} guesses:".format(self.depth, self.requiredguesses))
                    try:
                        for i in range(idx, len(self.guesslist)):
                            self.debugout("Depth {}: Applying ".format(self.depth), self.guesslist[i])
                            self.apply_guess(self.guesslist[i])
                    except Inconsistent:
                        self.debugout("Depth {}: Inconsistent".format(self.depth))
                        return
                    self.debugout("Depth {}: All applied consistently".format(self.depth))
                    break

                # Make a PuzzleSolver clone
                solver = self.clone()

                # Apply the guess
                self.debugout("Depth {}: Try this guess:".format(self.depth), guess)
                try:
                    solver.apply_guess(guess)
                    self.guess = idx
                    # And give it a solve!
                    solver.solve()
                    self.debugout("Depth {}: Done with guess:".format(self.depth), guess)
                except Inconsistent:
                    pass

                # We can now assume that this guess is incorrect
                # Apply any after-guess instructions
                if self.afterguess(guess):
                    # If returned true, something's changed, and we should go back to logic
                    break
                else:
                    # Otherwise, move onto the next guess
                    continue
            else:
                # We're out of guesses
                return

    def clone(self):
        """Make a new PuzzleState that is a clone of this object"""
        return self.__class__(self.state.clone(),
                              solutionlist=self.solutionlist,
                              hashes=self.hashes,
                              parent=self,
                              depth=self.depth + 1,
                              max_depth=self.max_depth,
                              debug=self.debug)

    def debugout(self, *args):
        """Outputs text if debug flag is set"""
        if self.debug:
            print(*args)

    @abc.abstractmethod
    def logic(self):
        """
        Perform logical operations on the current state to solve the puzzle
        as much as possible.

        Raises Solved if solved
        Raises Inconsistent if inconsistent

        Otherwise, returns a tuple (guesslist, requirednum) which contains a list of
        guesses to make, and the number of these guesses that must simultaneously apply.
        """

    @abc.abstractmethod
    def apply_guess(self, guess):
        """
        Apply the given guess.
        Raises Inconsistent if the guess is inconsistent.
        """

    def afterguess(self, guess):
        """
        Instruct the solver what to do after trying a guess.
        Return True to return to logic (typically after updating the state).
        """
        return False

    def presolve(self):
        """
        Routine that is called before any solving starts.
        Raises Inconsistent for an inconsistent state.
        Raises Solved if presolving solves the entire puzzle.
        """
