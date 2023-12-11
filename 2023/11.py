import networkx as nx
from matplotlib import pyplot as plt
from puzzle import Puzzle
import numpy as np

class DailyPuzzle(Puzzle):
    def __init__(self):
        super(DailyPuzzle, self).__init__(2023, 11)
        self.init_data(remote=True)
       
    universe: np.array = None
    def solve_a(self):
        for row in self._data.splitlines():
            if self.universe is None:
                self.universe = np.array(list(row), dtype=str)
            else:
                self.universe = np.vstack((self.universe, np.array(list(row), dtype=str)))
                
            if not '#' in row: #empty row, expand
                self.universe = np.vstack((self.universe, np.array(list(row), dtype=str)))
        
        new_universe = np.copy(self.universe)
        new_c = 0
        for c in range(0,self.universe.shape[1]):
            chars = self.universe[:,c]
            if not '#' in chars:
                b = np.zeros((new_universe.shape[0],new_universe.shape[1]+1), dtype=str)
                split = (new_universe[:,:new_c], new_universe[:,new_c:])
                b[:,:new_c] = split[0]
                b[:,new_c] = chars.T
                b[:,new_c+1:] = split[1]
                new_universe = b
                new_c +=1
            new_c += 1
                
        self.universe = new_universe
        coords = np.asarray(np.where(self.universe == '#')).T.tolist()
        res = [(tuple(a), tuple(b)) for idx, a in enumerate(coords) for b in coords[idx + 1:]]
        sum_path = 0
        for pair in res:
            shortest_path = abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1])
            sum_path += shortest_path
            print(f'Path between {pair[0]} - {pair[1]} is {shortest_path}')
        return sum_path
                
    def expand(self, coords, nc, nr, factor):
        return (coords[0] - nr + nr*factor, coords[1] - nc + nc * factor)
        
    def solve_b(self):
        self.universe = None
        EXPANSION_FACTOR = 1000000
        empty_rows = set()
        empty_cols = set()
        for idx,row in enumerate(self._data.splitlines()):
            if self.universe is None:
                self.universe = np.array(list(row), dtype=str)
            else:
                self.universe = np.vstack((self.universe, np.array(list(row), dtype=str)))
                
            if not '#' in row: #empty row, expand
                empty_rows.add(idx)
        
        for c in range(0,self.universe.shape[1]):
            chars = self.universe[:,c]
            if not '#' in chars:
                empty_cols.add(c)
        
        coords = [tuple(x) for x in np.asarray(np.where(self.universe == '#')).T.tolist()]
        for idx,coord in enumerate(coords):
            nc = sum(1 for c in empty_cols if c < coord[1])
            nr = sum(1 for r in empty_rows if r < coord[0])
            coords[idx] = self.expand(coord, nc, nr, EXPANSION_FACTOR)
            
        res = [(a, b) for idx, a in enumerate(coords) for b in coords[idx + 1:]]
        sum_path = 0
        print(f'Found {len(res)} pairs')
        # max_r = 0
        # max_c = 0
        for pair in res:
            new_dest_r, new_dest_c = pair[1]
            new_start_r, new_start_c = pair[0]

            #only for plotting...
            #if new_dest_r > max_r: max_r = new_dest_r
            #if new_dest_c > max_c: max_c = new_dest_c

            shortest_path = abs(new_start_r- new_dest_r) + abs(new_start_c - new_dest_c)
            sum_path += shortest_path
            #print(f'Path between {(new_start_r, new_start_c)} - {new_dest_r, new_dest_c} is {shortest_path}')
        
        # G = nx.grid_2d_graph(max_r,max_c)
        # plt.figure(figsize=(10,10))
        # pos = {(x,y):(y,-x) for x,y in G.nodes()}
        # color_map = list(map(lambda n: 'red' if n in coords else 'lightgreen', G) )
        # nx.draw(G, pos=pos, 
        #         node_color=color_map, 
        #         with_labels=True,
        #         node_size=600)
        
        # plt.show()
        return sum_path
            
    def solve(self):
        return (self.solve_a(), self.solve_b())

solution = DailyPuzzle()
SUBMIT=False

print(solution.solve_a())
print(solution.solve_b())
if (SUBMIT):
    solution.submit()