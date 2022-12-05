import copy
from aocd import submit
import re
from queue import LifoQueue as lq
from collections import deque, OrderedDict as od

from tools import get_data

# data = """
#     [D]    
# [N] [C]    
# [Z] [M] [P]
#  1   2   3


# move 1 from 2 to 1
# move 3 from 1 to 3
# move 2 from 2 to 1
# move 1 from 1 to 2
# """.splitlines()

data = get_data(day=5, year=2022, remote=True)

print(data)

stacks_init = {}
moves = []

for line in data:
    if move := re.match('move ([0-9]+) from ([1-9]+) to ([1-9]+)\s?', line):
        moves.append([int(move.group(1)), int(move.group(2)), int(move.group(3))])
        print(moves[-1])
    elif re.match('.*\[[A-Z]\].*', line):
        for charindex in range(0, len(line)):
            # charindex = 1 + 4*crateindex
            if crate := re.match('[A-Z]',line[charindex]):
                stackindex = (charindex - 1) // 4
                currentstack = stacks_init.get(stackindex)
                if not currentstack:
                    stacks_init[stackindex] = []
                stacks_init[stackindex].append(crate.string)

stacks_queue = {}
for i in copy.deepcopy(stacks_init):
    q = lq()
    for c in reversed(stacks_init[i]):
        q.put(c)
    stacks_queue[i] = q

stacks= od(sorted(stacks_queue.items()))

def move_9000(thismove: list):
    fr = thismove[1]-1
    to = thismove[2]-1
    
    for m in range(thismove[0]):
        print(f'move from {stacks[fr].queue} to {stacks[to].queue}')
        if (stacks[fr].empty()):
            continue
        stacks[to].put(stacks[fr].get())
    
    print(f'after move from {stacks[fr].queue} to {stacks[to].queue}')

def move_9001(thismove: list):
    fr = thismove[1]-1
    to = thismove[2]-1 
    print(f'move {thismove[0]} from {stacks[fr].queue} to {stacks[to].queue}')
    tomove = []
        
    for m in range(thismove[0]):
        if (stacks[fr].empty()):
            continue
        tomove.append(stacks[fr].get())
    
    for c in reversed(tomove):
        stacks[to].put(c)
    
    print(f'after move from {stacks[fr].queue} to {stacks[to].queue}')

answer_a = ''
answer_b = ''
for m in moves:
    print(m)
    move_9000(m)

for i in stacks:
    answer_a += stacks[i].get()

for i in copy.deepcopy(stacks_init):
    q = lq()
    for c in reversed(stacks_init[i]):
        q.put(c)
    stacks_queue[i] = q

stacks= od(sorted(stacks_queue.items()))

for m in moves:
    print(m)
    move_9001(m)

for i in stacks:
    answer_b += stacks[i].get()


print(answer_a)
print(answer_b)
submit(answer_a, part='a', day=5, year=2022)
submit(answer_b, part='b', day=5, year=2022)
