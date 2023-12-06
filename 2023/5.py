from puzzle import Puzzle
import re
from collections import deque

class DailyPuzzle(Puzzle):
    def __init__(self):
        super(DailyPuzzle, self).__init__(2023, 5)
        self.init_data(remote=True)
    
    maps = {}    
    
    def create_maps(self):
        map_id = 0
        for line in self._data.splitlines():
            if re.match('[a-z]+-to-[a-z]+ map:$', line):
                map_id += 1
                self.maps[map_id] = {}
                in_map = True
                continue
            
            if map_id >=1:
                (i, o, n) = map(lambda v: int(v), re.findall('\d+', line))
                for v in range(int(i), int(i)+int(n)+1):
                    self.maps[map_id][v] = int(o)
                    o += 1
    
    items: dict[str, list]
    items_multi: dict[str, dict[int, int]]
    maps: dict[tuple, list[tuple]] = {}
    def do_the_mapping(self, map_from_item: str, map_to_item: str, items_to_map: deque):
        self.maps[(map_from_item, map_to_item)] = sorted(self.maps[(map_from_item, map_to_item)], key=lambda t: t[1])
        check_maps = deque(self.maps[(map_from_item, map_to_item)])
        while len(items_to_map) > 0:
            map_idx = 0
            item_value = items_to_map.popleft()
            map_found = False
            while map_idx < len(check_maps):
                (to_value, from_value, n) = check_maps[map_idx]
                map_func = lambda x: to_value - from_value + x
                item_in_range = from_value + n - item_value > 0 and item_value >= from_value
                if item_in_range:
                    
                    #items_to_map.remove(item_value)
                    print(f'{map_from_item} {item_value} -> {map_to_item} {to_value - from_value + item_value} using map {(to_value, from_value, n)}')
                    if (self.items_multi):
                        num_of_items = self.items_multi[map_from_item][item_value]
                        avail_items = from_value - item_value + n
                        if num_of_items > avail_items:
                            #print("outlier")
                            self.items_multi[map_to_item][map_func(item_value)] = avail_items
                            items_to_map.append(item_value + avail_items)
                            self.items_multi[map_from_item][item_value + avail_items] = num_of_items - avail_items
                        else:
                            self.items_multi[map_to_item][map_func(item_value)] = self.items_multi[map_from_item][item_value]
                            #print(f'Another {self.items_multi[map_from_item][item_value]} {map_from_item} mapped')
                    else:
                        self.items[map_to_item].append(map_func(item_value))
                        
                    map_found = True
                    break
                else: map_idx += 1
                
            if not map_found:
                self.items[map_to_item].append(item_value)
                if (self.items_multi):
                    self.items_multi[map_to_item][item_value] = self.items_multi[map_from_item][item_value]
    
    def do_the_math(self):
        map_from_item = None
        map_to_item = None
        items_to_map = []
        for row in self._data[1:].splitlines():
            map_header = re.search('([a-z]+)-to-([a-z]+) map:$', row)
            if map_header:
                map_from_item = map_header.group(1)
                map_to_item = map_header.group(2)
                self.items[map_to_item] = []
                if (self.items_multi):
                    self.items_multi[map_to_item] = {}

                self.maps[(map_from_item, map_to_item)] = []
                if not self.items_multi:
                    items_to_map = deque(sorted(self.items[map_from_item]))
                else:
                    items_to_map = deque(sorted(self.items_multi[map_from_item].keys()))
                continue
            elif not row and map_from_item: #new map comes
                self.do_the_mapping(map_from_item, map_to_item, items_to_map)
                map_from_item = None
                map_to_item = None

            #building the mappings
            if map_from_item and map_to_item and row:
                (to_value, from_value, n) = map(lambda v: int(v), re.findall('\d+', row))
                self.maps[(map_from_item, map_to_item)].append((to_value, from_value, n))
        
        #end of file, do the last mapping
        self.do_the_mapping(map_from_item, map_to_item, items_to_map)
    
        return min(self.items_multi['location'].keys()) if self.items_multi else min(self.items['location'])
    
    def solve_a(self):
        self.items = { 'seed': list(map(lambda v: int(v), re.findall('\d+', self._data.splitlines()[0])))}
        return self.do_the_math()
        
    def solve_b(self):
        self.items = { 'seed': [] }
        self.items_multi = { 'seed': {}}
        i = 0
        seeds = list(map(lambda v: int(v), re.findall('\d+', self._data.splitlines()[0])))
        for s in range(0, len(seeds), 2):
            self.items['seed'].append(seeds[s])
            self.items_multi['seed'][seeds[s]] = seeds[s+1]
        return self.do_the_math()
    
    def solve(self):
        return (self.solve_a(), self.solve_b())

solution = DailyPuzzle()
SUBMIT=False


#print(solution.solve_a())
print(solution.solve_b())
if (SUBMIT):
    solution.submit()