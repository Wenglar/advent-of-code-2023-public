import re
import os
from typing import List, Set, Dict
from dataclasses import dataclass
from collections import namedtuple
from copy import deepcopy


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

example = [
    "...#......",
    ".......#..",
    "#.........",
    "..........",
    "......#...",
    ".#........",
    ".........#",
    "..........",
    ".......#..",
    "#...#.....",
]

pattern = re.compile(r"\#")

galaxies: List[List[int]] = []
empty_x: Set[int] = set()
y = 0


with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    for line_raw in input_:
        line = line_raw.strip('\n')
        if y == 0:
            for i in range(len(line)):
                empty_x.add(i)
        for x, c in enumerate(line):
            if c == '#':
                if x in empty_x:
                    empty_x.remove(x)
                galaxies.append([x, y])
        if "#" not in line:
            y += 1
        y += 1

print(empty_x)

# print(galaxies)

for idx, gal in enumerate(galaxies):
    compensate = len([x for x in empty_x if x < gal[0]])
    galaxies[idx][0] += compensate

result = 0
for i, gal1 in enumerate(galaxies):
    for gal2 in galaxies[i+1:]:
        dist = abs(gal1[0] - gal2[0]) + abs(gal1[1] - gal2[1])
        result += dist

print(result)
