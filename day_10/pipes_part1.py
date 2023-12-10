import re
import os
from typing import List, Set, Dict
from dataclasses import dataclass
from collections import namedtuple
from copy import deepcopy


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

example = [
    "-L|F7",
    "7S-7|",
    "L|7||",
    "-L-J|",
    "L|-JF",
]
result1 = 4

example2 = [
    "7-F7-",
    ".FJ|7",
    "SJLL7",
    "|F--J",
    "LJ.LJ",
]
result2 = 8

Position = namedtuple("Position", ['x', 'y'])

source_targets: Dict[Position, List[Position]] = {}
target_sources: Dict[Position, List[Position]] = {}
start = Position(-1, -1)

with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    # input_ = example2
    for y, line_raw in enumerate(input_):
        line = line_raw.strip('\n')
        for x, c in enumerate(line):
            pos = Position(x, y)
            if c == '|':
                source_targets[pos] = [Position(x, y-1), Position(x, y+1)]
            elif c == '-':
                source_targets[pos] = [Position(x-1, y), Position(x+1, y)]
            elif c == 'L':
                source_targets[pos] = [Position(x, y-1), Position(x+1, y)]
            elif c == 'J':
                source_targets[pos] = [Position(x, y-1), Position(x-1, y)]
            elif c == 'F':
                source_targets[pos] = [Position(x, y+1), Position(x+1, y)]
            elif c == '7':
                source_targets[pos] = [Position(x, y+1), Position(x-1, y)]
            elif c == 'S':
                start = pos
                continue
            else:
                continue
            for source in source_targets[pos]:
                if source not in target_sources:
                    target_sources[source] = []
                target_sources[source].append(pos)

# print(source_targets)
# print(target_sources)

source_targets[start] = target_sources[start]

print(start)
print(source_targets[start])

pipe_length = 0

last_node = start
node = source_targets[start][0]
pipe_length += 1

while node != start:
    for potential in source_targets[node]:
        if potential != last_node:
            last_node = node
            node = potential
            pipe_length += 1
            break

# print(pipe_length)

result = pipe_length // 2

print(result)
