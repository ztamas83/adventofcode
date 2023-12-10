from copy import deepcopy
from puzzle import Puzzle
import re
import math

MOVES = {'L': 0, 'R': 1}

class DailyPuzzle(Puzzle):
    playing_with_joker = False
    def __init__(self):
        super(DailyPuzzle, self).__init__(2023, 8)
        self.init_data(remote=True)
        
    def solve_a(self):
        steps_taken = 0
        next = "AAA"
        instructions = self._data[0:self._data.index('\n')]
        nodes = {}
        for row in self._data.splitlines()[2:]:
            (node, nbL, nbR) = re.findall('[A-Z]{3}', row)
            nodes[node] = (nbL, nbR)
        
        current_step = 0
        while True:
            step_index = current_step % len(instructions)
            next = nodes[next][MOVES[instructions[step_index]]]
            current_step +=1
            if next == "ZZZ":
                return current_step
        
            
    def solve_b(self):
        next : list[str] = []
        instructions = self._data[0:self._data.index('\n')]
        nodes = {}
        for row in self._data.splitlines()[2:]:
            (node, nbL, nbR) = re.findall('[1-9A-Z]{3}', row)
            nodes[node] = (nbL, nbR)
            if str(node).endswith('A'):
                next.append(node)
        
        current_step = 0
        start_nodes = deepcopy(next)
        loops = {}
        while True:
            #print(next)
            step_index = current_step % len(instructions)
            
            next = list(map(lambda n: nodes[n][MOVES[instructions[step_index]]], next))
            current_step +=1
            
            for node in filter(lambda n: str(n).endswith('Z'), next):
                loops[start_nodes[next.index(node)]] = current_step
                if len(loops) == len(next):
                    return math.lcm(*list(loops.values()))
                
            if all(str(n).endswith('Z') for n in next):
                return current_step
        
        print(loops)
    
    def solve(self):
        return (self.solve_a(), self.solve_b())

solution = DailyPuzzle()
SUBMIT=False

print(solution.solve_b())

if (SUBMIT):
    solution.submit()