from aocd import get_data

ROCK = 1
PAPER = 2
SCISSOR = 3

ITEMS = {'A': ROCK, 'B': PAPER, 'C': SCISSOR, 'X': ROCK, 'Y': PAPER, 'Z': SCISSOR}

WIN = 6
DRAW = 3
LOST = 0

PLAY_VALUES = {
    'AX': DRAW,
    'BY': DRAW,
    'CZ': DRAW,
    'AY': WIN,
    'BZ': WIN,
    'CX': WIN
}

total_score = 0
for line in get_data(day=2, year=2022).splitlines():
    play = line.strip().split(' ')
    score = ITEMS[play[1]] + PLAY_VALUES.get(play[0]+play[1], 0)
    print(f"{play} score: {score}")
    total_score += score

print(total_score)      
