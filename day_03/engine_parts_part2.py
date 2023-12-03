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

value_surrs = {}
gear_ratios = {}
gear_values = []

with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    # input_ = example2
    for line_nr, line_raw in enumerate(input_):
        line = line_raw.replace('\n', '')
        if not line:
            continue
        read_info_from_line(line, line_nr)

    # get positions, where there are numbers in the surrounding areas (with the numbers)
    for (x,y), number in numbers.items():
        added = set()
        for shift in range(number.size):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    position = Position(x + shift + i, y + j)
                    if position not in value_surrs:
                        value_surrs[position] = []
                    if position not in added:
                        value_surrs[position].append(number.value)
                        added.add(position)

    # pick only positions with exactly two numbers in their surrounding area
    for position, content in value_surrs.items():
        if len(content) == 2:
            gear_ratios[position] = content

    # check the gear symbol
    for position, symbol in symbols.items():
        if symbol.value == '*' and position in gear_ratios:
            a, b = gear_ratios[position]
            # print(a, b)
            gear_values.append(a*b)

# print(numbers)
# print(gear_ratios)
# print(gear_values)
print(sum(gear_values))
