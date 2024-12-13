import re
import numpy as np
from math import isclose
import sys

# setting path
from puzzle import Puzzle


SUBMIT = False
REMOTE = True

COST_A = 3
COST_B = 1


class Day(Puzzle):
    def __init__(self):
        super(Day, self).__init__(2024, 13)
        self.init_data(remote=REMOTE)

    def find_min_a(self, machine, max=sys.maxsize, tolerance=1e-09):
        A = np.array(
            [
                [machine["A"]["x"], machine["B"]["x"]],
                [machine["A"]["y"], machine["B"]["y"]],
            ]
        )
        B = np.array([machine["Prize"]["x"], machine["Prize"]["y"]])
        a, b = np.linalg.solve(A, B)
        print(a, b)
        if (
            isclose(a, round(a), rel_tol=tolerance) and round(a) > 0 and round(a) <= max
        ) and (
            isclose(b, round(b), rel_tol=tolerance) and round(b) <= max and round(b) > 0
        ):
            solution = f"Button A: {int(a)}, Button B: {int(b)}"
            print(solution)
            return COST_A * a + COST_B * b

        print("No solution found (a, b):", a, b)
        return 0

    def solve_a(self):
        lines = self._data.splitlines()
        print(lines)
        machines = []

        for i in range(0, len(lines), 4):
            if i + 2 >= len(lines):
                break

            button_a_data = re.findall(r"Button A: X\+(\d+), Y\+(\d+)", lines[i])
            button_b_data = re.findall(r"Button B: X\+(\d+), Y\+(\d+)", lines[i + 1])
            prize_data = re.findall(r"Prize: X=(\d+), Y=(\d+)", lines[i + 2])

            if button_a_data and button_b_data:
                machine = {
                    "A": {"x": int(button_a_data[0][0]), "y": int(button_a_data[0][1])},
                    "B": {"x": int(button_b_data[0][0]), "y": int(button_b_data[0][1])},
                    "Prize": {"x": int(prize_data[0][0]), "y": int(prize_data[0][1])},
                }
                machines.append(machine)

        sum = 0
        for machine in machines:
            print(machine)
            sum += self.find_min_a(machine, 100)

        return sum

    def solve_b(self):
        lines = self._data.splitlines()
        print(lines)
        machines = []

        for i in range(0, len(lines), 4):
            if i + 2 >= len(lines):
                break

            button_a_data = re.findall(r"Button A: X\+(\d+), Y\+(\d+)", lines[i])
            button_b_data = re.findall(r"Button B: X\+(\d+), Y\+(\d+)", lines[i + 1])
            prize_data = re.findall(r"Prize: X=(\d+), Y=(\d+)", lines[i + 2])

            if button_a_data and button_b_data:
                machine = {
                    "A": {"x": int(button_a_data[0][0]), "y": int(button_a_data[0][1])},
                    "B": {"x": int(button_b_data[0][0]), "y": int(button_b_data[0][1])},
                    "Prize": {
                        "x": int(prize_data[0][0]) + 10000000000000,
                        "y": int(prize_data[0][1]) + 10000000000000,
                    },
                }
                machines.append(machine)

        sum = 0
        for machine in machines:
            print(machine)
            sum += self.find_min_a(machine, tolerance=1e-13)

        return sum

    def solve(self):
        return (self.solve_a(), self.solve_b())


solution = Day()

print(f"Solution A: {solution.solve_a()}")
print(f"Solution B: {solution.solve_b()}")
if SUBMIT:
    solution.submit(sub_a=True, sub_b=False)
