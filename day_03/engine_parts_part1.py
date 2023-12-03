import re
import os
from collections import namedtuple
from typing import Dict


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

example = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
]

example2 = [
    "467..114..",
    "...*......",
    "..35...633",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
]


Position = namedtuple('Position', ['x', 'y'])
Element = namedtuple('Element', ['value', 'size'])
numbers: Dict[Position,Element] = {}
symbols: Dict[Position,Element] = {}


def read_info_from_line(txt, line_nr):
    line_end = len(txt) - 1
    nr_txt = ''
    for i, c in enumerate(txt):
        sym = False
        if c != '.':
            if c in '0123456789':
                nr_txt = nr_txt + c
            else:
                symbols[Position(i, line_nr)] = Element(c, 1)
                sym = True
        if (c == '.' or i == line_end or sym) and nr_txt:
            size = len(nr_txt)
            numbers[Position(i-size, line_nr)] = Element(int(nr_txt), size)
            nr_txt = ''

result = 0
numbers_with_symbols = []
numbers_without_symbols = []

with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    # input_ = example2
    for line_nr, line_raw in enumerate(input_):
        line = line_raw.replace('\n', '')
        if not line:
            continue
        read_info_from_line(line, line_nr)

    for (x,y), number in numbers.items():
        # get area around the number
        # (the area of the number is also included, but for these purposes it doesn't make much difference)
        surr = set()
        for shift in range(number.size):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    surr.add((x+shift+i, y+j))

        # check if there is a symbol in the area
        if any(x in symbols for x in surr):
            numbers_with_symbols.append(number.value)
        else:
            numbers_without_symbols.append(number.value)

# print(numbers)
# print(numbers_with_symbols)
print(numbers_without_symbols)
print(sum(numbers_with_symbols))
