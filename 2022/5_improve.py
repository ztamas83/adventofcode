import copy
from aocd import submit
import re
from queue import LifoQueue as lq
from collections import deque, OrderedDict as od

from tools import get_data

data = get_data(day=5, year=2022, remote=True)

stacks = {}
moves = []

for line in data:
    if move := re.match('move ([0-9]+) from ([1-9]+) to ([1-9]+)\s?', line):
        moves.append([int(move.group(1)), int(move.group(2)), int(move.group(3))])
    elif re.match('.*\[[A-Z]\].*', line):
        for cratepos in range(1,len(line),4):
            if not line[cratepos].strip():
                continue
            stackno = (cratepos - 1) // 4
            if not stacks.get(stackno):
                stacks[stackno] = []
            stacks[stackno].append(line[cratepos])

def b() -> list:
    stack_b = copy.deepcopy(stacks)
    answer = [None] * len(stack_b)
    for m in moves:
        fr = m[1]-1
        to = m[2]-1 
        print(f'move {m[0]} from {stack_b[fr]} to {stack_b[to]}')
        for x in reversed(stack_b[fr][0:m[0]]):
            stack_b[fr].pop(0)
            stack_b[to].insert(0, x)

        if stack_b[fr]:
            answer[fr] = stack_b[fr][0]
        if stack_b[to]:
            answer[to] = stack_b[to][0]
       
        print(f'after move from {stack_b[fr]} to {stack_b[to]}')
    
    return answer

def a() -> list:
    stack_a = copy.deepcopy(stacks)
    answer = [None] * len(stack_a)
    for m in moves:
        fr = m[1]-1
        to = m[2]-1
        for i in range(m[0]):
            #print(f'move from {stack_a[fr]} to {stack_a[to]}')
            stack_a[to].insert(0, stack_a[fr].pop(0))
        if stack_a[fr]:
            answer[fr] = stack_a[fr][0]
        if stack_a[to]:
            answer[to] = stack_a[to][0]
        #print(f'after move from {stack_a[fr]} to {stack_a[to]}')
    
    return answer

submit(''.join(a()), part='a', day=5, year=2022)
submit(''.join(b()), part='b', day=5, year=2022)
