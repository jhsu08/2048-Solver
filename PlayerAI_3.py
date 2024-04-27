from BaseAI_3 import BaseAI
import numpy as np
import time

time_limit = 0.15

class PlayerAI(BaseAI):

    def getMove(self, grid):
        self.prevTime = time.process_time()
        self.depth = 0
        self.over = False
        best_move = None
        best_utility = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        
        while not self.over:

            self.updateTime(time.process_time()) # update state of clock
            self.depth += 1 # iterative deepening

            available_moves = grid.getAvailableMoves()

            for move, new_grid in available_moves:
                utility = self.expectiminimax(new_grid, depth = self.depth, alpha = alpha, beta = beta, is_max_player = False)
                if utility > best_utility:
                    best_utility = utility
                    best_move = move
                alpha = max(alpha, best_utility)
            
            if self.over:
                break
                
        return best_move

    def updateTime(self, current_time):
        """Helper function to update the time"""
        if current_time - self.prevTime > time_limit:
            self.over = True
        
    def expectiminimax(self, grid, depth, alpha, beta, is_max_player):
        """Expectiminimax with alpha-beta pruning"""

        # base case when leaf is reached
        if depth == 0 or not grid.canMove():
            # evaluate grid using heuristic function
            return self.evaluate(grid)

        # maximizing player
        if is_max_player:
            max_utility = float("-inf")
            for _, new_grid in grid.getAvailableMoves():
                utility = self.expectiminimax(new_grid, depth - 1, alpha, beta, False)
                max_utility = max(max_utility, utility)
                
                # update time limit
                self.updateTime(time.process_time())
                if self.over:
                    return float("inf")
                
                # beta cut-off
                if max_utility > beta:
                    break
                
                # update alpha
                alpha = max(alpha, max_utility)

            return max_utility
        
        # minimizing playing
        else:
            min_utility = float("inf")
            empty_cells = grid.getAvailableCells()
            
            for cell in empty_cells:

                # 90% chance 2 is the next tile
                next_is_2 = grid.clone()
                next_is_2.insertTile(cell, 2)
                utility = 0.9 * self.expectiminimax(next_is_2, depth - 1, alpha, beta, True)
                
                # update time limit
                self.updateTime(time.process_time())
                if self.over:
                    return float("-inf")

                # 10% chance 4 is the next tile
                next_is_4 = grid.clone()
                next_is_4.insertTile(cell, 4)
                utility += 0.1 * self.expectiminimax(next_is_4, depth - 1, alpha, beta, True)
                
                # update time limit
                self.updateTime(time.process_time())
                if self.over:
                    return float("-inf")

                # find the minimum utility
                min_utility = min(utility, min_utility)
                if min_utility < alpha:
                    break  # alpha cut-off
                beta = min(beta, min_utility)

            return min_utility
        
    # def adjacency(self, grid):
    #     """Heuristic to penalize when neighboring tiles have large differences"""
    #     score = 0
    #     for i in range(4):
    #         for j in range(3):
    #             if grid.map[i][j] == grid.map[i][j+1]:
    #                 score += 1
        
    #     for j in range(4):
    #         for i in range(3):
    #             if grid.map[i][j] == grid.map[i+1][j]:
    #                 score += 1

    #     return score

    def smoothness(self, grid):
        """Heuristic to penalize when neighboring tiles have large differences"""
        score = 0
        # calculate smoothness in the y-direction
        for i in range(4):
            for j in range(3):
                score += abs(grid.map[i][j] - grid.map[i][j+1])

        # calculate smoothness in the x-direction
        for j in range(4):
            for i in range(3):
                score += abs(grid.map[i][j] - grid.map[i+1][j])

        return score

    def monotonicity(self, grid):
        """Heuristic to encourage values to increase monotonically in both the x and y directions"""
        score = 0
        # calculate monotonicity in the x-direction
        for i in range(4):
            for j in range(3):
                # next tile is greater than or equal to current tile's value
                if grid.map[i][j] <= grid.map[i][j+1]:
                    score += 1

        # calculate monotonicity in the y-direction
        for j in range(4):
            for i in range(3):
                # next tile is greater than or equal to current tile's value
                if grid.map[i][j] <= grid.map[i+1][j]:
                    score += 1

        return score
    
    def tile_values(self, grid):
        """Heuristic to encourage larger tile values"""
        score = 0
        for i in range(4):
            for j in range(4):
                # squaring the tile value gives more weight to larger tiles
                score += grid.map[i][j] ** 2
        
        return score
    
    def evaluate(self, grid):

        # heuristic weights
        (w1, w2, w3, w4) = (1, 1, 3, 1)

        # take the log of the different heuristics to normalize values
        tile_values = np.log(self.tile_values(grid)+1)
        monotonicity = np.log(self.monotonicity(grid)+1)
        empty_cells = np.log(len(grid.getAvailableCells())+1) # this heuristic encourages tiles to be combined
        smoothness = np.log(self.smoothness(grid)+1)

        # weighted sum of heuristic components
        weighted_sum = w1 * tile_values + w2 * monotonicity + w3 * empty_cells + w4 * smoothness

        return weighted_sum
