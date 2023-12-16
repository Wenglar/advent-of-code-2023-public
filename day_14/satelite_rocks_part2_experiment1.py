import re
import os
import time
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
    input_ = example
    for y, line_raw in enumerate(input_):
        line = line_raw.strip('\n')
        for x, c in enumerate(line):
            if c == '#':
                fixed.add((x, y))
            elif c == "O":
                mobile.add((x, y))

y_edge = y + 1
x_edge = x + 1

s = time.perf_counter()
for i in range(100000):
    for x, y in sorted(list(mobile), key=lambda x: (x[1])):
        y -= 1
        while y > -1 and (x,y) not in fixed and (x,y) not in mobile2:
            y -= 1

        mobile2.add((x, y+1))

    mobile = set()

    for x, y in sorted(list(mobile2), key=lambda x: (x[0])):
        x -= 1
        while x > -1 and (x,y) not in fixed and (x,y) not in mobile:
            x -= 1

        mobile.add((x+1, y))

    mobile2 = set()

    for x, y in sorted(list(mobile), key=lambda x: (x[1]), reverse=True):
        y += 1
        while y < y_edge and (x,y) not in fixed and (x,y) not in mobile2:
            y += 1

        mobile2.add((x, y-1))

    mobile = set()

    for x, y in sorted(list(mobile2), key=lambda x: (x[0]), reverse=True):
        x += 1
        while x < x_edge and (x,y) not in fixed and (x,y) not in mobile:
            x += 1

        mobile.add((x-1, y))

    mobile2 = set()

    result = 0

for rock in mobile:
    result += (y_edge - rock[1])
    # print(rock)

print(result)
print(time.perf_counter() - s)
# 100000 cycles: 9.75s
