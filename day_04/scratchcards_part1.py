import re
import os
from typing import List, Set
from dataclasses import dataclass


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

example = [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
]


@dataclass
class Card():
    winning: Set[str]
    got: List[str]


pattern = re.compile('\d+')


def read_info_from_line(txt):
    _, txt = txt.split(':')
    winning_txt, got_txt = txt.split('|')

    winning = pattern.findall(winning_txt)
    got = pattern.findall(got_txt)

    return Card(winning, got)

def get_card_value(card: Card):
    value = 0

    for element in card.got:
        if element in card.winning:
            if not value:
                value = 1
            else:
                value *= 2

    return value


result = 0


with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    for line_nr, line_raw in enumerate(input_):
        line = line_raw.replace('\n', '')
        if not line:
            continue
        card = read_info_from_line(line)

        result += get_card_value(card)

print(result)
