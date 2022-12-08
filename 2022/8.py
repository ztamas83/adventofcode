import numpy as np
from puzzle import Puzzle

SUBMIT = True

class Puzzle8(Puzzle):
    def __init__(self):
        super().__init__(2022, 8)

    def solve(self):
        data = self._data
        forest = np.array([(list(row.strip())) for row in data], dtype=int)
        forest = forest.reshape(forest.shape[0], forest.shape[1])
        visible = 0
        max_scenic_score = 0
        it = np.nditer(forest, flags=['multi_index'])
        for tree in it: #tree is array, why???
            #outermost is visible
            (row, col) = it.multi_index

            if row + 1 in [1, forest.shape[1]] or col + 1 in [1, forest.shape[0]]:
                visible += 1
                continue
            
            look_left = forest[row, :col]
            look_right = forest[row, col+1:]
            look_up = forest[:row, col]
            look_down = forest[row+1:, col]
        
            scenic_score_left = min([t for t in range(len(look_left)) if list(reversed(look_left))[t] >= it[0]], default = len(look_left) - 1) + 1
            scenic_score_right = min([t for t in range(len(look_right)) if look_right[t] >= it[0]], default = len(look_right) - 1) + 1
            scenic_score_up = min([t for t in range(len(look_up)) if list(reversed(look_up))[t] >= it[0]], default=len(look_up) - 1) + 1
            scenic_score_down = min([t for t in range(len(look_down)) if look_down[t] >= it[0]], default = len(look_down) - 1) + 1

            total_score = scenic_score_down * scenic_score_up * scenic_score_right * scenic_score_left
            if total_score > max_scenic_score:
                max_scenic_score = total_score

            print(f'{row}:{col} = {tree[...]}')
            if (max(look_left) < tree[...] #from left
                or max(look_right) < tree[...] #from right
                or max(look_up) < tree[...] #from up
                or max(look_down) < tree[...] #from down
                ):
                print(it[0], it.multi_index, ' is visible')
                visible += 1

        return (visible, max_scenic_score)

daily_puzzle = Puzzle8()

if SUBMIT:
    daily_puzzle.submit()
else:
    daily_puzzle.init_data()
    (answer_a, answer_b) = daily_puzzle.solve()
    assert(answer_a == 21)
    assert(answer_b == 8)