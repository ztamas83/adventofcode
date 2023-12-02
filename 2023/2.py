from puzzle import Puzzle
import re
import math

limits = {'red':12, 'green':13, 'blue':14}
class DailyPuzzle(Puzzle):
    def __init__(self):
        super(DailyPuzzle, self).__init__(2023, 2)
        self.init_data(remote=True)
    
    def get_cubes(self, game: str) -> tuple[int, list[tuple[int, str]]]: # 3 red, 4 green
        matches = re.findall('((Game (\d+): )|(\d+ (?:red|green|blue)))', game)
        return (int(matches[0][2]), list(map(lambda m: str(m[0]).split(' '), matches[1:])))
    
    def solve_a(self):
        sum = 0
        for game in self._data.splitlines():
            valid = True
            (gameid, cubes) = self.get_cubes(game) 
            for (num, color) in cubes:
                print(num, color)
                if int(num) > limits[color]:
                    valid = False
                if not valid:
                    break
                
            if (valid):
                sum += gameid
            else:
                print('Invalid game, continue')
                continue
            
        return sum
    
    def solve_b(self):
        sum = 0
        for game in self._data.splitlines():
            (gameid, cubes) = self.get_cubes(game)
            cubes.sort(key=lambda c: int(c[0]), reverse=True)
            min = {}
            for (n,c) in cubes:
                if not min.get(c):
                    min[c] = int(n)
                if len(min) == 3:
                    break
            sum += min['red'] * min['blue'] * min['green']
            
        return sum
        
    def solve(self):
        return (self.solve_a(), self.solve_b())

solution = DailyPuzzle()
SUBMIT=False

print(solution.solve_a())
print(solution.solve_b())
if (SUBMIT):
    solution.submit()