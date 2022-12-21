from puzzle import Puzzle
import numpy as np
from queue import Queue
import copy

SUBMIT = True
    
class Day20(Puzzle):
    def __init__(self):
        super().__init__(2022, 20)

    def solve_b(self):
        elements = [int(n) for n in self._data.split('\n')]
        multi = 811589153
        mixed = []
        for i in range(10):
            mixed, null_element = self.mix(elements, mixed, multi)
            print (mixed)

        null_pos = mixed.index(null_element)
        return sum(int(mixed[(null_pos + coord) % (len(mixed))][1]) for coord in [1000, 2000, 3000])

    def mix(self, elements, mixed = [], multi = 1):
        undef = (-1, -1)
        orig_elements = []
        for i,v in enumerate(elements):
            if v == 0:
                null_element = (i,v)
            orig_elements.append((i,v * multi))
        if not mixed:
            mixed = copy.deepcopy(orig_elements)

        max_index = len(mixed)
        while len(orig_elements) > 0:
            to_move = orig_elements.pop(0)
            orig_index = mixed.index(to_move)
            
            target_index = (orig_index + to_move[1]) % (max_index - 1)

            mixed.remove(to_move)
            #target_index = target_index - orig_index
            mixed = mixed[:target_index] + [to_move] + mixed[target_index:]
            if undef in mixed:
                mixed.remove(undef)
            #print([e[1] for e in mixed])

        print([e[1] for e in mixed])
        return mixed, null_element

    def solve_a(self):
        elements = [int(n) for n in self._data.split('\n')]
        
        mixed, null_element = self.mix(elements)
        
        null_pos = mixed.index(null_element)

        return sum(int(mixed[(null_pos + coord) % (len(mixed))][1]) for coord in [1000, 2000, 3000])

d = Day20()

if not SUBMIT:
    d.init_data()
    print(d.solve_a())
    print(d.solve_b())
else:
    d.submit()
