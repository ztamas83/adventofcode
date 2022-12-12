from puzzle import Puzzle
import re
import inspect
import numpy as np

class Monkey():
    def __init__(self, items, operator, value, test, ispass, isfail, modulo = 1):
        self._items: list[int]= items
        self._operation = eval(f'lambda old: old {operator} {value}')
#        inspect.getsource(self._operation)
        self._next_monkey = lambda i: ispass if i % test == 0 else isfail
        self.inspected: int = 0
        self._modulo: int = modulo
        self._testvalue = test

    def update_modulo(self, modulo):
        self._modulo = modulo
        
    def your_turn(self, worried = False) -> tuple[int,int] | None:
        unworry = 3 if not worried else 1
        for item in self._items:
            self.inspected += 1
            item = self._items.pop(0)
            #print(f'Monkey inspects an item with a worry level of {item}.')

            #print(inspect.getsource(self._operation))

            new_worry = (self._operation(item) // unworry) % self._modulo
            
            #print(f'.   Worry level increases {new_worry}.')
            
            return (self._next_monkey(new_worry), new_worry)

        return None
    
    def catch_item(self, value):
        self._items.append(value)
    

class Day11(Puzzle):
    def __init__(self):
        super(Day11, self).__init__(2022, 11)
        self.monkeys:list[Monkey] = []

    def init_monkeys(self):
        regex = r"Monkey ([0-9]):\n\s+Starting items: (.*)\n\s+Operation: new = (.*)\n\s+Test: divisible by (.*)\n.*([0-9])\n.*([0-9])"
        
        matches = re.finditer(regex, self._data, re.MULTILINE)

        for i, match in enumerate(matches, start=1):
            items = [int(x) for x in list(match.group(2).split(','))]
            operation = match.group(3)
            op = ''
            if '*' in operation:
                op = '*'
            elif '+' in operation:
                op = '+'
            
            parts = operation.split(op)
            test = int(match.group(4))
            ispass = int(match.group(5))
            isfail = int(match.group(6))
            
            if parts[1].strip() == 'old':
                val = 'old'
            if parts[1].strip().isdigit():
                val = int(parts[1])

            self.monkeys.append(Monkey(items, op, val, test, ispass, isfail))
        
        modulo = np.prod(list(map(lambda x: x._testvalue, self.monkeys)))
        for m in self.monkeys:
            m.update_modulo(modulo)
    
    def solve(self):
        self.init_monkeys()
        return (self.solve_a(), self.solve_b())
    
    def solve_a(self):
        return self.dont_worry_be_happy(20, False)
        
    def solve_b(self):
        return self.dont_worry_be_happy(10000, True)
        
    def _lcm(self, a, b):
        lcm = 1
        for num in range(1, max(a,b)):
            for i in range(2,num):
                if (num % i) == 0:
                    break
            else:
                if (a % num == 0) or (b % num == 0):
                    lcm *= num
        return lcm
        
    def dont_worry_be_happy(self, rounds, stillworry): 
        for i in range(rounds):
            if i % 1000 == 0:
                print(f'Current round {i}')
            for m in range(len(self.monkeys)):
                #print(f'Monkey {m} turn')

                result = self.monkeys[m].your_turn(stillworry)

                while result:
                    (to_monkey, item) = result 
                    #print(f'.   Item with {item} to {to_monkey}')
                    self.monkeys[to_monkey].catch_item(item)
                    result = self.monkeys[m].your_turn(stillworry)
        
        return np.prod(sorted(map(lambda m: m.inspected, self.monkeys))[-2:])
                

puzzle = Day11()
puzzle.init_data(True)
puzzle.init_monkeys()

# puzzle.submit()

result = puzzle.solve_b()
print(result)