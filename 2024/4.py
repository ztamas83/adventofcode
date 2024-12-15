import re
import numpy as np

# setting path
from puzzle import Puzzle


SUBMIT = False
REMOTE = True


class Day(Puzzle):
    def __init__(self):
        super(Day, self).__init__(2024, 4)
        self.init_data(remote=REMOTE)

    def find_in_list(self, ls):
        print(f"Finding in: {ls}")
        hits = re.findall(r"(?=(XMAS|SAMX))", "".join(ls))
        print(f"Hits: {hits}")
        return len(hits)

    def find_sequence(self, arr):
        # Create a sliding window view of the array
        sum_hits = 0
        # horizontal
        row = 0
        while row < arr.shape[0]:
            curr = arr[row, :].tolist()
            hits = self.find_in_list(curr)
            if hits > 0:
                print(f"Found XMAS {hits} times: {curr}")
                sum_hits += hits
            row += 1

        return sum_hits

    def solve_a(self):
        sum = 0
        words = self._data.splitlines()
        array = np.zeros((len(words), len(words[0])), dtype=str)

        for row, data in enumerate(words):
            array[row, :] = list(data)

        sum = self.find_sequence(array)
        sum += self.find_sequence(array.T)

        # diagonals
        for i in range(0, array.shape[0]):
            diag = np.linalg.diagonal(array, offset=i)
            if len(diag) < 4:
                continue
            sum += self.find_in_list(np.linalg.diagonal(array, offset=i))
            sum += self.find_in_list(np.linalg.diagonal(np.flipud(array), offset=i))
            if i > 0:
                sum += self.find_in_list(np.linalg.diagonal(array, offset=-i))
                sum += self.find_in_list(
                    np.linalg.diagonal(np.flipud(array), offset=-i)
                )

            # sum += self.find_in_list(np.linalg.diagonal(np.flipud(array), offset=i))
            # sum += self.find_in_list(
            #     np.linalg.diagonal(np.fliplr(np.flipud(array)), offset=i)
            # )

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

print(f"Solution A: {solution.solve_a()}")
# print(f"Solution B: {solution.solve_b()}")
if SUBMIT:
    solution.submit(sub_a=True, sub_b=False)
