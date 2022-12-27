"""
This file contains functions used by AI when processes information
"""
import math
import time
import numpy as np

UP, DOWN, LEFT, RIGHT = range(4)

class AI():

    def get_move(self, board):
        best_move, _ = self.maximize(board)
        return best_move

    def eval_board(self, board, n_empty): 
        """
        Return the utility of the grid at given state. The utility itself includes 3 different components, which are empty_u(tility), smooth_u(tility), big_t_u(tility).
        empty_u represents for the contribution of empty cells at that state to the current utility
        smoothness_u represents for the "balance" of the current state
        """
        grid = board.grid

        utility = 0
        smoothness = 0

        big_t = np.sum(np.power(grid, 2))
        s_grid = np.sqrt(grid)
        smoothness -= np.sum(np.abs(s_grid[::,0] - s_grid[::,1]))
        smoothness -= np.sum(np.abs(s_grid[::,1] - s_grid[::,2]))
        smoothness -= np.sum(np.abs(s_grid[::,2] - s_grid[::,3]))

        smoothness -= np.sum(np.abs(s_grid[0,::] - s_grid[1,::]))
        smoothness -= np.sum(np.abs(s_grid[1,::] - s_grid[2,::]))
        smoothness -= np.sum(np.abs(s_grid[2,::] - s_grid[3,::]))
        
        empty_w = 100000 # Empty weight
        smoothness_w = 9 # Smootheness weight

        empty_u = n_empty * empty_w             # Empty utility 
        smooth_u = smoothness ** smoothness_w   # Smooth utility
        big_t_u = big_t                         # Big_t utility

        utility += big_t
        utility += empty_u
        utility += smooth_u

        # print((utility, empty_u, smooth_u, big_t_u))

        return (utility, empty_u, smooth_u, big_t_u)

    def maximize(self, board, depth = 0):
        moves = board.get_available_moves()
        moves_boards = []

        for m in moves:
            m_board = board.clone()
            m_board.move(m)
            moves_boards.append((m, m_board))

        max_utility = (float('-inf'),0,0,0)
        best_direction = None

        for mb in moves_boards:
            utility = self.chance(mb[1], depth + 1)

            if utility[0] >= max_utility[0]:
                max_utility = utility
                best_direction = mb[0]

        return best_direction, max_utility

    def chance(self, board, depth = 0):
        empty_cells = board.get_available_cells()
        n_empty = len(empty_cells)

        #if n_empty >= 7 and depth >= 5:
        #    return self.eval_board(board, n_empty)

        if n_empty >= 6 and depth >= 3:
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
if __name__ == "__main__":
    ai = AI()
    grid = np.array([[1,1,1,0], [1,1,1,0], [1,1,1,0], [1,1,1,0]])
    # s_grid = np.sqrt(grid)
    # print(s_grid)
    # print(np.sum(np.abs(s_grid[::,0] - s_grid[::,1])))
    
    print(ai.eval_board(grid, 4))
