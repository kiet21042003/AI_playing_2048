import numpy as np

UP, DOWN, LEFT, RIGHT = range(4)

SNAKE_WEIGHT_MATRIX = [[10**15, 10**14, 10**13, 10**12],
                        [10**8, 10**9, 10**10, 10**11],
                        [10**7, 10**6, 10**5, 10**4],
                        [10**0, 10**1, 10**2, 10**3]]

MAX_DEPTH = 2

class AI():

    def get_move(self, board):
        best_move, _ = self.maximize(board)
        return best_move

    def eval_board(self, board, n_empty):
        grid = board.grid

        pos_score = 0
        for i in range(4):
            for j in range(4):
                pos_score += SNAKE_WEIGHT_MATRIX[i][j] * grid[i][j]

        return (pos_score, 0, 0, 0)

    def maximize(self, board, depth=0):
        moves = board.get_available_moves()
        moves_boards = []

        for m in moves:
            m_board = board.clone()
            m_board.move(m)
            moves_boards.append((m, m_board))

        max_utility = (float('-inf'), 0, 0, 0)
        best_direction = None

        for mb in moves_boards:
            utility = self.chance(mb[1], depth + 1)

            if utility[0] >= max_utility[0]:
                max_utility = utility
                best_direction = mb[0]

        return best_direction, max_utility

    def chance(self, board, depth=0):
        empty_cells = board.get_available_cells()
        n_empty = len(empty_cells)

        if depth >= MAX_DEPTH:
           return self.eval_board(board, n_empty)

        if n_empty >= 6 and depth >= 2:
            return self.eval_board(board, n_empty)

        if n_empty >= 0 and depth >= 5:
            return self.eval_board(board, n_empty)

        if n_empty == 0:
            _, utility = self.maximize(board, depth + 1)
            return utility

        possible_tiles = []

        chance_2 = (.9 * (1 / n_empty))
        chance_4 = (.1 * (1 / n_empty))

        for empty_cell in empty_cells:
            possible_tiles.append((empty_cell, 2, chance_2))
            possible_tiles.append((empty_cell, 4, chance_4))

        utility_sum = [0, 0, 0, 0]

        for t in possible_tiles:
            t_board = board.clone()
            t_board.insert_tile(t[0], t[1])
            _, utility = self.maximize(t_board, depth + 1)

            for i in range(4):
                utility_sum[i] += utility[i] * t[2]

        return tuple(utility_sum)


if (__name__ == "__main__"):
    print("This is the code for the used AI")

    
