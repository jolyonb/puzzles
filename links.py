#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dancing links library

See https://arxiv.org/abs/cs/0011047 (Knuth)

Jolyon Bloomfield, January 2018
"""

class Cell(object):
    """Represents a cell containing a 1 in the dancing links algorithm"""

    def __init__(self, header, name):
        """Initialize the cell to only point to itself. header is the column header for the cell"""
        self.up = self
        self.down = self
        self.left = self
        self.right = self
        self.header = header
        self.name = name

class Column(Cell):
    """Represents a column header"""

    def __init__(self, name):
        """Initialize the sum to zero"""
        super(Column, self).__init__(self, name)
        self.sum = 0

class DLX(object):
    """Represents a dancing links matrix"""

    def __init__(self, numcols):
        """Initialize the dancling links matrix with a given number of columns"""
        # Start by making a root cell
        # This isn't part of the matrix, but it gives an entry point to the matrix
        # root.right is the first column header, root.left is the last
        # root.up and root.down just wrap around to itself
        root = Column("root")
        self.root = root
        self.numcols = numcols
        self.numrows = 0
        # Now make all of the column headers
        for col in range(numcols):
            c = Column("header-" + str(col))
            # Insert this column to the right side of the matrix
            root.left.right = c
            c.left = root.left
            c.right = root
            root.left = c

    def add_row(self, cols, name=None):
        """
        Add a row to the matrix.
        cols is a sorted list of the column numbers that have a 1, indexed from 0.
        """

        def get_header(col_current, col_shift):
            """
            Starting at the current column header, shift to the right col_shift times
            """
            header = col_current
            for i in range(col_shift):
                header = header.right
            return header

        # Update the number of rows
        self.numrows += 1
        if name is None:
            name = self.numrows

        # Get the first column header
        head = self.root.right
        head = get_header(head, cols[0])
        # Place the first cell
        cell = Cell(head, name)
        cell.up = head.up
        cell.down = head
        head.up.down = cell
        head.up = cell
        head.sum += 1
        oldcell = cell
        oldcol = cols[0]

        # Loop over all of the other entries
        for col in cols[1:]:
            # Shift to get the header
            head = get_header(head, col - oldcol)
            # Add in the cell
            cell = Cell(head, name)
            cell.up = head.up
            cell.down = head
            head.up.down = cell
            head.up = cell
            # Now add the left/right links
            cell.left = oldcell
            cell.right = oldcell.right
            cell.right.left = cell
            cell.left.right = cell
            # Add to the header sum
            head.sum += 1
            # Keep the old cell for reference
            oldcell = cell
            oldcol = col

    def remove_col(self, col_header):
        """
        Remove the specified column header from the header chain
        All rows that appear in this column are also removed
        """
        # Remove the column header from the header chain
        col_header.right.left = col_header.left
        col_header.left.right = col_header.right
        # Loop down through the column and remove the rows
        cell = col_header.down
        while cell != col_header:
            row_cell = cell.right
            # Move through all cells in this row and update their up/down links
            while row_cell != cell:
                row_cell.down.up = row_cell.up
                row_cell.up.down = row_cell.down
                row_cell.header.sum -= 1
                # Move on to the next cell in the row
                row_cell = row_cell.right
            # Move on to the next row
            cell = cell.down

    def unremove_col(self, col_header):
        """
        Adds the specified column header back into the header chain
        Also adds all rows that this column removed back in
        """
        # Add the column head back into the chain
        col_header.right.left = col_header
        col_header.left.right = col_header
        # Loop up through the column and add the rows back in
        # Doing this in exactly the reverse order of the removing ensures that we return
        # to the state we were in before the removal
        cell = col_header.up
        while cell != col_header:
            row_cell = cell.left
            # Move through all cells in this row and update their up/down links
            while row_cell != cell:
                row_cell.down.up = row_cell
                row_cell.up.down = row_cell
                row_cell.header.sum += 1
                # Move on to the next cell in the row
                row_cell = row_cell.left
            # Move on to the next row
            cell = cell.up

    def get_minimum_column(self):
        """
        Find the column that has the minimum number of cells in it to minimize branching
        Returning a column with 0 cells in it is ok - this gets dealt with in the solving
        loop
        """
        min_col = self.root.right
        current_col = min_col.right
        while current_col != self.root:
            if current_col.sum < min_col.sum:
                min_col = current_col
            # Move on to the next column
            current_col = current_col.right
        return min_col

    def solve(self, solution_rows):
        """Solve the exact cover problem recursively"""

        # Are we out of columns?
        # Can only occur if each column has been removed through row selection
        if self.root.right == self.root:
            # Construct a tuple of the rows in this solution
            soln = []
            for row in solution_rows:
                soln.append(row.name)
            # Add it to the list of solutions
            self.solutions.append(tuple(sorted(soln)))
            return

        # Choose the column with the minimum sum
        col = self.get_minimum_column()
        # Remove the column
        self.remove_col(col)
        # print("Chosen to remove column " + str(col.name))

        # Try adding each row in this column to the solution, one at a time
        row = col.down
        while row != col:
            # If there are no rows in this column, there is nothing to loop over here

            # Add to the solution
            solution_rows.append(row)
            # print("Trying row " + str(row.name))

            # Every column on this row needs to be removed
            cell = row.right
            while cell != row:
                self.remove_col(cell.header)
                cell = cell.right

            # Now try to solve
            self.solve(solution_rows)

            # Now add that row back in
            cell = row.left
            while cell != row:
                self.unremove_col(cell.header)
                cell = cell.left

            # Remove this row from the solution
            solution_rows.pop()
            # print("Removing row " + str(row.name))

            # Move on to the next row
            row = row.down

        # Add the column back in
        self.unremove_col(col)

    def run(self):
        """
        Runs the algorithm
        Returns a list of solutions: each solution is a tuple of the row numbers used
        """
        # Reset the list of solutions
        self.solutions = []
        # Start the solver with an empty list of rows
        self.solve([])
        return self.solutions


if __name__ == "__main__":
    # We use the following matrix:
    # (0 0 1 0 1 1 0) *
    # (1 0 0 1 0 0 1)
    # (0 1 1 0 0 1 0)
    # (1 0 0 1 0 0 0) *
    # (0 1 0 0 0 0 1) *
    # (0 0 0 1 1 0 1)
    # Three rows (with a star) form an eact cover

    # Construct the problem
    links = DLX(7)
    links.add_row([2,4,5], 1)
    links.add_row([0,3,6], 2)
    links.add_row([1,2,5], 3)
    links.add_row([0,3], 4)
    links.add_row([1,6], 5)
    links.add_row([3,4,6], 6)

    # Run the algorithm
    results = links.run()

    print(results)
