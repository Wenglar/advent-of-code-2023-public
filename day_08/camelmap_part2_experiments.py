import re
import os
import math
from typing import List, Set, Dict
from dataclasses import dataclass
from copy import deepcopy


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

example3 = [
    "LR",
    "",
    "11A = (11B, XXX)",
    "11B = (XXX, 11Z)",
    "11Z = (11B, XXX)",
    "22A = (22B, XXX)",
    "22B = (22C, 22C)",
    "22C = (22Z, 22Z)",
    "22Z = (22B, 22B)",
    "XXX = (XXX, XXX)",
]

pattern = re.compile(r'([\S]{3}) = \(([\S]{3}), ([\S]{3})\)')


node_template = {
    "L": "",
    "R": ""
}


map: Dict[str, Dict[str, str]] = {}
positions: List[str] = []
directions: str = ""

result = 0


with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example3
    for line_nr, line_raw in enumerate(input_):
        line = line_raw.strip('\n')
        if line_nr == 0:
            directions = line
        elif not line:
            continue
        else:
            info = pattern.findall(line)
            if info:
                node = deepcopy(node_template)
                node["L"] = info[0][1]
                node["R"] = info[0][2]
                map[info[0][0]] = node
                if info[0][0].endswith("A"):
                    positions.append(info[0][0])
                if node["L"] == node["R"]:
                    print(info[0][0], node)

print(positions)

# exit(0)

def is_end(positions: List[str]):
    output = True
    for pos in positions:
        if not pos.endswith("Z"):
            output = False
            break
    return output

idx = 0
length = len(directions)
ctr = 0

while not is_end(positions):
    direction = directions[idx]

    for i, position in enumerate(positions):
        positions[i] = map[position][direction]

    idx += 1
    if idx >= length:
        idx = 0

    result += 1

    if positions[5].endswith("Z"):
        print(result)
        result = 0
        ctr += 1
        if ctr > 10:
            break

# lengths: List[int] = []

# for i, pos in enumerate(positions):
#     ctr = 0
#     idx = 0
#     while not pos.endswith("Z"):
#         direction = directions[idx]

#         pos = map[pos][direction]

#         idx += 1
#         if idx >= length:
#             idx = 0

#         ctr += 1

#     lengths.append(ctr)

# print(lengths)

# def get_denominators(nr: int):
#     output = []
#     lim = math.floor(math.sqrt(round(nr, 6)))
#     i = 2
#     while i <= lim:
#         d, m = divmod(nr, i)
#         if m == 0:
#             output.append(i)
#             nr = d
#         else:
#             i += 1
#     output.append(nr)
#     return output

# denominators: List[List[int]] = []

# for nr in lengths:
#     denominators.append(get_denominators(nr))

# print(denominators)

# multipliers: List[int] = []

# for dens1 in denominators:
#     while dens1:
#         d1 = dens1[0]
#         multipliers.append(d1)
#         for idx2, dens2 in enumerate(denominators):
#             if d1 in dens2:
#                 denominators[idx2].remove(d1)

# print(multipliers)

# result = 1

# for m in multipliers:
#     result *= m

# print(result)
