import re
import os
from typing import List, Set, Dict
from dataclasses import dataclass
from copy import deepcopy


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

example = [
    "Time:      7  15   30",
    "Distance:  9  40  200",
]

pattern = re.compile(r'\d+')


@dataclass
class Boat():
    time: int = 0
    distance: int = 0


boats: List[Boat] = []

result = 1


with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    for line_nr, line_raw in enumerate(input_):
        line = pattern.findall(line_raw.strip('\n'))
        if line_nr == 0:
            for t in line:
                boats.append(Boat(time=int(t)))
        else:
            for i, d in enumerate(line):
                boats[i].distance = int(d)

for boat in boats:
    over = 0
    for t in range(boat.time):
        d = t * (boat.time - t)
        if d > boat.distance:
            over += 1
    result = result * over

print(result)
