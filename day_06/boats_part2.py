import re
import os
import time
import math
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


boat = Boat

result = 0


with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    for line_nr, line_raw in enumerate(input_):
        line = ''.join(pattern.findall(line_raw.strip('\n')))

        if line_nr == 0:
            boat.time = int(line)
        else:
            boat.distance = int(line)

# # Time: 8.5s
# start = time.perf_counter()
# for t in range(boat.time):
#     d = t * (boat.time - t)
#     if d > boat.distance:
#         result += 1
# end = time.perf_counter()

# Time: 1.5s
# start = time.perf_counter()
# for t in range(boat.time):
#     d = t * (boat.time - t)
#     if d > boat.distance:
#         if boat.time % 2 == 0:
#             result = ((boat.time // 2) - t) * 2 + 1
#         else:
#             result = ((boat.time // 2) - t + 1) * 2
#         break
# end = time.perf_counter()

# Time: cca 0.000013s
start = time.perf_counter()

lim = math.floor((boat.time / 2) ** 2)
dif = lim - boat.distance

if dif > 0:
    if boat.time % 2 == 0:
        x = math.sqrt(abs(dif - 0.01))
        result = 2 * (math.ceil(x) - 1) + 1
    else:
        x = 0.5 * (math.sqrt(4 * dif + 1) - 1)
        result = 2 * math.ceil(x)

end = time.perf_counter()

print(result)
print(result == 35349468)
print(end - start)
