import networkx as nx
from matplotlib import pyplot as plt
from puzzle import Puzzle
import numpy as np

class DailyPuzzle(Puzzle):
    def __init__(self):
        super(DailyPuzzle, self).__init__(2023, 11)
        self.init_data(remote=True)
       
    universe: np.array = None
                    
    def expand(self, coords, nc, nr, factor):
        return (coords[0] - nr + nr*factor, coords[1] - nc + nc * factor)
    
    def solve_expanded(self, factor):
        self.universe = None
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
            coords[idx] = self.expand(coord, nc, nr, factor)
            
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
        
    def solve_a(self):
        return self.solve_expanded(2)
    
    def solve_b(self):
        return self.solve_expanded(100000)
            
    def solve(self):
        return (self.solve_a(), self.solve_b())

solution = DailyPuzzle()
SUBMIT=False

print(solution.solve_a())
print(solution.solve_b())
if (SUBMIT):
    solution.submit()