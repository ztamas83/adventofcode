from puzzle import Puzzle
import re
import math
from functools import cmp_to_key

CARDS = "23456789TJQKA"
CARDS2 = "J23456789TQKA"
HAND_TYPES = [
    "11111", #high card
    "21110", #one pair
    "22100", #two pairs
    "31100", #three of a kind
    "32000", #full house
    "41000", #four of a kind
    "50000", #five of a kind
]

class DailyPuzzle(Puzzle):
    playing_with_joker = False
    def __init__(self):
        super(DailyPuzzle, self).__init__(2023, 7)
        self.init_data(remote=True)
        
    
    def card_value(self, c):
        return CARDS.index(c) if not self.playing_with_joker else CARDS2.index(c)
    
    def get_hand_type(self, hand: list[str]):
        card_count = {k: 0 for (k) in CARDS2} if self.playing_with_joker else {k: 0 for (k) in CARDS}
        for c in hand:
            card_count[c] += 1
        
        sum = 0
        pos = 4
        for (c,n) in sorted(card_count.items(), key = lambda i: i[1], reverse=True):
            if self.playing_with_joker and pos == 4 and c != 'J': #add joker to the highes num of cards
                sum += math.pow(10, pos) * (n + card_count['J'])
            elif self.playing_with_joker and c == 'J':
                continue
            else:
                sum += math.pow(10, pos) * n
            pos -= 1
            if pos < 0:
                break
        
        return int(sum)
    
    def compare_hands(self, hand, compare_with):
        # hand value first
        if hand[0] > compare_with[0]:
            return 1
        if hand[0] < compare_with[0]:
            return -1

        # compare cards
        for pos in range(0, 5):
            if self.card_value(hand[1][pos]) > self.card_value(compare_with[1][pos]):
                return 1
            if self.card_value(compare_with[1][pos]) > self.card_value(hand[1][pos]):
                return -1
        
        #compare rank if cards are the same
        if (hand[1] == compare_with[1]):
            if hand[2] > compare_with[2]:
                return 1
            if compare_with[2] > hand[2]:
                return -1

        return 0
    
    def rank_hands(self):
        hands = []
        for hand in self._data.splitlines():
            cards = list(re.findall('\w', hand.split(' ')[0].strip()))
            bid = int(hand.split(' ')[1].strip())
            hands.append((self.get_hand_type(cards), cards, bid))
        
        sum = 0
        for rank, h in enumerate(sorted(hands, key=cmp_to_key(self.compare_hands))):
            print(f'{h} rank {rank+1}')
            sum += (rank + 1) * h[2]
        
        return sum
  
    def solve_a(self):
        return self.rank_hands()
        
            
    def solve_b(self):
        self.playing_with_joker = True
        return self.rank_hands()
    
    def solve(self):
        return (self.solve_a(), self.solve_b())

solution = DailyPuzzle()
SUBMIT=False

print(solution.solve())

if (SUBMIT):
    solution.submit()