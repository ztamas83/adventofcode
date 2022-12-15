from typing import Any
from puzzle import Puzzle
from functools import cmp_to_key
import numpy as np

class Day13(Puzzle):
    def __init__(self) -> None:
        super().__init__(2022, 13)

    pair = []

    def read_pairs(self) -> tuple:
        pair = []
        for line in self._data.splitlines():
            if line.strip():
                pair.append(line)
            else:
                yield tuple(pair)
                pair.clear()

        yield tuple(pair)

    def parse(self, input: str, i = 0):
        data = ''
        parsed = []
        if i == 0 and input.startswith('['):
            input = input[1:][:-1]
        while i < len(input):
            if input[i] == '[':
                i, subdata = self.parse(input, i+1)
                parsed.append(subdata)
            elif input[i] == ']':
                if data:
                    parsed += [int(data)]
                    data = ''
                return i+1, parsed
            else:
                if input[i].isdigit():
                    data += input[i]

                if input[i] == ',' or i == len(input):
                    if data:
                        parsed += [int(data)]
                        data = ''
            
                i += 1
        if data:
            parsed += [int(data)]
            data = ''
        return i, parsed

    def compareint(self, i1, i2, prefix):
        print(f'{prefix} compare {i1} to {i2}')
        c1 = i1 if type(i1) == int else i1[0]
        c2 = i2 if type(i2) == int else i2[0]
        return c2 - c1

    def is_integer(self, data):
        return type(data) == int or (type(data) == list and len(data) == 1 and type(data[0]) == int)

    
    def compare(self, p1, p2, level = 0):
        prefix = "--"*level
        if self.is_integer(p1) and self.is_integer(p2) : #integers
            return self.compareint(p1, p2, prefix)
        
        if type(p1) == type(p2) == list:
            for i in range(max(len(p1), len(p2))):
                if i == len(p2): return -1 #right run out
                if i == len(p1): return 1 #left run out

                print(f'{prefix} compare {p1[i]} to {p2[i]}')
                cres = self.compare(p1[i], p2[i], level+1)
                
                print(f'{prefix} result {cres}')
                if cres:
                    return cres
        elif type(p1) == list:
            return self.compare(p1, [p2], level+1)
        elif type(p2) == list:
            return self.compare([p1], p2, level+1)
        return 0

    def solve_a(self):
        index_sum = 0
        for pair_index, pair in enumerate(self.read_pairs()):
            print(pair)
            _,p1 = self.parse(pair[0], 0)
            _,p2 = self.parse(pair[1], 0)
            
            result = self.compare(p1,p2, 0)
           
            print(f'result {result}')

            if result > 0:
                index_sum += (pair_index + 1)

        return index_sum

    def solve_b(self):
        distress2 = [[2]]
        distress6 = [[6]]
        
        all_signals = [distress2, distress6]
        for line in self._data.splitlines():
            if line.strip():
                all_signals.append(self.parse(line)[1])

        compare_func = cmp_to_key(self.compare)
        ordered_signals = sorted(all_signals, reverse=True, key = compare_func)
        
        finalvalue = 1

        for i,s in enumerate(ordered_signals):
            if s == distress2:
                finalvalue *= i+1
            if s == distress6:
                finalvalue *= i+1
                break
        
        return finalvalue
    

d = Day13()

#d.init_data()
#res = d.solve_a()
d.submit()
#assert(res == 13)
