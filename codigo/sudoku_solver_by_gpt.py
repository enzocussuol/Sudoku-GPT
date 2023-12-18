def solve_sudoku(board):
    """
    Solves a Sudoku puzzle using a backtracking algorithm.

    Parameters:
    board: A 9x9 numpy array representing the Sudoku puzzle, with unknown values represented by 0.

    Returns:
    A 9x9 numpy array representing the solved Sudoku puzzle.
    """

    # Find an unassigned cell
    for row in range(9):
        for col in range(9):
            if board[row, col] == 0:
                # Try each possible value for the cell
                for value in range(1, 10):
                    # Check if the value is valid
                    if is_valid(board, row, col, value):
                        # Assign the value to the cell
                        board[row, col] = value

                        # Recursively solve the rest of the puzzle
                        solved_board = solve_sudoku(board)

                        # If the puzzle is solved, return the solution
                        if solved_board is not None:
                            return solved_board

                        # If the puzzle is not solved, reset the cell to 0 and continue searching
                        board[row, col] = 0

                # If no valid value was found for the cell, return None to indicate that the puzzle is unsolvable
                return None

    # If all cells are assigned, the puzzle is solved
    return board

def is_valid(board, row, col, value):
    """
    Checks if a value is valid for a given cell in a Sudoku puzzle.

    Parameters:
    board: A 9x9 numpy array representing the Sudoku puzzle.
    row: The row of the cell to check.
    col: The column of the cell to check.
    value: The value to check.

    Returns:
    True if the value is valid, False otherwise.
    """

    # Check if the value is already in the row
    for i in range(9):
        if board[row, i] == value:
            return False

    # Check if the value is already in the column
    for j in range(9):
        if board[j, col] == value:
            return False

    # Check if the value is already in the 3x3 block
    block_row = row // 3
    block_col = col // 3
    for i in range(block_row * 3, block_row * 3 + 3):
        for j in range(block_col * 3, block_col * 3 + 3):
            if board[i, j] == value:
                return False

    # If the value is not in the row, column, or 3x3 block, it is valid
    return True