import re
import numpy as np

# setting path
from puzzle import Puzzle


SUBMIT = False
REMOTE = True


class Day(Puzzle):
    def __init__(self):
        super(Day, self).__init__(2024, 3)
        self.init_data(remote=REMOTE)

    def solve_a(self):
        sum = 0
        for line in self._data.splitlines():
            print(line)
            reg = r"mul\((\d{1,3}),(\d{1,3})\)"

            instructions = re.findall(reg, line)
            for instruction in instructions:
                print(instruction)
                sum += int(instruction[0]) * int(instruction[1])
        return sum

    def solve_b(self):
        sum = 0
        enabled = True
        for line in self._data.splitlines():
            print(line)
            reg = r"(do\(\)|don\'t\(\)|mul\((\d{1,3}),(\d{1,3})\))"

            instructions = re.findall(reg, line)
            for instruction in instructions:
                print(instruction)
                if instruction[0] == "don't()":
                    enabled = False
                if instruction[0] == "do()":
                    enabled = True

                if enabled and instruction[0].startswith("mul"):
                    sum += int(instruction[1]) * int(instruction[2])
        return sum

    def solve(self):
        return (self.solve_a(), self.solve_b())


solution = Day()

# print(f"Solution A: {solution.solve_a()}")
print(f"Solution B: {solution.solve_b()}")
if SUBMIT:
    solution.submit(sub_a=True, sub_b=False)
