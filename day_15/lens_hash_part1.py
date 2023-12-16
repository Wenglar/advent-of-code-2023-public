import re
import os
from typing import List, Set, Dict, Tuple
from dataclasses import dataclass
from collections import namedtuple
from copy import deepcopy


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

example = [
    "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7",
]

instructions: List[str] = []

def get_hash(instruction: str) -> int:
    output = 0
    for c in instruction:
        output += ord(c)
        output *= 17
        output &= 0xFF
    return output


with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    for y, line_raw in enumerate(input_):
        instructions = line_raw.strip('\n').split(',')

result = 0

for instruction in instructions:
    result += get_hash(instruction)

print(result)
