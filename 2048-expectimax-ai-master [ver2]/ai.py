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
                       [4**0, 4**1, 4**2, 4**3]]  # snake-shaped

SYMMETRIC_WEIGHT_MATRIX = [[4**6, 4**5, 4**4, 4**3],
                           [4**5, 4**4, 4**3, 4**2],
                           [4**4, 4**3, 4**2, 4**1],
                           [4**3, 4**2, 4**1, 4**0]]  # symmetric

EDGE_EVALUATION_MATRIX = [[4**6, 4**5, 4**4, 4**3],
                          [4**5, 0, 0, 4**2],
                          [4**4, 0, 0, 4**1],
                          [4**3, 4**2, 4**1, 4**0]]

SPIRAL_MATRIX = [[4**15, 4**14, 4**13, 4**12],
                 [4**4, 4**3, 4**2, 4**11],
                 [4**5, 4**0, 4**1, 4**10],
                 [4**6, 4**7, 4**8, 4**9]]


class AI():

    def get_move(self, board):
        best_move, _ = self.maximize(board)
        return best_move

    def eval_board(self, board, n_empty):
        grid = board.grid

        utility = 0
        
        #Hàm của Tri nghĩ
        '''
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

        empty_u = a = n_empty * EMPTY_WEIGHT
        potential_merges_u = b = potential_merges * POTENTIAL_MERGES_WEIGHT
        num_of_mono_u = c = num_of_mono_r * MONOTONIC_R_WEIGHT + np.sum(np.array(np.dot(num_of_mono_c, MONOTONIC_C_WEIGHT)))

        utility += empty_u
        utility += potential_merges_u
        utility += num_of_mono_u
        utility += pos_score
        '''
        
        #Original function
        '''
        smoothness = 0

        big_t = np.sum(np.power(grid, 2))
        s_grid = np.sqrt(grid)
        smoothness -= np.sum(np.abs(s_grid[::,0] - s_grid[::,1]))
        smoothness -= np.sum(np.abs(s_grid[::,1] - s_grid[::,2]))
        smoothness -= np.sum(np.abs(s_grid[::,2] - s_grid[::,3]))
        smoothness -= np.sum(np.abs(s_grid[0,::] - s_grid[1,::]))
        smoothness -= np.sum(np.abs(s_grid[1,::] - s_grid[2,::]))
        smoothness -= np.sum(np.abs(s_grid[2,::] - s_grid[3,::]))
        
        empty_w = 100000
        smoothness_w = 3
        empty_u = b = n_empty * empty_w
        smooth_u = c = smoothness ** smoothness_w
        big_t_u = big_t = a
        
        utility += big_t
        utility += empty_u
        utility += smooth_u
        '''
        
        #Snake-shaped weight matrix function
        '''
        for i in range(4):
            for j in range(4):
                utility += SNAKE_WEIGHT_MATRIX[i][j] * grid[i][j]
        a, b, c = (0, 0, 0)
        '''
        
        #Symmetric weight matrix function
        '''
        for i in range(4):
            for j in range(4):
                utility += SYMMETRIC_WEIGHT_MATRIX[i][j] * grid[i][j]
        a, b, c = (0, 0, 0)
        '''
        
        #Edge evaluation matrix
        '''
        for i in range(4):
            for j in range(4):
                utility += EDGE_EVALUATION_MATRIX[i][j] * grid[i][j]
        a, b, c = (0, 0, 0)
        '''
        
        #Spiral matrix
        
        for i in range(4):
            for j in range(4):
                utility += SPIRAL_MATRIX[i][j] * grid[i][j]
        a, b, c = (0, 0, 0)
        
        
        return (utility, a, b, c)

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


    
