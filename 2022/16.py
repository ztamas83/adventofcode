import sympy as sym
from puzzle import Puzzle
import re
import copy
from queue import PriorityQueue, Queue

class Day16(Puzzle):
    def __init__(self):
        """
        Purpose: 
        """
        super().__init__(2022, 16)

    def get_value(self, valve):
        return self.nodes[valve][0]

    def get_paths(self, valve):
        return self.nodes[valve][1]

    def travel(self, start_node = None, target_node = None, start_time_left = 30, start_value = 0, start_path = []):
        all_paths = Queue()
        if start_path:
            all_paths.put((start_time_left, start_value, start_path))
        else:
            all_paths.put((start_time_left, start_value, [start_node]))
        valid_paths = []
        time_left = start_time_left
        pressure_rel = start_value
        explored = set()
        while not all_paths.empty():
            #print(iteration)
            time_left, p_rel,path = all_paths.get()
            current_node = path[-1]
            neighbors = self.get_paths(current_node)
            for node in neighbors:
                new_time_left = time_left
                new_p_rel = p_rel
                if node in explored:
                    continue
                explored.add(node)
                if len(path)>2 and [current_node, node] == [path[-3], path[-2]]:
                    continue
                if node.endswith('b') and self.get_value(node) > 0: #open this node if it makes sense
                    new_time_left = time_left - 2
                    new_p_rel = p_rel + new_time_left * self.get_value(node)
                elif node.endswith('b'): #drop this path
                    continue
                else:
                    new_time_left = time_left - 1
                new_path = path + [node]
                if node == target_node or new_time_left <= 0:
                    valid_paths.append((new_time_left, new_p_rel, new_path))
                else:
                    all_paths.put((new_time_left, new_p_rel, new_path))
        
        return valid_paths
    
    def solve_a(self):
        self.nodes: dict[str,tuple[int,str]] = {}
        pattern = ".*([A-Z]{2}).*=([0-9]{1,});.*valve(s|) (.*)$"
        
        for line in self._data.splitlines():
            #Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
            match = re.match(pattern, line)
            self.nodes[match.group(1)] = (int(match.group(2)), match.group(4).split(', ') + [n + 'b' for n in match.group(4).split(', ')])
            self.nodes[match.group(1)+'b'] = (int(match.group(2)), match.group(4).split(', ') + [n + 'b' for n in match.group(4).split(', ')] )

            # open_variants
            print (self.nodes[match.group(1)])


        # closed valves
        
        all_valves = self.nodes.keys()

        print(all_valves)
        time_left = 30
        start_pos = 'AA'
    
        best_value = 0
        for valve in filter(lambda n: n.endswith('b') and self.get_value(n), all_valves):
            #find all path that gives points
            if not valve.startswith(start_pos):
                possible_paths = self.travel(start_pos, valve)
                for time_left,p_rel,path in possible_paths:
                    remaining_valves = list(filter(lambda n: n.endswith('b') and n not in path and self.get_value(n),  [v for v in all_valves]))
                    if time_left > 0:
                        for ov in remaining_valves:
                            next_segment = self.travel(path[-1], ov)

                        best_value = p_rel
                        print(f'{path} with value {p_rel}')



d = Day16()
d.init_data()
d.solve_a()