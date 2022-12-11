from puzzle import Puzzle
import numpy as np

class Day10(Puzzle):
    def __init__(self):
        super(Day10, self).__init__(2022, 10)

    def solve(self):
        screen = np.matrix(['.']*240)
        screen = screen.reshape(6,40)
        cycle = 0
        to_do = (0, 0)
        reg1 = 1
        sprite = [reg1 - 1, reg1, reg1 + 1]
        signal_strength = []
        inst_it = iter([l.strip().split(' ') for l in self._data])
        while True:
            cycle += 1
    
            row = (cycle // 40) % 6
            col = (cycle - 1)  % 40
            
            if to_do[0] == cycle:
                reg1 += to_do[1]
                sprite = [reg1 - 1, reg1, reg1 + 1]
                to_do = (0,0)

            if col in sprite:
                screen[row,col] = '#'
                print (screen[row,])

            if cycle>=20 and (cycle-20) % 40 == 0:
                signal_strength.append(reg1 * cycle)

            if to_do[0] > cycle:
                continue
            
            try:
                inst = next(inst_it)
                
                match inst[0]:
                    case 'noop':
                        to_do = (cycle + 1, 0)
                    case 'addx':
                        to_do = (cycle + 2, int(inst[1]))
                        
            except Exception as e:
                print(e)
                break

        return sum(signal_strength), screen

puzzle = Day10()
# puzzle.submit(sub_b=False)
puzzle.init_data(True)
res, screen = puzzle.solve()
print(screen)
#assert(res == 13140)

