import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, 'input.txt'), 'r') as f:
    lines = f.readlines()
    max_calories = 0
    current_calories = 0
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            if current_calories > max_calories:
                max_calories = current_calories
            current_calories = 0
            continue
        if c := int(line):
            current_calories += c
    print(max_calories)