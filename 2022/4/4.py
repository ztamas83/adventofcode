
from aocd import get_data, submit

in_data = get_data(day=4, year=2022).splitlines()


def a():
    full_overlap = 0
    for pair in in_data:
        areas = []
        for area in pair.split(','):
            r = area.split('-')
            areas.append(set(range(int(r[0]), int(r[1])+1)))
        (a1, a2) = tuple(areas)
        overlap = a1.intersection(a2)
        if (sum(overlap) == sum(a1) or sum(overlap) == sum(a2)):
            full_overlap += 1
        
    return full_overlap

def b():
    overlap = 0
    for pair in in_data:
        areas = []
        for area in pair.split(','):
            r = area.split('-')
            areas.append(set(range(int(r[0]), int(r[1])+1)))
        if len(areas[0].intersection(areas[1])) > 0:
            overlap += 1
        
    return overlap

submit(a(), day=4, year=2022)
submit(b(), day=4, year=2022)

