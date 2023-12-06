from puzzle import Puzzle
import re
import math

class DailyPuzzle(Puzzle):
    def __init__(self):
        super(DailyPuzzle, self).__init__(2023, 6)
        self.init_data(remote=True)

    def calc_travel(self, charge_time_ms, total_race_time_ms):
        # for each charge_time_ms the travel speed increases with 1 ms/mm -> speed == charge_time_ms
        return (total_race_time_ms - charge_time_ms) * charge_time_ms
    
    def get_charge_for_travel(self, race_time, distance):
        discriminant = math.pow(race_time, 2) - 4*distance
        ct1 = math.floor((-race_time +  math.sqrt(discriminant)) / -2)
        ct2 = math.floor((-race_time - math.sqrt(discriminant)) / -2)
        return [ct1, ct2]
                
    def solve_a(self):
        times = list(map(lambda d: int(d),re.findall("\d+", self._data.splitlines()[0])))
        distances = list(map(lambda d: int(d), re.findall("\d+", self._data.splitlines()[1])))
        sum = 1
        
        for race in range(0,len(times)):
            race_time = times[race]
            d_to_beat = distances[race]
            ct_to_win = self.get_charge_for_travel(race_time, d_to_beat)
            print(f'Race can be won with charges {min(ct_to_win)+1} .. {max(ct_to_win)-1}')
            sum = sum * (max(ct_to_win) - min(ct_to_win))
        return sum
            
    def solve_b(self):
        race_time = 0
        for part in re.finditer("\d+", self._data.splitlines()[0]):
            race_time = race_time * math.pow(10, len(part.group())) + int(part.group())
            
        distance_to_beat =0
        for part in re.finditer("\d+", self._data.splitlines()[1]):
            distance_to_beat = distance_to_beat * math.pow(10, len(part.group())) + int(part.group())
        
        distance_to_beat += 1
        ct_to_win = self.get_charge_for_travel(race_time, distance_to_beat)
        return max(ct_to_win) - min(ct_to_win)
    
    def solve(self):
        return (self.solve_a(), self.solve_b())

solution = DailyPuzzle()
SUBMIT=False

print(solution.solve_a())
print(solution.solve_b())
if (SUBMIT):
    solution.submit()