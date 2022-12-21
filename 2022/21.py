from puzzle import Puzzle
import re


def add(a, b):
    return a+b


class Day21(Puzzle):

    def __init__(self):
        super().__init__(2022, 21)

    def get_func(self, operand):
        if operand == '+':
            func = lambda m1,m2: m1 + m2
            calc_m1 = calc_m2 = lambda res, m2: res - m2
        if operand == '-':
            func = lambda m1,m2: m1 - m2
            calc_m1 = lambda res, m2: res + m2
            calc_m2 = lambda res, m1: m1 - res
        if operand == '*':
            func = lambda m1,m2: m1 * m2
            calc_m1 = calc_m2 = lambda res, m2: res // m2
        if operand == '/':
            func = lambda m1,m2: m1 // m2
            calc_m1 = lambda res, m2: res * m2
            calc_m2 = lambda res, m1: m1 // res

        return func, calc_m1, calc_m2

    def shout(self, monkeys, monkey_id, humn_shout = None):
        if not humn_shout and monkey_id == 'humn':
            return None
        elif type(monkeys[monkey_id]) == int:
            return monkeys[monkey_id]

        m1, m2, operand = monkeys[monkey_id]

        func, _, _ = self.get_func(operand)

        m1_res = self.shout(monkeys, m1, humn_shout)
        m2_res = self.shout(monkeys, m2, humn_shout)
        if m1_res and m2_res:
            return func(m1_res, m2_res)

        return None

    def what_should_human_shout(self, monkeys, monkey_id, target):
        if monkey_id == 'humn':
            return target

        if type(monkeys[monkey_id]) == int:
            return None

        m1, m2, op = monkeys[monkey_id]
        func, calc_m1, calc_m2 = self.get_func(op)
        
        m1_res = self.shout(monkeys, m1)
        m2_res = self.shout(monkeys, m2)

        if not m1_res:
            return self.what_should_human_shout(monkeys, m1, calc_m1(target, m2_res))
        
        return self.what_should_human_shout(monkeys, m2, calc_m2(target, m1_res))


    def get_monkeys(self):
        monkeys = {}
        regex = r"([a-z]{4}): ([a-z]{4}|[0-9]+)( ([\+\-\*\/]) ([a-z]{4})|)"
        matches = re.finditer(regex, self._data, re.MULTILINE)

        for match in matches:
            monkey_id = match.group(1)
            op1 = match.group(2)

            if op1.isnumeric():
                monkeys[monkey_id] = int(op1)
                continue
            
            op2 = match.group(5)
            operand = match.group(4)

            monkeys[monkey_id] = (op1, op2, operand)
        
        return monkeys

    def solve_a(self):
        monkeys = self.get_monkeys()        
        print(monkeys)

        return self.shout(monkeys, "root", monkeys['humn'])

    def solve_b(self):
        monkeys = self.get_monkeys()

        m1, m2, _ = monkeys['root']

        m1_res = self.shout(monkeys, m1)
        m2_res = self.shout(monkeys, m2)

        if not m1_res:
            return self.what_should_human_shout(monkeys, m1, m2_res)
        
        return self.what_should_human_shout(monkeys, m2, m1_res)

SUBMIT = True
d = Day21()

if SUBMIT:
    d.submit()
else:
    d.init_data()
    #print(d.solve_a())
    print(d.solve_b())
