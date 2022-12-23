from puzzle import Puzzle
import numpy as np
from collections import deque
import copy


KEYN = 'N'
KEYNW = 'NW'
KEYNE = 'NE'
KEYS = 'S'
KEYSW = 'SW'
KEYSE = 'SE'
KEYW = 'W'
KEYE = 'E'

MOVEDICT = {
    KEYN: lambda pos: (pos[0] - 1, pos[1]),
    KEYNW: lambda pos: (pos[0] - 1, pos[1] - 1),
    KEYNE: lambda pos: (pos[0] - 1, pos[1] + 1),
    KEYS: lambda pos: (pos[0] + 1, pos[1]),
    KEYSW: lambda pos: (pos[0] + 1, pos[1] - 1),
    KEYSE: lambda pos: (pos[0] + 1, pos[1] + 1),
    KEYW: lambda pos: (pos[0], pos[1] - 1),
    KEYE: lambda pos: (pos[0], pos[1] + 1)
}

N = MOVEDICT[KEYN]
NW = MOVEDICT[KEYNW]
NE = MOVEDICT[KEYNE]
S = MOVEDICT[KEYS]
SE = MOVEDICT[KEYSE]
SW = MOVEDICT[KEYSW]
E = MOVEDICT[KEYE]
W = MOVEDICT[KEYW]

TRYN = [KEYN, KEYNE, KEYNW]
TRYS = [KEYS, KEYSE, KEYSW]
TRYW = [KEYW, KEYNW, KEYSW]
TRYE = [KEYE, KEYNE, KEYSE]

class Elf():
    def __init__(self) -> None:
        self.next_key: str = ''
        self.moves: deque = deque([TRYN, TRYS, TRYW, TRYE])

    def __hash__(self) -> int:
        return hash(self.pos)

    def __str__(self) -> str:
        return f'Elf -> {self.next_key})'

    def propose(self, grove: np.matrix, current_pos: tuple):
        try_moves = copy.deepcopy(self.moves)
        possible_moves = []
        while try_moves:
            try_directions = try_moves.popleft()
            direction_ok = True
            for current_move in try_directions:
                new_pos = MOVEDICT[current_move](current_pos)
                if not (0 <= new_pos[0] < grove.shape[0] and 0 <= new_pos[1] < grove.shape[1]): #looking outside the grove
                    pass
                elif grove[new_pos[0], new_pos[1]] > 0:
                    direction_ok = False

            if direction_ok:
                possible_moves.append(try_directions[0])

        self.moves.append(self.moves.popleft())
        
        if 0 < len(possible_moves) < 4:
            self.next_key = possible_moves[0]
            return self #returns an Elf object so it can be moved in the next round
        
        return None
    
    def cancel_move(self):
        self.next_key = ''

    def move(self, current_pos:tuple) -> tuple:
        return MOVEDICT[self.next_key](current_pos) if self.next_key else None

class Day23(Puzzle):
    def __init__(self):
        super().__init__(2022, 23)

    def get_grove(self) -> tuple[np.matrix, dict[int,Elf]]:
        rows = self._data.splitlines()
        grove = np.zeros((len(rows), len(rows[0])), dtype=int)
        elves = {}
        for r,row in enumerate(rows):
            for c, col in enumerate(row):
                if col == '#':
                    elve_id = len(elves) + 1
                    elves[elve_id] = Elf()
                    grove[r,c] = elve_id

        return grove, elves

    def propose_moves(self, grove, elves: list[Elf]) -> tuple[np.matrix, dict[tuple,int]]:
        to_move: dict[tuple,int] = {}
        # scan grove for moves
        expand = set()
        it = np.nditer(grove, flags=['multi_index'])
        for coord in it:
            elfid = int(it[0])
            elf = elves.get(elfid)
            if elf and elf.propose(grove, it.multi_index):
                proposed_position = MOVEDICT[elf.next_key](it.multi_index)
                if not to_move.get(proposed_position):
                    to_move[proposed_position] = elfid
                    if (proposed_position[0] < 0): #expand up
                        expand.add(KEYN)
                    if (proposed_position[1] < 0): #expand left
                        expand.add(KEYW)
                    if (proposed_position[0] >= grove.shape[0]): #expand down
                        expand.add(KEYS)
                    if (proposed_position[1] >= grove.shape[1]): #expand right
                        expand.add(KEYE)
                else:
                    elves[to_move.pop(proposed_position)].cancel_move()
                    elf.cancel_move()

        if KEYN in expand: #expand up
            row = np.zeros((1, grove.shape[1]), dtype=int)
            grove = np.vstack((row, grove))
        if KEYW in expand: #expand left
            col = np.zeros((grove.shape[0], 1), dtype=int)
            grove = np.hstack((col,grove))
        if KEYS in expand: #expand down
            row = np.zeros((1, grove.shape[1]), dtype=int)
            grove = np.vstack((grove, row))
        if KEYE in expand: #expand right
            col = np.zeros((grove.shape[0], 1), dtype=int)
            grove = np.hstack((grove,col))

        return grove,to_move

    def move_elves(self, grove, elves, moves) -> np.matrix:
        new_grove = np.copy(grove)
        # stage 2 - move
        for elfid in moves.values():
            elf = elves[elfid]
            elf_pos = np.where(grove == elfid)
            x,y = (int(elf_pos[0]), int(elf_pos[1]))
            
            new_x, new_y = elf.move((x,y))

            new_grove[x,y] = 0
            new_grove[new_x, new_y] = elfid

        #print(new_grove)
        return new_grove

    def solve(self):
        a, b = self.solve_a()
        return (a, b)

    def solve_a(self):
        grove, elves = self.get_grove()
        
        to_move = {(0,0): None}
        count = 0
        while to_move:
            count += 1
            grove, to_move = self.propose_moves(grove,elves)
            grove = self.move_elves(grove, elves, to_move)
            print('Grove size: ', grove.shape, np.count_nonzero(grove), count, len(to_move))
            if count == 10:
                # from: https://stackoverflow.com/questions/4808221/is-there-a-bounding-box-function-slice-with-non-zero-values-for-a-ndarray-in
                rows = np.any(grove, axis=1)
                cols = np.any(grove, axis=0)
                ymin, ymax = np.where(rows)[0][[0, -1]]
                xmin, xmax = np.where(cols)[0][[0, -1]]
                reduced = grove[ymin:ymax+1, xmin:xmax+1]

                answer_a = reduced.size - np.count_nonzero(reduced)
                print('Answer A: ', answer_a)

        return answer_a, count

SUBMIT = True
d = Day23()

if SUBMIT:
    d.submit()
else:
    d.init_data()
    #print(d.solve_a())
    print(d.solve)
