from copy import deepcopy
from puzzle import Puzzle
import re
import math

MOVES = {'L': 0, 'R': 1}

class DailyPuzzle(Puzzle):
    playing_with_joker = False
    def __init__(self):
        super(DailyPuzzle, self).__init__(2023, 9)
        self.init_data(remote=True)
        
        
    def calc_reduction(self, row, sum, reversed=False):
        reduction = []
        for idx in range(0, len(row) - 1):
            red_value = row[idx + 1] - row[idx]
            reduction.append(red_value)
        
        if all(x == 0 for x in reduction):
            return sum
        
        if reversed:
            return sum - self.calc_reduction(reduction, reduction[0], True)
        return sum + self.calc_reduction(reduction, reduction[-1])
    
    def calc_reduction_backwards(self, row, diff):
        reduction = []
        for idx in reversed(range(1, len(row))):
            red_value = row[idx] - row[idx-1]
            reduction.insert(0, red_value)
        
        if all(x == 0 for x in reduction):
            return sum
        
        return diff - self.calc_reduction_backwards(reduction, reduction[0])
        
    def solve_a(self):
        sum = 0
        for row in self._data.splitlines():
            history = list(map(lambda n: int(n.strip()), row.split(' ')))
            sum = self.calc_reduction(history, history[-1])
            #print(f'predicted: {self.calc_reduction(history, history[-1])}')
        return sum
    
    def solve_b(self):
        sum = 0
        for row in self._data.splitlines():
            history = list(map(lambda n: int(n.strip()), row.split(' ')))
            sum += self.calc_reduction(history, history[0], True)
            print(f'predicted: {self.calc_reduction(history, history[0], True)}')
        return sum
    # def solve_a(self):
    #     for row in self._data.splitlines():
    #         history = list(map(lambda n: int(n.strip()), row.split(' ')))
    #         reductions = list([history])
    #         red_idx = 0
    #         while True:
    #             allzero = True
    #             reductions.append([])
    #             if (red_idx > 0):
    #                 pred_value = reductions[red_idx][-1] + reductions[red_idx - 1][-1]
    #                 reductions[red_idx - 1].append(pred_value)
    #             for idx in range(0, len(reductions[red_idx]) - 1):
    #                 red_value = reductions[red_idx][idx + 1] - reductions[red_idx][idx]
    #                 if red_value != 0:
    #                     allzero = False
    #                 reductions[red_idx + 1].append(red_value)
    #             red_idx += 1
    #             if allzero:
    #                 print(f'Predicted value: {reductions[0][-1]}')
    #                 break
            
            # prediction = list(reversed(reductions))
            # for idx in range(0, len(prediction)-1):
            #     prediction[idx + 1].append(prediction[idx][-1] + prediction[idx + 1][-1])
            # print(prediction[-1][-1])
            
   
    def solve(self):
        return (self.solve_a(), self.solve_b())

solution = DailyPuzzle()
SUBMIT=False

print(solution.solve_b())

if (SUBMIT):
    solution.submit()