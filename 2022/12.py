from puzzle import Puzzle
import numpy as np
import copy


class Node():
    def __init__(self, level, row, col):
        self.level = level
        self.coords = (row, col)
        self.neighbors = []
    
    def get_full_path(self) -> list:
        if self.neighbors:
            print(list(map(lambda n: n.coords, self.neighbors)))
        
    def add_neighbor(self, row, col):
        new_node = Node(self.level + 1, row, col)
        self.neighbors.append(new_node)
        
        return new_node
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.coords == other.coords
        else:
            return False
    
    def __contains__(self, item):
        if isinstance(item, self.__class__):
            return self.coords == item.coords
        else:
            return False
    
    def __hash__(self):
        return hash(self.coords)

    
class Day12(Puzzle):
    def __init__(self):
        super(Day12, self).__init__(2022, 12)
        
    def create_terrain(self):
        lines = self._data.splitlines()
        terrain = []
        for line in lines:
            terrain.append(np.array(list(map(lambda c: ord(c), line))))
            
        return np.matrix(terrain)
    
    def dfs(self, terrain, current_node: tuple, target_node: tuple, visited: dict[list[tuple]] = {}, path_id = 0):
        if visited and current_node in [node for nodes in visited.values() for node in nodes]:
                return visited
        
        if not visited.get(path_id):
            visited[path_id] = copy.deepcopy(visited[path_id - 1]) if path_id > 0 else []
                    
        visited[path_id].append(current_node)
        
        if (current_node == target_node): #reached goal
            return visited
        
        row, col = current_node
        if terrain[row, col] >= 96:
            current_elevation = terrain[row, col]
        elif terrain[row, col] == ord('S'):
            current_elevation = ord('a')
        else:
            current_elevation = ord('z')

        left = (row, col-1) if col-1 > 0 and terrain[row, col-1] - current_elevation <= 1 else None
        right = (row, col+1) if col + 1 < terrain.shape[1] and terrain[row, col+1] - current_elevation <= 1 else None
        up = (row-1, col) if row-1 > 0 and terrain[row-1, col] - current_elevation <= 1 else None
        down = (row+1, col) if row+1 < terrain.shape[0] and terrain[row+1, col] - current_elevation <= 1 else None
        
        if left:
            self.dfs(terrain, left, target_node, visited, path_id)
            path_id += 1
        if right:
            self.dfs(terrain, right,target_node, visited, path_id)
            path_id += 1
        if down:
            self.dfs(terrain, down, target_node,visited, path_id)
            path_id += 1
        if up:
            self.dfs(terrain, up, target_node,visited, path_id)
            path_id += 1
            
        return visited

    def solve_a(self):
        terrain = self.create_terrain()
        (x, y) = start = np.where(terrain == ord('S'))
        (ex,ey) =end = np.where(terrain == ord('E'))
        
        start_node = (x[0], y[0])
        end_node = (ex[0],ey[0])
        all_path = self.dfs(terrain, start_node, end_node)
                
        for path in all_path:
            print(all_path[path])
        current_node = start_node
      
       
        
puzzle = Day12()
puzzle.init_data()

puzzle.solve_a()