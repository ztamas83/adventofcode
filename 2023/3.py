from puzzle import Puzzle
import re
import math

class DailyPuzzle(Puzzle):
    def __init__(self):
        super(DailyPuzzle, self).__init__(2023, 3)
        self.init_data(remote=True)
    
    
    def solve_a(self):
        sum = 0
        rowNum = 0
        lines: list[str] = list(map(lambda r: r.replace('.', 'x'), self._data.splitlines()))
        for row in lines:
            testrows = range(max(0, rowNum - 1), min(rowNum + 2, len(lines)))
            partnos = re.finditer('(\d+)', row)
            for m in partnos:
                found = False
                for testrow in testrows:
                    if found: break
                    search_in = lines[testrow][m.start()-1 if m.start()>0 else 0:m.end()+1 if m.end()<len(lines[testrow]) -1 else len(lines[testrow])]
                    print(f'Testing {m.group()} -> {search_in}')
                    if re.search('\W', search_in):
                        sum += int(m.group())
                        found = True
            rowNum+=1
    
        return sum
    
    def solve_b(self):
        sum = 0
        rowNum = 0
        lines: list[str] = list(map(lambda r: r.replace('.', 'x'), self._data.splitlines())) #all lines
        numbers_per_lines: dict[int, dict[int, list[int]]] = {}
        for row in lines:
            numbers_per_lines[rowNum] = {}
            
            for m in re.finditer('\d+', lines[rowNum]):
                found_number = int(m.group())
                if numbers_per_lines[rowNum].get(found_number):
                    numbers_per_lines[rowNum][found_number].extend(list(range(m.start(), m.end())))
                else:
                    numbers_per_lines[rowNum][found_number] = list(range(m.start(), m.end()))
            rowNum +=1
            
        rowNum = 0
        gearnogear = {True: 0, False: 0}
        for row in lines:
            testrows = range(max(0, rowNum - 1), min(rowNum + 2, len(lines))) # indices of rows to look at
            gears = re.finditer('\*', row)
            
            for g in gears:
                print(' -------- ')
                found = False
                min_x = max(g.start() - 1, 0)
                max_x = min(g.end(), len(lines[0])) # hope all lines are the same length
                check_x = set(range(min_x, max_x + 1))
                numbers_around = []
                
                for testrow_idx in testrows:
                    #print(f'Testing gear on line {rowNum} against row {testrow_idx} -> {numbers_per_lines[testrow_idx]} \n between positions {min_x} .. {max_x}')
                    for (k,v) in  numbers_per_lines[testrow_idx].items():
                        #if min_x in v or max_x in v:
                        if check_x.intersection(v):
                            numbers_around.append(k)
                    
                if len(numbers_around) == 2:
                    #print(f'This is a gear, found ratio: {numbers_around}')
                    sum += numbers_around[0] * numbers_around[1]
                    gearnogear[True] = gearnogear[True] + 1
                else:
                    for testrow_idx in testrows:
                        print(f'{lines[testrow_idx][max(min_x-3, 0):min(max_x+3, len(lines[testrow_idx]))]}')
                    print('Not a gear?')
                    gearnogear[False] = gearnogear[False] + 1
                    

            rowNum+=1
    
        print(gearnogear)
        return sum    
    
    def solve(self):
        return (self.solve_a(), self.solve_b())

solution = DailyPuzzle()
SUBMIT=False

print(solution.solve_a())
print(solution.solve_b())
if (SUBMIT):
    solution.submit()