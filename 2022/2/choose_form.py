from aocd import get_data

ROCK = 1
PAPER = 2
SCISSOR = 3

ITEMS = {'A': ROCK, 'B': PAPER, 'C': SCISSOR}

WIN = 6
DRAW = 3
LOST = 0

WINNING_FORM = {
    'A': PAPER,
    'B': SCISSOR,
    'C': ROCK
}

LOOSING_FORM = {
    'C': PAPER,
    'A': SCISSOR,
    'B': ROCK
}

PLAY_GOAL = {
    'X': LOST,
    'Y': DRAW,
    'Z': WIN,
}



lines = get_data(day=2, year=2022).splitlines()
total_score = 0
for line in lines:
    play = line.strip().split(' ')
    match PLAY_GOAL[play[1]]:
        case 6:
            choosen_form = WINNING_FORM[play[0]]
        case 3:
            choosen_form = ITEMS[play[0]]
        case 0:
            choosen_form = LOOSING_FORM[play[0]]

    score = PLAY_GOAL[play[1]] + choosen_form

    print(f"{play}, goal: {PLAY_GOAL[play[1]]} choosen: {choosen_form}, score: {score}")
    total_score += score

print(total_score)
    