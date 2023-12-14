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


@dataclass
class Position():
    x: int
    y: int


fixed: List[Position] = []
mobile: List[Position] = []


with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    for y, line_raw in enumerate(input_):
        line = line_raw.strip('\n')
        for x, c in enumerate(line):
            if c == '#':
                fixed.append(Position(x, y))
            elif c == "O":
                mobile.append(Position(x, y))

y_edge = y + 1


for idx, rock in enumerate(mobile):
    new_pos = deepcopy(rock)
    new_pos.y -= 1

    while new_pos.y > -1 and new_pos not in fixed and new_pos not in mobile:
        new_pos.y -= 1

    mobile[idx].y = new_pos.y + 1

result = 0
mobile.sort(key=lambda x: (x.x))

for rock in mobile:
    result += (y_edge - rock.y)
    # print(rock.x, rock.y)

print(result)
