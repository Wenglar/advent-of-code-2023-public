import re
import os
from typing import List, Set, Dict, Tuple
from dataclasses import dataclass
from collections import namedtuple
from copy import deepcopy


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

example = [
    "O....#....",
    "O.OO#....#",
    ".....##...",
    "OO.#O....O",
    ".O.....O#.",
    "O.#..O.#.#",
    "..O..#O..O",
    ".......O..",
    "#....###..",
    "#OO..#....",
]

example_result = [
    "OOOO.#.O..",
    "OO..#....#",
    "OO..O##..O",
    "O..#.OO...",
    "........#.",
    "..#....#.#",
    "..O..#.O.O",
    "..O.......",
    "#....###..",
    "#....#....",
]


fixed: Set[Tuple[int, int]] = set()
mobile: Set[Tuple[int, int]] = set()
mobile2: Set[Tuple[int, int]] = set()


with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    for y, line_raw in enumerate(input_):
        line = line_raw.strip('\n')
        for x, c in enumerate(line):
            if c == '#':
                fixed.add((x, y))
            elif c == "O":
                mobile.add((x, y))

y_edge = y + 1


for x, y in sorted(list(mobile), key=lambda x: (x[1])):
    y -= 1
    while y > -1 and (x,y) not in fixed and (x,y) not in mobile2:
        y -= 1

    mobile2.add((x, y+1))

result = 0

for rock in mobile2:
    result += (y_edge - rock[1])
    # print(rock)

print(result)
