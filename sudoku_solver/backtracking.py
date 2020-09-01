def get_empty_cell(board, cell=(0, 0)):
    for i in range(cell[0], len(board)):
        for j in range(cell[1], len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None


def is_valid(board, cell=(0, 0), value=0):
    # check cell
    up_lft_cell = (cell[0] - cell[0] % 3, cell[1] - cell[1] % 3)
    for i in range(up_lft_cell[0], up_lft_cell[0] + 3):
        for j in range(up_lft_cell[1], up_lft_cell[1] + 3):
            if value == board[i][j]:
                return False

    # check row
    for i in range(len(board)):
        if value == board[cell[0]][i]:
            return False

    # check column
    for i in range(len(board[0])):
        if value == board[i][cell[1]]:
            return False
    return True


def solve(board):
    cell = get_empty_cell(board)
    if not cell:
        return True, board
    else:
        row, col = cell

    for i in range(1, 10):
        if is_valid(board, cell, i):
            board[row][col] = i

            if solve(board)[0]:
                return True, board

            board[row][col] = 0

    return False,


sudoku = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
          [6, 0, 0, 1, 9, 5, 0, 0, 0],
          [0, 9, 8, 0, 0, 0, 0, 6, 0],
          [8, 0, 0, 0, 6, 0, 0, 0, 3],
          [4, 0, 0, 8, 0, 3, 0, 0, 1],
          [7, 0, 0, 0, 2, 0, 0, 0, 6],
          [0, 6, 0, 0, 0, 0, 2, 8, 0],
          [0, 0, 0, 4, 1, 9, 0, 0, 5],
          [0, 0, 0, 0, 8, 0, 0, 7, 9]]
