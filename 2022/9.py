from puzzle import Puzzle
import copy
import matplotlib.pyplot as plt

SUBMIT = False


class Day9(Puzzle):
    def __init__(self):
        super(Day9, self).__init__(2022, 9)

    def touching(self, hpos:tuple[int,int], tpos:tuple[int,int]) -> bool:
        return abs(hpos[0]- tpos[0]) < 2 and abs(hpos[1]-tpos[1]) < 2

    def get_new_pos(self, curr, direction) -> tuple[int,int]:
        match direction:
            case 'D':
                return (curr[0], curr[1] - 1)
            case 'U':
                return (curr[0], curr[1] + 1)
            case 'L':
                return (curr[0] - 1, curr[1])
            case 'R':
                return (curr[0] + 1, curr[1])

    def solve_a(self):
        head_pos = (0,0)
        head_pos_history = []
        tail_pos = (0,0)
        tail_pos_history = []
        for (direction,n) in [tuple(m.strip().split(' ')) for m in self._data]:
            print(f'move {direction} {n}')
            for i in range(1, int(n) + 1):
                new_pos = self.get_new_pos(head_pos, direction)
                head_pos_history.append(head_pos)
                head_pos = new_pos
                if self.touching(head_pos, tail_pos):
                    print(head_pos, tail_pos)
                    continue
                
                tail_pos_history.append(tail_pos)
                tail_pos = head_pos_history[-1]
                print(head_pos, tail_pos)

        tail_pos_history.append(tail_pos)
        return len(set(tail_pos_history))

    def solve_b(self):
        rope = [(0,0)] * 10
        tail_pos_history = []
        rope_history = []
        for (direction,n) in [tuple(m.strip().split(' ')) for m in self._data]:
            print(f'move {direction} {n}')
            for i in range(1, int(n) + 1):
                rope_new = copy.deepcopy(rope)
                new_head_pos = self.get_new_pos(rope[0], direction)
                rope_new[0] = new_head_pos
                prev_pos = new_head_pos
                for this_knot_idx in range(1, len(rope)): #no need to work on the head and tail
                    if (this_knot_idx == len(rope) - 1):
                        tail_pos_history.append(rope_new[-1])
                    knot_pos = rope_new[this_knot_idx]

                    if self.touching(prev_pos, knot_pos): #no need for the next knot to move and then the whole rope doesn't move
                        prev_pos = knot_pos
                        break
                    else:
                        # otherwise move the next knot
                        new_pos = knot_pos
                        x_diff = prev_pos[0] - knot_pos[0]
                        y_diff = prev_pos[1] - knot_pos[1]
                        if (x_diff == 0): #same row
                            new_pos = (new_pos[0], new_pos[1] + (prev_pos[1] - knot_pos[1]) // 2)
                        elif (y_diff == 0): #same col
                            new_pos = (new_pos[0] + (prev_pos[0] - knot_pos[0]) // 2, new_pos[1])
                        else:
                            if (x_diff == 1):
                                new_pos = (prev_pos[0], new_pos[1] + y_diff // 2)

                            if (y_diff == 1):
                                new_pos = (new_pos[0] + x_diff // 2, prev_pos[1])

                        rope_new[this_knot_idx] = new_pos
                        prev_pos = new_pos
                rope = rope_new
                field = np.
                for pos in rope:
                    line = ['.'] * 10
                    line[]
                print(rope_new)

        return len(set(tail_pos_history))


puzzle = Day9()

if SUBMIT:
    puzzle.submit(sub_b = False)
    
else:
    puzzle.init_data()
    #res_a = puzzle.solve_a()
    res_b = puzzle.solve_b()
    #assert(res_a == 13)
    assert(res_b == 36)