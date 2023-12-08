import re
import os
import math
from typing import List, Set, Dict
from dataclasses import dataclass
from copy import deepcopy


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

def get_denominators(nr: int):
    output = []
    lim = math.floor(math.sqrt(round(nr, 6)))
    i = 2
    while i <= lim:
        d, m = divmod(nr, i)
        if m == 0:
            output.append(i)
            nr = d
        else:
            i += 1
    output.append(nr)
    return output

def get_multipliers(denominators_list: List[List[int]]):
    multipliers: List[int] = []
    for dens1 in denominators_list:
        while dens1:
            d1 = dens1[0]
            multipliers.append(d1)
            for idx2, dens2 in enumerate(denominators_list):
                if d1 in dens2:
                    denominators_list[idx2].remove(d1)
    return multipliers

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

length = len(directions)
paths: List[int] = []
denominators: List[List[int]] = []
multipliers: List[int] = []

# Each path from ##A to ##Z has a fixed length which repeats periodically (see part2_experiments)
# -> find length of each path
for i, pos in enumerate(positions):
    ctr = 0
    idx = 0
    while not pos.endswith("Z"):
        direction = directions[idx]

        pos = map[pos][direction]

        idx += 1
        if idx >= length:
            idx = 0

        ctr += 1

    paths.append(ctr)

# -> Get denominators and construct the lowest common product for the present denominators
for path in paths:
    denominators.append(get_denominators(path))

multipliers = get_multipliers(denominators)

result = 1
for m in multipliers:
    result *= m

print(result)
