import re
import os
from typing import List, Set, Dict
from dataclasses import dataclass
from collections import namedtuple
from copy import deepcopy


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

example = [
    ".|...\\....",
    "|.-.\\.....",
    ".....|-...",
    "........|.",
    "..........",
    ".........\\",
    "..../.\\\\..",
    ".-.-/..|..",
    ".|....-|.\\",
    "..//.|....",
]

example_output = [
    "######....",
    ".#...#....",
    ".#...#####",
    ".#...##...",
    ".#...##...",
    ".#...##...",
    ".#..####..",
    "########..",
    ".#######..",
    ".#...#.#..",
]


@dataclass
class Position():
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class PathPart():
    pos: Position
    direction: str


mirrors: Dict[Position, Dict[str, str]] = {}
splitters: Dict[Position, Dict[str, List[str]]] = {}
energized: Dict[Position, List[str]] = {}

paths: List[PathPart] = []

with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    for y, line_raw in enumerate(input_):
        line = line_raw.strip('\n')
        for x, c in enumerate(line):
            if c == "\\":
                mirrors[Position(x,y)] = {
                    ">": "V",
                    "^": "<",
                    "<": "^",
                    "V": ">",
                }
            elif c == "/":
                mirrors[Position(x,y)] = {
                    ">": "^",
                    "^": ">",
                    "<": "V",
                    "V": "<",
                }
            elif c == "-":
                splitters[Position(x,y)] = {
                    "^": ["<", ">"],
                    "V": ["<", ">"],
                    ">": [">",],
                    "<": ["<",],
                }
            elif c == "|":
                splitters[Position(x,y)] = {
                    ">": ["^", "V"],
                    "<": ["^", "V"],
                    "V": ["V",],
                    "^": ["^",],
                }

x_lim = x
y_lim = y

paths.append(PathPart(Position(0, 0), '>'))

while paths:
    path = paths.pop(0)
    # print(path.pos, path.direction)
    if path.pos in energized and path.direction in energized[path.pos]:
        # already visited in the same direction
        continue
    else:
        if path.pos not in energized:
            # not visited at all
            energized[path.pos] = []
        # add direction to visited
        energized[path.pos].append(path.direction)

    new_paths: List[PathPart] = []
    if path.pos in mirrors:
        # curve the beam
        new = deepcopy(path)
        new.direction = mirrors[path.pos][path.direction]
        new_paths.append(new)
    elif path.pos in splitters:
        # split the beam if applicable
        for dir in splitters[path.pos][path.direction]:
            new = deepcopy(path)
            new.direction = dir
            new_paths.append(new)
    else:
        # nada
        new_paths.append(deepcopy(path))

    # print("\t", new_paths)
    for path in new_paths:
        if path.direction == ">":
            path.pos.x += 1
        elif path.direction == "<":
            path.pos.x -= 1
        elif path.direction == "^":
            path.pos.y -= 1
        elif path.direction == "V":
            path.pos.y += 1
        if path.pos.x < 0 or path.pos.x > x_lim or path.pos.y < 0 or path.pos.y > y_lim:
            # out of bounds
            continue
        else:
            paths.insert(0, deepcopy(path))

for y in range(y_lim+1):
    line = []
    for x in range(x_lim+1):
        if Position(x,y) in energized:
            line.append('#')
        else:
            line.append('.')
    # print(''.join(line))
# print(energized)
print(len(energized))
