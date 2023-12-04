from puzzle import Puzzle
import re
import math

class DailyPuzzle(Puzzle):
    def __init__(self):
        super(DailyPuzzle, self).__init__(2023, 4)
        self.init_data(remote=True)
    
    def get_winners(self, scratch_card) -> set[int]:
        winning_numbers = set(re.findall('\d+', scratch_card.split('|')[0][scratch_card.index(':')+1:]))
        my_numbers = set(re.findall('\d+', scratch_card.split('|')[1]))
        return my_numbers.intersection(winning_numbers)
    
    def solve_a(self):
        sum = 0
        for card in self._data.splitlines():
            matching = self.get_winners(card)
            if (matching):
                game_value = math.pow(2, len(matching) - 1)
                #print(f'Game - matching numbers {matching}, game value {game_value}')
                sum += game_value
            #else:
                #print('No win')
        return sum
        
    cards: dict[int, int]
    # processes the card and returns the new card numbers won    
    def process_card(self, all_cards, card_no) -> list[int]:
        #card_no = int(re.search('\d+',card.split(':')[0]).group())
        card = all_cards[card_no - 1]
        matching = self.get_winners(card)
        won_cards = list(map(lambda c: card_no + c, range(1, len(matching) + 1)))
        #print(won_cards)
        for won_card in won_cards:
            self.cards[won_card] = self.cards[won_card] + self.cards[card_no]*1
            
        
    def solve_b(self):
        all_cards = self._data.splitlines()
        self.cards = {k: 1 for k in range(1, len(all_cards) + 1)}
        for cardno in range(1, len(all_cards) + 1):
            self.process_card(all_cards, cardno)
        return sum(self.cards.values())
            
    def solve(self):
        return (self.solve_a(), self.solve_b())

solution = DailyPuzzle()
SUBMIT=False

print(solution.solve_a())
print(solution.solve_b())
if (SUBMIT):
    solution.submit()