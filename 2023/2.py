from puzzle import Puzzle
import re

limits = {'red':12, 'green':13, 'blue':14}
class DailyPuzzle(Puzzle):
    def __init__(self):
        super(DailyPuzzle, self).__init__(2023, 2)
        self.init_data(remote=True)
    
    def get_cubes(self, draw: str) -> dict[str, int]: # 3 red, 4 green
        cubes: dict[str,int] = {}
        for instance in draw.split(','):
            (num, color) = instance.strip().split(' ')
            cubes[color] = int(num)
        return cubes
    
    def solve_a(self):
        sum = 0
        for game in self._data.splitlines():
            valid = True
            gameid = int(str(game).split(':')[0].replace('Game ', ''))
            draws = str(game).split(':')[1].split(';')
            for draw in draws:
                if not valid:
                    break
                cubes = self.get_cubes(draw)
                print(f'{gameid}: {cubes}')
                for c in cubes.keys():
                    if cubes[c] > limits[c]:
                        valid = False
            if (valid):
                sum += gameid
            else:
                print('Invalid game, continue')
                continue
            
        return sum
    
    def solve_b(self):
        sum = 0
        for game in self._data.splitlines():
            min = {'red':0, 'green':0, 'blue':0}
            gameid = int(str(game).split(':')[0].replace('Game ', ''))
            draws = str(game).split(':')[1].split(';')
            for draw in draws:
                
                cubes = self.get_cubes(draw)
                print(f'{gameid}: {cubes}')
                for c in cubes.keys():
                    if cubes[c] > min[c]:
                        min[c] = cubes[c]
            
            print(min)
            sum += min['red'] * min['blue'] * min['green']
            
        return sum
        
    def solve(self):
        return (self.solve_a(), self.solve_b())

solution = DailyPuzzle()
SUBMIT=False

#print(solution.solve_a())
print(solution.solve_b())
if (SUBMIT):
    solution.submit()