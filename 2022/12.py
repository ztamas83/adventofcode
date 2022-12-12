from puzzle import Puzzle
import numpy as np
import copy
from queue import PriorityQueue

class Nodes():
    def __init__(self):
        self.nodes: dict[tuple, dict] = {}
        self.neighbors: dict[tuple, list] = {}
        self._end: tuple
        self._start: tuple
     
    def get_node(self, coords: tuple[int,int]) -> dict:
        return self.nodes.get(coords)

    def add_node(self, coords, elevation, special = ''):
        if (coords in self.nodes):
            return
        self.nodes[coords] = {'visited': False, 'spec_node': special, 'elev': elevation}
        if special == 'E':
            self._end = coords
        if special == 'S':
            self._start = coords

    def add_neighbor(self, coords, neighbor_coords):
        if not self.neighbors.get(coords):
            self.neighbors[coords] = []
        
        self.neighbors[coords].append(neighbor_coords)
    
    def get_neighbors(self, coords) -> list[tuple[int,int]]:
        return self.neighbors.get(coords, [])

    @property
    def start_node(self) -> tuple[int,int]:
        return self._start

    @property
    def end_node(self) -> tuple[int,int]:
        return self._end

    def visited(self, coords) -> bool:
        return self.nodes[coords]['visited']

    def set_visited(self, coords):
        self.nodes[coords]['visited'] = True

    def clear_visited(self, coords):
        for node in self.nodes:
            self.nodes[node]['visited'] = False
    
class Day12(Puzzle):
    def __init__(self):
        super(Day12, self).__init__(2022, 12)
        self.all_path = []
        
    def create_terrain(self):
        lines = self._data.splitlines()
        self.terrain = []
        for line in lines:
            self.terrain.append(np.array(list(map(lambda c: ord(c), line))))
            
        self.terrain = np.matrix(self.terrain)

    def _real_elevation(self, coordx: int, coordy:int):
        value = self.terrain[coordx, coordy]
        if value >= 96:
            current_elevation = value
            special = ''
        elif value == ord('S'):
            current_elevation = ord('a')
            special = 'S'
        else:
            current_elevation = ord('z')
            special = 'E'

        return current_elevation, special

    def create_nodes(self, solve_b = False):
        it = np.nditer(self.terrain, flags=['multi_index'])
        self.nodes = Nodes()

        for coord in it:
            row = it.multi_index[0]
            col = it.multi_index[1]

            if current_node := self.nodes.get_node(it.multi_index):
                current_elevation = current_node['elev']
            else:
                current_elevation, this_spec = self._real_elevation(row, col)
                self.nodes.add_node(it.multi_index, current_elevation, this_spec)

            directions = [(row, col-1), (row, col+1), (row-1, col), (row+1, col)]

            for trow, tcol in directions:
                if tcol >= 0 and tcol < self.terrain.shape[1] and trow >=0 and trow < self.terrain.shape[0]:
                    if not solve_b:
                        elev_function = self._real_elevation(trow, tcol)[0] - current_elevation <= 1
                    else:
                        elev_function = self._real_elevation(trow, tcol)[0] - current_elevation >= -1

                    if elev_function:
                        self.nodes.add_node((trow, tcol), self._real_elevation(trow, tcol)[0], self._real_elevation(trow, tcol)[1])
                        self.nodes.add_neighbor(it.multi_index, (trow, tcol))

    def solve(self):
        self.create_terrain()
        return (self.solve_a(), self.solve_b())

    def travel(self, start_node = None, target_node = None):
        all_paths = PriorityQueue()
        if start_node:
            all_paths.put((1, [start_node]))
        else:
            all_paths.put((1, [self.nodes.start_node]))
        
        if not target_node:
            target_node = self.nodes.end_node

        explored = set()
        shortest_path = 0
        iteration = 0
        while not all_paths.empty():
            #print(iteration)
            iteration+=1
            _,path = all_paths.get()
            current_node = path[-1]
            if current_node in explored:
                continue
            explored.add(current_node)
            for node in self.nodes.get_neighbors(current_node):
                if node == target_node:
                    if shortest_path == 0 or len(path) < shortest_path:
                        shortest_path = len(path)
                elif not node in path:
                    new_path = path + [node]
                    if shortest_path == 0 or len(new_path) < shortest_path:
                        all_paths.put((len(new_path), new_path))
            #print(f'Handling {all_paths.qsize()} paths')
        return shortest_path
    
    def solve_a(self):
        self.create_nodes(False)
        shortest =  self.travel()
        print (shortest)
        return shortest

    def solve_b(self):
        self.create_nodes(True)
        possible_paths = []
        for point in reversed(self.nodes.nodes):
            if self.nodes.get_node(point)['elev'] == ord('a'):
                steps = self.travel(self.nodes.end_node, point)
                print (f'travel to {point} takes {steps}')
                if steps:
                    possible_paths.append(steps)
                print(f'current shortest: {min(possible_paths, default=None)}')
        return min(possible_paths)

       
        
puzzle = Day12()

puzzle.submit()