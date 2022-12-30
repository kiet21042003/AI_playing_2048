import math
import time
import numpy as np

UP, DOWN, LEFT, RIGHT = range(4)

EMPTY_WEIGHT = 10**5
POTENTIAL_MERGES_WEIGHT = 10**4
MONOTONIC_R_WEIGHT = 10**3
MONOTONIC_C_WEIGHT = [1, 10**1, 10**2, 10**3]

SNAKE_WEIGHT_MATRIX = [[4**15, 4**14, 4**13, 4**12],
            [4**8, 4**9, 4**10, 4**11],
            [4**7, 4**6, 4**5, 4**4],
            [1, 4, 16, 64]]  # snake-shaped

weight_2 = [[4**6, 4**5, 4**4, 4**3],
            [4**5, 4**4, 4**3, 4**2],
            [4**4, 4**3, 4**2, 4],
            [64, 16, 4, 1]]  # symmetric


class AI():

    def get_move(self, board):
        best_move, _ = self.maximize(board)
        return best_move

    def eval_board(self, board, n_empty):
        grid = board.grid

        utility = 0
        potential_merges = 0
        num_of_mono_r = 0; num_of_mono_c = [0,0,0,0]
        pos_score = 0
        # Count the number of monotonic rows and columns
        for i in range(4):
            if ((grid[i][0]>=grid[i][1]) and (grid[i][1]>=grid[i][2]) and (grid[i][2]>=grid[i][3])) or\
                ((grid[i][0]<=grid[i][1]) and (grid[i][1]<=grid[i][2]) and (grid[i][2]<=grid[i][3])):
                num_of_mono_r += 1
            if ((grid[0][i]>=grid[1][i]) and (grid[1][i]>=grid[2][i]) and (grid[2][i]>=grid[3][i])) or\
                ((grid[0][i]<=grid[1][i]) and (grid[1][i]<=grid[2][i]) and (grid[2][i]<=grid[3][i])):
                num_of_mono_c[i] += 1
        # Count the number of possible merges
        potential_merges += np.count_nonzero(
            np.abs(grid[::, 0] - grid[::, 1]) == 0)
        potential_merges += np.count_nonzero(
            np.abs(grid[::, 1] - grid[::, 2]) == 0)
        potential_merges += np.count_nonzero(
            np.abs(grid[::, 2] - grid[::, 3]) == 0)

        potential_merges += np.count_nonzero(
            np.abs(grid[1, ::] - grid[2, ::]) == 0)
        potential_merges += np.count_nonzero(
            np.abs(grid[0, ::] - grid[1, ::]) == 0)
        potential_merges += np.count_nonzero(
            np.abs(grid[2, ::] - grid[3, ::]) == 0)

        for i in range(4):
            for j in range(4):
                pos_score += SNAKE_WEIGHT_MATRIX[i][j] * grid[i][j]

        empty_u = n_empty * EMPTY_WEIGHT
        potential_merges_u = potential_merges * POTENTIAL_MERGES_WEIGHT
        num_of_mono_u = num_of_mono_r * MONOTONIC_R_WEIGHT + np.sum(np.array(np.dot(num_of_mono_c, MONOTONIC_C_WEIGHT)))

        utility += empty_u
        utility += potential_merges_u
        utility += num_of_mono_u
        utility += pos_score

        return (utility, empty_u, potential_merges_u, num_of_mono_u)

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

        if depth >= 8:
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
    a = np.array([[1,2],[3,4]]) 
    b = np.array([[1,2],[3,4]]) 
    
    print(np.dot(a,b))

    
