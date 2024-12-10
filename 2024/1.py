import sys
import regex as re
import bisect

# setting path
from puzzle import Puzzle

SUBMIT = False
REMOTE = True


class Day1(Puzzle):
    def __init__(self):
        super(Day1, self).__init__(2024, 1)
        self.init_data(remote=REMOTE)

    def solve_a(self):
        sum = 0
        left_list = []
        right_list = []
        for line in self._data.splitlines():
            digits = re.findall(r"\d+", line)
            left_list.append(int(digits[0]))
            right_list.append(int(digits[1]))

        left_list.sort()
        right_list.sort()

        for pair in zip(left_list, right_list):
            distance = abs(pair[0] - pair[1])
            print(f"{pair} -> {distance}")
            sum = sum + distance

        return sum

    def solve_b(self):
        sum = 0
        left_list = []
        right_list = []
        for line in self._data.splitlines():
            digits = re.findall(r"\d+", line)
            left_list.append(int(digits[0]))
            right_list.append(int(digits[1]))

        similarity_score = {}
        left_list.sort()
        right_list.sort()

        for right in right_list:
            if similarity_score.get(right):
                similarity_score[right] += 1
                continue
            similarity_score[right] = 1

        for left in left_list:
            if similarity_score.get(left):
                print(f"{left} -> {similarity_score[left]}")
                sum += similarity_score[left] * left

        return sum

    def solve(self):
        return (self.solve_a(), self.solve_b())


solution = Day1()

# print(solution.solve_a())
print(solution.solve_b())
if SUBMIT:
    solution.submit()
