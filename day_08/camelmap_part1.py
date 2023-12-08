import re
import os
from typing import List, Set, Dict
from dataclasses import dataclass
from copy import deepcopy


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

example = [
    "RL",
    "",
    "AAA = (BBB, CCC)",
    "BBB = (DDD, EEE)",
    "CCC = (ZZZ, GGG)",
    "DDD = (DDD, DDD)",
    "EEE = (EEE, EEE)",
    "GGG = (GGG, GGG)",
    "ZZZ = (ZZZ, ZZZ)",
]

example2 = [
    "LLR",
    "",
    "AAA = (BBB, BBB)",
    "BBB = (AAA, ZZZ)",
    "ZZZ = (ZZZ, ZZZ)",
]

pattern = re.compile(r'([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)')


node_template = {
    "L": "",
    "R": ""
}


map: Dict[str, Dict[str, str]] = {}
directions: str = ""

result = 0


with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    # input_ = example2
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

print(map)

position = "AAA"

idx = 0
length = len(directions)

while position != "ZZZ":
    direction = directions[idx]

    position = map[position][direction]

    idx += 1
    if idx >= length:
        idx = 0

    result += 1

print(result)
