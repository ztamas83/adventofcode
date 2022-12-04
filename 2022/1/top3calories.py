import os
from queue import Queue

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, 'input.txt'), 'r') as f:
    lines = f.readlines()
    all_calories = []
    current_calories = 0
    for line in lines:
        line = line.strip()
        if len(line) == 0:    
            all_calories.append(current_calories)
            current_calories = 0
            continue
        if c := int(line):
            current_calories += c
    all_calories.sort(reverse=True)
    print(sum(all_calories[:3]))
