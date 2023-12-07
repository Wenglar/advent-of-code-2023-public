import re
import os
from typing import List, Set, Dict
from dataclasses import dataclass
from copy import deepcopy


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

card_vals = {
    "A":0x0D, "K":0x0C, "Q":0x0B, "T":0x09, "9":0x08, "8":0x07,
    "7":0x06, "6":0x05, "5":0x04, "4":0x03, "3":0x02, "2":0x01, "J":0x00
}

example = [
    "32T3K 765",
    "T55J5 684",
    "KK677 28",
    "KTJJT 220",
    "QQQJA 483",
]

pattern = re.compile(r'(\S+) (\d+)')


@dataclass
class Hand():
    cards: str
    bid: int
    value: int = 0
    card_value: int = 0

    def evaluate_hand(self):
        cards = set(list(self.cards))
        jokers = self.cards.count('J')

        occurences: Dict[int, List[str]] = {}
        for card in cards:
            cnt = self.cards.count(card)
            if cnt not in occurences:
                occurences[cnt] = []
            occurences[cnt].append(card)

        # apply jokers
        if jokers:
            if 4 in occurences:
                # if 4 X and 1 J -> 5 X; if 1 X and 4 J -> 5 X
                occurences[5] = occurences.pop(4)
            elif 3 in occurences:
                if jokers == 1:
                    occurences[4] = occurences.pop(3)
                elif jokers == 2:
                    occurences[5] = occurences.pop(3)
                else:
                    if 2 in occurences:
                        occurences[5] = occurences[2].pop(0)
                    else:
                        occurences[4] = occurences[1].pop(0)
            elif 2 in occurences:
                if len(occurences[2]) == 1:
                    # if 2 X and 1 J -> 3 X; if 1 X and 2 J -> 3 X
                    occurences[3] = occurences.pop(2)
                elif len(occurences[2]) == 2:
                    occurences[2+jokers] = [occurences[2].pop(0)]
            elif 1 in occurences:
                occurences[2] = occurences[1].pop(0)

        if 2 in occurences and not occurences[2]:
            occurences.pop(2)

        if 5 in occurences:
            self.value = 7
        elif 4 in occurences:
            self.value = 6
        elif 3 in occurences:
            if 2 in occurences:
                self.value = 5
            else:
                self.value = 4
        elif 2 in occurences:
            if len(occurences[2]) == 2:
                self.value = 3
            elif len(occurences[2]) == 1:
                self.value = 2
        else:
            self.value = 1

    def evaluate_cards(self):
        base = 1
        value = 0

        for c in reversed(self.cards):
            value += (card_vals[c] * base)
            base *= 16

        self.card_value = value


hands: List[Hand] = []

result = 0


with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    for line_nr, line_raw in enumerate(input_):
        line = pattern.findall(line_raw.strip('\n'))
        cards = line[0][0]
        bid = line[0][1]
        hands.append(Hand(cards, int(bid)))

for idx, _ in enumerate(hands):
    hands[idx].evaluate_hand()
    hands[idx].evaluate_cards()

# print(hands)

hands.sort(key= lambda x: (x.value, x.card_value))

# print(hands)

for rank, hand in enumerate(hands, start=1):
    result += (rank * hand.bid)

print(result)

# 248936675 is too high
# 247577156 is too low
# 247656957 is too low
print(result > 247656957 and result < 248936675)
