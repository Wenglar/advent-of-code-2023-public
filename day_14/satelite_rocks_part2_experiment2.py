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


field: List[List[str]] = []


with open(FILEPATH, encoding='utf-8') as input_:
    input_ = example
    for line_raw in input_:
        line = line_raw.strip('\n')
        field.append(list(line))

y_size = len(field)
x_size = len(field[0])

s = time.perf_counter()
for i in range(100000):
    for x in range(x_size):
        target = 0
        for y in range(y_size):
            val = field[y][x]
            if val == '#':
                target = y + 1
            elif val == "O":
                field[y][x] = "."
                field[target][x] = "O"
                target += 1

    for y in range(y_size):
        target = 0
        for x in range(x_size):
            val = field[y][x]
            if val == '#':
                target = x + 1
            elif val == "O":
                field[y][x] = "."
                field[y][target] = "O"
                target += 1

    for x in range(x_size):
        target = y_size - 1
        for y in range(y_size-1, -1, -1):
            val = field[y][x]
            if val == '#':
                target = y - 1
            elif val == "O":
                field[y][x] = "."
                field[target][x] = "O"
                target -= 1

    for y in range(y_size):
        target = x_size - 1
        for x in range(x_size-1, -1, -1):
            val = field[y][x]
            if val == '#':
                target = x - 1
            elif val == "O":
                field[y][x] = "."
                field[y][target] = "O"
                target -= 1

result = 0

for y, line in enumerate(field):
    result += ((y_size - y) * line.count('O'))
    # print(''.join(line))

print(result)
print(time.perf_counter() - s)
# 100000 cycles: 10.22s
