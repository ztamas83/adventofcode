from puzzle import Puzzle
import re
import numpy as np
from collections import deque

class DailyPuzzle(Puzzle):
    def __init__(self):
        super(DailyPuzzle, self).__init__(2023, 10)
        self.init_data(remote=False)
    
    E = 'east'
    N = 'north'
    S = 'south'
    W = 'west'
    MOVES = {
        'north': lambda pos: (pos[0]-1,pos[1]),
        'south': lambda pos: (pos[0]+1,pos[1]),
        'east': lambda pos: (pos[0], pos[1]+1),
        'west': lambda pos: (pos[0], pos[1]-1)    
    }
    
    POSSIBLE_MOVES = {
        '-': [E, W],
        '|': [N, S],
        '7': [W, S],
        'J': [W, N],
        'F': [E, S],
        'L': [E, N],
        'S': [N,E,S,W]
    }
    
    world: np.array = None
    def can_move(self, dir:str, current_pos: tuple[int,int]):
        new_pos = self.MOVES[dir](current_pos)
        if new_pos in self.visited:
            return False
        if new_pos[0] < 0 or new_pos[0] > self.world.shape[0] - 1:
            return False
        if new_pos[1] < 0 or new_pos[1] > self.world.shape[1] - 1:
            return False
        
        current_pipe = self.world[current_pos[0], current_pos[1]]
        match current_pipe:
            case 'S':
                if self.world[new_pos] == '.': return False
                if dir == 'south' and self.world[new_pos] in set('J|LS'):
                    return True
                if dir == 'west' and self.world[new_pos] in set('L-FS'):
                    return True
                if dir == 'north' and self.world[new_pos] in set('|F7S'):
                    return True
                if dir == 'east' and self.world[new_pos] in set('-7JS'):
                    return True
            case '|':
                #north / south
                if dir in ('north', 'south') and not self.world[new_pos] == '-':
                    return True
                return False
            case '-':
                #east / west
                if dir in ('east', 'west') and not self.world[new_pos] == '|':
                    return True
                return False
            case '7':
                # possible moves: west, south
                if dir == 'south' and self.world[new_pos] in set('J|LS'):
                    return True
                if dir == 'west' and self.world[new_pos] in set('L-FS'):
                    return True
                pass
            case 'L':
                # possible moves: north, east
                if dir == 'north' and self.world[new_pos] in set('|F7S'):
                    return True
                if dir == 'east' and self.world[new_pos] in set('-7JS'):
                    return True
                pass
            case 'J':
                # possible moves: north, west
                if dir == 'north' and self.world[new_pos] in set('|F7S'):
                    return True
                if dir == 'west' and self.world[new_pos] in set('-FLS'):
                    return True
                pass
            case 'F':
                # possible moves: south, east
                if dir == 'south' and self.world[new_pos] in set('J|LS'):
                    return True
                if dir == 'east'  and self.world[new_pos] in set('-J7S'):
                    return True
                pass
        # match self.world[new_pos]:
        #     case '|':
        #         if current_pipe == '-':
        #             return False
        #         return new_pos[1] == current_pos[1] and new_pos[0] in (current_pos[0]+1, current_pos[0]-1)
        #     case '-':
        #         if current_pipe == '|':
        #             return False
        #         return new_pos[0] == current_pos[0] and new_pos[1] in (current_pos[1]+1, current_pos[1]-1)
        #     case 'L':
        #         return new_pos[1] == current_pos[1] and new_pos[0] == current_pos[0] - 1 and current_pipe in set('|F7S')\
        #             or new_pos[0] == current_pos[0] and new_pos[1] == current_pos[1] + 1 and current_pipe in set('-7JS')
        #     case 'F':
        #         return new_pos[1] == current_pos[1] and new_pos[0] == current_pos[0] + 1 and current_pipe in set('|LJS')\
        #             or new_pos[0] == current_pos[0] and new_pos[1] == current_pos[1] + 1 and current_pipe in set('-7JS')
        #     case 'J':
        #         return new_pos[1] == current_pos[1] and new_pos[0] == current_pos[0] - 1 and current_pipe in set('|F7S')\
        #             or new_pos[0] == current_pos[0] and new_pos[1] == current_pos[1] - 1 and current_pipe in set('-LFS')
        #     case '7':
        #         return new_pos[1] == current_pos[1] and new_pos[0] == current_pos[0] + 1 and current_pipe in set('|LJS') \
        #             or new_pos[0] == current_pos[0] and new_pos[1] == current_pos[1] - 1 and current_pipe in set('-LFS')
        
        return False
    
    
    
    
    max_distance = 0
    visited: set[tuple] = set()
    distances = {}
    def move(self, start_pos, move_count = 0):
        # myworld = np.copy(self.world)
        # myworld[start_pos] = '*'
        # print(myworld)
        self.visited.add(start_pos)
        distance_at_this_pos = self.distances.get(start_pos)
        if distance_at_this_pos: #already visited from the other side
            if distance_at_this_pos in [0, move_count]:
                return distance_at_this_pos
            distance_at_this_pos = move_count
        else: 
            self.distances[start_pos] = move_count
        
        for dir in self.POSSIBLE_MOVES[self.world[start_pos]]:
            if self.can_move(dir, start_pos):
                return self.MOVES[dir](start_pos)
                #return self.move(func(start_pos), move_count + 1)
                
    def solve_a(self):
        for row in self._data.splitlines():
            if self.world is None:
                self.world = np.array(list(row), dtype=str)
                continue
            self.world = np.vstack((self.world, np.array(list(row), dtype=str)))
        #print(self.world)
        start_pos = np.asarray(np.where(self.world=='S')).T[0].tolist()
        print(start_pos)
        self.visited.add((start_pos[0], start_pos[1]))
        # find first possible moves:
        possible_moves = []
        for dir in self.POSSIBLE_MOVES['S']:
            if self.can_move(dir, start_pos):
                possible_moves.append(dir)
        print(possible_moves)
        moves = 1
        current_pos = self.MOVES[possible_moves[0]](start_pos)
        self.distances[(start_pos[0], start_pos[1])] = 0
        
        while new_pos := self.move(current_pos, moves):
            if new_pos is int:
                print(f'Loop length = {new_pos}')
                break
            current_pos = new_pos
            moves += 1
            
        print(f'Done, moves: {moves}, current pos {current_pos}')
            
        return (moves + 1) / 2     
        
    def solve_b(self):
        if not self.visited:
            self.solve_a()
        
        it = np.nditer(self.world, flags=['multi_index'], op_flags=['writeonly'])
        for x in it:
            if it.multi_index not in self.visited:
                self.world[it.multi_index]= '.'
        
        # ray from above:
        for c in range(0, self.world.shape[1]):
            for r in range(0, self.world.shape[0]):
                match self.world[r,c]:
                    case '.': self.world[r,c] = 'x'
                    case '-': break
                print(self.world)
        # ray from below:
        for c in range(0, self.world.shape[1]):
            for r in reversed(range(0, self.world.shape[0])):
                match self.world[r,c]:
                    case '.': self.world[r,c] = 'x'
                    case '-': break
                print(self.world)
        
        np.savetxt('array.txt', self.world, fmt='%s')
        
        # ray from left:
        for r in range(0, self.world.shape[0]):
            for c in range(0, self.world.shape[1]):
                match self.world[r,c]:
                    case '.': self.world[r,c] = 'x'
                    case '|': break
                print(self.world)
                
        # ray from right:
        for r in range(0, self.world.shape[0]):
            for c in reversed(range(0, self.world.shape[1])):
                match self.world[r,c]:
                    case '.': self.world[r,c] = 'x'
                    case '|': break
                print(self.world)
        
        dots = deque(np.asarray(np.where(self.world=='.')).T.tolist())
        while len(dots) > 0:
            pos = dots.popleft()
            for neighbor in map(lambda f: self.world[f((pos[0], pos[1]))], self.MOVES.values()):
                if neighbor == 'x':
                    self.world[pos[0], pos[1]] = 'x'
                    break
            print(self.world)            
        
            
        unique, counts= np.unique(self.world, return_counts=True)
        return dict(zip(unique, counts))['.']
        
    def solve(self):
        return (self.solve_a(), self.solve_b())

solution = DailyPuzzle()
SUBMIT=False

#print(solution.solve_a())
print(solution.solve_b())
if (SUBMIT):
    solution.submit()