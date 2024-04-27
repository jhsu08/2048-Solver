# 2048 Solver

## Description
This Python program is a solver for the popular game 2048. It uses the expectiminimax algorithm with alpha-beta pruning to make optimal moves in the game. The program provides a text-based interface for playing the game, displaying the current state of the board and suggesting the best move based on an AI algorithm. It also includes various heuristic functions to evaluate game states and make decisions accordingly.

The solver aims to achieve the highest possible score in the game by strategically merging tiles and reaching the 2048 tile. It provides a demonstration of how AI algorithms can be applied to solve complex puzzles and games.

## Usage
Run the program 'GameManager_3.py' and the game will automatically proceed. Each move and the resulting board by the AI player and the computer will be printed.

## Example
### Input:

python GameManager_3.py

### Output:
|   |   |   |   |
|---|---|---|---|
| 2 | 4 | 2 | 4 |
| 8 | 16 | 256 | 8 |
| 32 | 1024 | 32 | 512 |
| 4 | 128 | 16 | 2 |
|   |   |   |   |
                                

1024

## Implementation Details
### Expectiminimax & Alpha-Beta Pruning
The program uses the expectiminimax algorithm to evaluate possible moves at each game state. It also employs alpha-beta pruning to improve the efficiency of the search by eliminating branches that are guaranteed to be worse than previously examined moves.

### Move Time Limit
- Iterative deepening is used in order to ensure a best move can be made within the time limit.
- Before the time limit is up, the search depth is incremented each time all moves have been explored.
- If the time limit is exceeded, the current best move is returned.
- The move time limit is set at 0.15 seconds.

### Heuristics
- The tile value heuristic squares the value of the tile in order to encourage the merging of tiles to form larger tiles.
- Monotonicty gives rewards to moves that result in monotonically increasing tiles values.
- Empty cells count also encourages merging of tiles to create more space on the board by rewarding the number of empty cells.
- Since the heuristic scores are of different scales, the log of the scores is used to normalize them.
- Smoothness measures the difference in value between adjacent tiles
- Heuristic weights were determined from experimentation.

## Version used
- Python 3.11.6
