from aocd import get_data, submit

def get_prio(s: str) -> int:
    offset = 96 if s.islower() else 38
    return ord(s) - offset

backpacks = get_data(day=3, year=2022).splitlines()

print (f'No of backpacks: {len(backpacks)}')
error_items = {}

def a():
    error_sum = 0
    counter = 0
    for backpack in backpacks:
        backpack = backpack.strip()
        compartment_capacity = len(backpack) // 2
        c1 = backpack[:compartment_capacity]
        c2 = backpack[compartment_capacity:]
        for item in c1:
            if item in c2:
                item_prio = get_prio(item)
                error_sum += item_prio
                error_items[counter] = (item, item_prio)
                c2 = c2.replace(item, '')

    return error_sum

def b():
    group_badges = {}
    group_badge_prio_sum = 0
    for group in range(0, (len(backpacks) // 3)):
        offset = group * 3
        (bp1, bp2, bp3) = tuple(backpacks[offset:offset+3])
        for item in set(bp1):
            if item in set(bp2) and item in set(bp3):
                print(f'Group {group} found badge {item}')
                group_badges[group] = (item, get_prio(item))
                group_badge_prio_sum += get_prio(item)
    return group_badge_prio_sum

submit(answer=a(), part='a', day=3, year=2022)
submit(answer=b(), part='b', day=3, year=2022)

