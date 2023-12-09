import re
import os
from typing import List, Set, Dict
from dataclasses import dataclass
from copy import deepcopy


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

example = [
    "0 3 6 9 12 15",
    "1 3 6 10 15 21",
    "10 13 16 21 30 45",
]

reading_set: List[List[int]] = []
pattern = re.compile(r'([-]?\d+)')

with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    for line_nr, line_raw in enumerate(input_):
        line = pattern.findall(line_raw.strip('\n'))
        readings = [int(x) for x in line]
        reading_set.append(readings)

# print(reading_set)

result = 0

for reading in reading_set:
    a = deepcopy(reading)
    first_numbers: List[int] = [a[0]]

    while not all([x == 0 for x in a]):
        b: List[int] = []
        for i in range(len(a)-1):
            b.append(a[i+1] - a[i])
        a = deepcopy(b)
        first_numbers.insert(0, a[0])

    # print(first_numbers)

    for i in range(len(first_numbers)-1):
        first_numbers[i+1] -= first_numbers[i]

    # print(first_numbers)

    result += first_numbers[-1]


print(result)
