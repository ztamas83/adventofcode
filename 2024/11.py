import concurrent.futures
import math

# setting path
from puzzle import Puzzle


SUBMIT = False
REMOTE = True


class Day11(Puzzle):
    def __init__(self):
        super(Day11, self).__init__(2024, 11)
        self.init_data(remote=REMOTE)

    @staticmethod
    def number_of_digits(n: int) -> int:
        if n == 0:
            return 1
        return math.floor(math.log10(n)) + 1

    def mutate(self, stone: int):
        # print(f"Processing stone {stone}")
        if stone == 0:
            return 1

        digits = self.number_of_digits(stone)
        # print(f"Digits: {digits}")
        if digits % 2 == 0:
            left = stone // 10 ** (digits // 2)
            # print([left, stone - left * 10 ** (digits // 2)])
            return [left, stone - left * 10 ** (digits // 2)]

        return 2024 * stone

    def mutate_infinite(self, stones, iteration=1):
        if isinstance(stones, int):
            stones = [stones]

        print(f"Iteration {iteration}, no of stones: {len(stones)}")
        input("Press Enter to continue...")
        # print(f"Processing {stones} after making them a list")

        results = []

        with concurrent.futures.ThreadPoolExecutor(16) as executor:
            for r in executor.map(self.mutate, stones):
                if isinstance(r, list):
                    # stones[i, i + 1] = r
                    for i in range(0, len(r)):
                        results.append(r[i])
                else:
                    results.append(r)

        if iteration < 75:
            # print(results)
            result = self.mutate_infinite(results, iteration + 1)
        return result

    def solve_a(self):
        stones = [int(s) for s in self._data.split()]
        for i in range(1, 26):
            # print(f"Round {i}")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = []
                for r in executor.map(self.mutate, stones):
                    if isinstance(r, list):
                        # stones[i, i + 1] = r
                        results.append(r[0])
                        results.append(r[1])
                    else:
                        results.append(r)

                stones = results

                print(f"After blink {i}: {len(stones)}")

    def solve_b(self):
        stones = [int(s) for s in self._data.split()]
        sum = 0
        for s in stones:
            # print(f"Processing {s}")
            sum += len(list(self.mutate_infinite(s)))
            # print(f"Round {i}")

        return sum

    def solve(self):
        return (self.solve_a(), self.solve_b())


solution = Day11()

# print(solution.solve_a())
print(f"Solution: {solution.solve_b()}")
if SUBMIT:
    solution.submit()
