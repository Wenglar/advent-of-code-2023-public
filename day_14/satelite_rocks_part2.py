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

chars = ('O',)

def get_hash(field: List[List[str]]) -> int:
    obstacles = set()
    for i, line in enumerate(field):
        for j, c in enumerate(line):
            if c in chars:
                obstacles.add((i,j))
    return hash(frozenset(obstacles))

def get_load(field: List[List[str]]) -> int:
    output = 0
    for y, line in enumerate(field):
        output += ((y_size - y) * line.count('O'))
    return output


field: List[List[str]] = []


with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    for line_raw in input_:
        line = line_raw.strip('\n')
        field.append(list(line))

y_size = len(field)
x_size = len(field[0])

history_hash: List[int] = []
history_load: List[int] = []
found  = None
first = None
second = None
i = 0

s = time.perf_counter()
while found is None:
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

    h = get_hash(field)
    
    if h not in history_hash:
        history_hash.append(h)
        history_load.append(get_load(field))
    else:
        print(f"Hash {h} from iteration {i} found in previous iteration {history_hash.index(h)}")
        found = h
        second = i
        first = history_hash.index(h)

    i += 1

cycle_size = second - first

target_cycle = (1000000000 - 1 - first) % cycle_size + first

result = history_load[target_cycle]


print(result)
print(time.perf_counter() - s)
# 1000000000 cycles: 2.25s
