import re
import os
from typing import List, Set, Dict, Tuple
from dataclasses import dataclass
from collections import namedtuple
from copy import deepcopy


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

example = [
    "#.##..##.",
    "..#.##.#.",
    "##......#",
    "##......#",
    "..#.##.#.",
    "..##..##.",
    "#.#.##.#.",
    "",
    "#...##..#",
    "#....#..#",
    "..##..###",
    "#####.##.",
    "#####.##.",
    "..##..###",
    "#....#..#",
]


@dataclass
class RockField():
    field: Set[Tuple[int, int]]
    x_lim: int
    y_lim: int


def get_score(field: RockField) -> int:
    hors = 0
    vers = 0

    for x in range(field.x_lim):
        f = deepcopy(field.field)
        r = min(x, (field.x_lim - x - 1))

        for i in range(r + 1):
            x1 = x - i
            x2 = x + 1 + i
            for y in range(field.y_lim + 1):
                is1 = (x1, y) in field.field
                is2 = (x2, y) in field.field
                if is1 and not is2:
                    f.add((x2, y))
                elif is2 and not is1:
                    f.add((x1, y))
        if abs(len(f) - len(field.field)) == 1:
            vers += (x + 1)
            break

    if not vers:
        for y in range(field.y_lim):
            f = deepcopy(field.field)
            r = min(y, (field.y_lim - y - 1))
            sym = True
            for i in range(r + 1):
                y1 = y - i
                y2 = y + 1 + i
                for x in range(field.x_lim + 1):
                    is1 = (x, y1) in field.field
                    is2 = (x, y2) in field.field
                    if is1 and not is2:
                        f.add((x, y2))
                    elif is2 and not is1:
                        f.add((x, y1))
            if abs(len(f) - len(field.field)) == 1:
                hors += (y + 1)
                break

    return hors * 100 + vers


fields: List[RockField] = []
x = 0

with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    field: Set[Tuple[int, int]] = set()
    y = 0
    for line_raw in input_:
        line = line_raw.strip('\n')
        if not line:
            fields.append(RockField(field, x, y-1))
            field = set()
            y = 0
            continue
        for x, c in enumerate(line):
            if c == "#":
                field.add((x,y))
        y += 1

fields.append(RockField(field, x, y-1))


result = 0
for rf in fields:
    # print(rf)
    result += get_score(rf)

print(result)
