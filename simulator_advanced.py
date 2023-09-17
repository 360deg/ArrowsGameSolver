def get_available_cells(board, last_move, direction):
    available_cells = []
    row, col = last_move

    def all_non_empty_cells():
        return [(r, c) for r in range(len(board)) for c in range(len(board[r])) if board[r][c] != 0]

    def left():
        return [(row, c) for c in range(col - 1, -1, -1) if board[row][c] != 0]

    def right():
        return [(row, c) for c in range(col + 1, len(board[row])) if board[row][c] != 0]

    def top():
        return [(r, col) for r in range(row - 1, -1, -1) if board[r][col] != 0]

    def bottom():
        return [(r, col) for r in range(row + 1, len(board)) if board[r][col] != 0]

    def horizontal():
        return left() + right()

    def vertical():
        return top() + bottom()

    def all_directions():
        return left() + right() + top() + bottom()

    switcher = {
        -1: all_non_empty_cells,
        0: lambda: [],
        1: left,
        2: right,
        3: top,
        4: bottom,
        5: horizontal,
        6: vertical,
        7: all_directions
    }

    available_cells = switcher.get(direction, lambda: [])()
    return available_cells


def simulate_moves(board, depth, cell_to_click):
    sequences = []
    row, col = cell_to_click

    def simulate(current_board, last_move, current_sequence, depth_remaining):
        direction = current_board[last_move[0]][last_move[1]]
        available_moves = get_available_cells(current_board, last_move, direction)

        if depth_remaining == 0 or len(available_moves) == 0:
            sequences.append(current_sequence)
            return

        current_board[last_move[0]][last_move[1]] = 0

        for move in available_moves:
            board_copy = [row.copy() for row in current_board]
            simulate(board_copy, move, current_sequence + [move], depth_remaining - 1)

    simulate(board, (row, col), [(row, col)], depth)

    return sequences

