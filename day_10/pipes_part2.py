import re
import os
from typing import List, Set, Dict
from dataclasses import dataclass
from collections import namedtuple
from copy import deepcopy


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

example = [
    "..........",
    ".S------7.",
    ".|F----7|.",
    ".||OOOO||.",
    ".||OOOO||.",
    ".|L-7F-J|.",
    ".|II||II|.",
    ".L--JL--J.",
    "..........",
]

example2 = [
    "OF----7F7F7F7F-7OOOO",
    "O|F--7||||||||FJOOOO",
    "O||OFJ||||||||L7OOOO",
    "FJL7L7LJLJ||LJIL-7OO",
    "L--JOL7IIILJS7F-7L7O",
    "OOOOF-JIIF7FJ|L7L7L7",
    "OOOOL7IF7||L7|IL7L7|",
    "OOOOO|FJLJ|FJ|F7|OLJ",
    "OOOOFJL-7O||O||||OOO",
    "OOOOL---JOLJOLJLJOOO",
]

example3 = [
    "FF7FSF7F7F7F7F7F---7",
    "L|LJ||||||||||||F--J",
    "FL-7LJLJ||||||LJL-77",
    "F--JF--7||LJLJIF7FJ-",
    "L---JF-JLJIIIIFJLJJ7",
    "|F|F-JF---7IIIL7L|7|",
    "|FFJF7L7F-JF7IIL---7",
    "7-L-JL7||F7|L7F-7F7|",
    "L.L7LFJ|||||FJL7||LJ",
    "L7JLJL-JLJLJL--JLJ.L",
]

Position = namedtuple("Position", ['x', 'y'])

source_targets: Dict[Position, List[Position]] = {}
target_sources: Dict[Position, List[Position]] = {}
symbols: Dict[Position, str] = {}
horizontal_transitions: Set[Position] = set()
start = Position(-1, -1)

y_min = 0
x_min = 0

## Get the pipe parts and symbols
with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    # input_ = example2
    # input_ = example3
    for y, line_raw in enumerate(input_):
        line = line_raw.strip('\n')
        for x, c in enumerate(line):
            pos = Position(x, y)
            if c == '|':
                symbols[pos] = c
                source_targets[pos] = [Position(x, y-1), Position(x, y+1)]
            elif c == '-':
                symbols[pos] = c
                source_targets[pos] = [Position(x-1, y), Position(x+1, y)]
            elif c == 'L':
                symbols[pos] = c
                source_targets[pos] = [Position(x, y-1), Position(x+1, y)]
            elif c == 'J':
                symbols[pos] = c
                source_targets[pos] = [Position(x, y-1), Position(x-1, y)]
            elif c == 'F':
                symbols[pos] = c
                source_targets[pos] = [Position(x, y+1), Position(x+1, y)]
            elif c == '7':
                symbols[pos] = c
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

y_max = y
x_max = x

# print(source_targets)
# print(target_sources)

## Copy start (probably reundant)
source_targets[start] = target_sources[start]

# print(start)
# print(source_targets[start])

## Get the loop: pipe length and pipe parts
pipe_length = 0

last_node = start
node = source_targets[start][0]
pipe_length += 1

loop: Set[Position] = set()
loop.add(start)
loop.add(node)

while node != start:
    for potential in source_targets[node]:
        if potential != last_node:
            last_node = node
            node = potential
            pipe_length += 1
            loop.add(node)
            break

## Replace the "S" symbol
start_dirs = source_targets[start]
x = start.x
y = start.y

for c in '|-LJF7':
    if c == '|':
        pos_comb = [Position(x, y-1), Position(x, y+1)]
    elif c == '-':
        pos_comb = [Position(x-1, y), Position(x+1, y)]
    elif c == 'L':
        pos_comb = [Position(x, y-1), Position(x+1, y)]
    elif c == 'J':
        pos_comb = [Position(x, y-1), Position(x-1, y)]
    elif c == 'F':
        pos_comb = [Position(x, y+1), Position(x+1, y)]
    elif c == '7':
        pos_comb = [Position(x, y+1), Position(x-1, y)]

    if all(pos_comb[x] in source_targets[start] for x in range(2)):
        symbols[start] = c
        break

## Count fields contained in the loop
cnt = 0
last_symbol = ""

for y in range(y_min, y_max+1):
    in_loop = False
    for x in range(x_min, x_max+1):
        pos = Position(x, y)
        if pos in loop:
            symbol = symbols[pos]
            if symbol in "|LF7J":
                if (symbol == "7" and last_symbol == "L") or (symbol == "J" and last_symbol == "F"):
                    pass
                else:
                    in_loop = not in_loop
                last_symbol = symbol
        elif in_loop:
            print(pos)
            cnt += 1

print(cnt)

# 666 is too high
