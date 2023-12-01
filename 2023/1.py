import sys
import regex as re

# setting path
from puzzle import Puzzle

SUBMIT=False

DIGIT_DICT = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}


class Day1(Puzzle):
    def __init__(self):
        super(Day1, self).__init__(2023, 1)
        self.init_data(remote=True)
    
    def convert_digit(self, digit) -> int:
        if digit.isdigit():
            return int(digit)
        
        return DIGIT_DICT[digit]
            
    def solve_a(self):
        sum = 0
        for code in self._data.splitlines():
            digits = re.findall('[0-9]', code)
            if digits:
               value = 10 * int(digits[0]) + int(digits[len(digits)-1])
               print(f'{code} -> {digits} -> {value}')
               sum = sum + value
        return sum
            
    
    def solve_b(self):
        sum = 0
        for code in self._data.splitlines():
            # need overlapping matches because some words are like "oneight" -> '1' and '8' so the last is 8, not 1
            digits = re.findall('[0-9]|one|two|three|four|five|six|seven|eight|nine', code, overlapped=True )
            converted = list(map(lambda d: self.convert_digit(d), digits))
            
            if digits:
               value = 10 * int(converted[0]) + int(converted[len(converted)-1])
               print(f'{code} -> {digits} -> {converted} -> {value}')
               sum = sum + value
            else:
                print(f'{code}')
        return sum
        
    def solve(self):
        return (self.solve_a(), self.solve_b())

solution = Day1()

print(solution.solve_a())
print(solution.solve_b())
if (SUBMIT):
    solution.submit()