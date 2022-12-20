from puzzle import Puzzle
import numpy as np
from queue import LifoQueue
import copy

class Day14(Puzzle):
    def __init__(self) -> None:
        super().__init__(2022, 14)
    
    def draw_cave(self, cave_bottom = False):
        rocks = []
        dimensions = [0,0]
        for line in self._data.splitlines():
            x1 = []
            for x2 in map(lambda l: [int(l[0]), int(l[1])], [l.strip().split(',') for l in  line.split('->')]):
                print(f'{x1} -> {x2}')
                rocks.append(x2)
                if x2[0] > dimensions[0]: dimensions[0] = x2[0]
                if x2[1] > dimensions[1]: dimensions[1] = x2[1]
                if x1: # draw
                    if (x1[0] != x2[0]):
                        for x in range(min(x1[0], x2[0])+1, max(x1[0], x2[0])):
                            rocks.append([x, x1[1]])
                    if (x1[1] != x2[1]):
                        for y in range(min(x1[1], x2[1])+1, max(x1[1], x2[1])):
                            rocks.append([x1[0], y])
                x1 = x2

        if cave_bottom:
            for col in range(dimensions[0]+1):
                rocks.append([col, dimensions[1]+2])
            
            dimensions[1] += 2
            dimensions[0] += 1

        cave = np.matrix(np.zeros((dimensions[1]+1, dimensions[0]+1), dtype=int))
        for rock in rocks:
            cave[rock[1], rock[0]] = 1
        print(cave[:, dimensions[0] - 30:])
        return cave

    def pour_sand(self, cave: np.matrix, cave_bottom = False):
        sand_source = (0, 500)
        sand_pos = self.find_next_pos(sand_source, cave, cave_bottom)
        particles = 0
        while sand_pos:
            particles += 1
            cave[sand_pos[0], sand_pos[1]] = 2
            print(cave[:, cave.shape[1] - 30:])
            print('-------'*6)
            sand_pos = self.find_next_pos(sand_source, cave, cave_bottom)
        
        return particles
    
    def item_at_pos(self, pos, cave):
        if pos[0]==cave.shape[0]: return None #abyss
        if pos[1]<0 or pos[1] == cave.shape[1]: return None #abyss
        return cave[pos[0], pos[1]]

    def item_at_pos_with_bottom(self, pos, cave):
        if pos[0]==cave.shape[0]: return None #abyss
        if pos[1]<0 or pos[1] == cave.shape[1]: return None #abyss
        return cave[pos[0], pos[1]]

    def find_next_pos(self, current_pos: tuple, cave: np.matrix, cave_bottom = False) -> tuple:
        
        pos_down = lambda t: (t[0]+1, t[1])
        pos_diag_left = lambda t: (t[0]+1,t[1]-1)
        pos_diag_right = lambda t: (t[0]+1,t[1]+1) 

        possible_moves = LifoQueue()
        possible_moves.put(pos_down)

        while not possible_moves.empty():
            next_move = possible_moves.get()
            item = self.item_at_pos(next_move(current_pos), cave)
            if item is None:
                return None
            elif item == 0: #position free
                current_pos = next_move(current_pos)
                possible_moves.put(pos_down)
            elif item > 0: #rock or sand
                if next_move(current_pos) == pos_down(current_pos):
                    possible_moves.put(pos_diag_left)
                elif next_move(current_pos) == pos_diag_left(current_pos): #move diagonal left blocked
                    possible_moves.put(pos_diag_right)
                else: #move diag right blocked
                    return current_pos
        
            

    def solve_a(self):
        cave = self.draw_cave()
        return self.pour_sand(cave) # queues with key at the bottom of the drop

    def solve_b(self):
        cave = self.draw_cave(True)
        return self.pour_sand(cave, True) # queues with key at the bottom of the drop
        

d = Day14()
d.init_data()
bres = d.solve_b()
#d.submit(sub_b=False)
print(bres)
