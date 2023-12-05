import re
import os
from typing import List, Set, Dict
from dataclasses import dataclass
from copy import deepcopy


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

example = [
    "seeds: 79 14 55 13",
    "",
    "seed-to-soil map:",
    "50 98 2",
    "52 50 48",
    "",
    "soil-to-fertilizer map:",
    "0 15 37",
    "37 52 2",
    "39 0 15",
    "",
    "fertilizer-to-water map:",
    "49 53 8",
    "0 11 42",
    "42 0 7",
    "57 7 4",
    "",
    "water-to-light map:",
    "88 18 7",
    "18 25 70",
    "",
    "light-to-temperature map:",
    "45 77 23",
    "81 45 19",
    "68 64 13",
    "",
    "temperature-to-humidity map:",
    "0 69 1",
    "1 0 69",
    "",
    "humidity-to-location map:",
    "60 56 37",
    "56 93 4",
]


seed_template = {
    'seed': 0,
    'soil': None,
    'fertilizer': None,
    'water': None,
    'light': None,
    'temperature': None,
    'humidity': None,
    'location': None,
}

order = ['seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity', 'location']
order_index = 0
current_source = order[0]
current_target = order[order_index]

pattern_start = re.compile(r'\d+')
pattern = re.compile(r'(\d+) (\d+) (\d+)')


seeds: List[Dict[str,int]] = []
used_seeds: List[Dict[str,int]] = []

result = 0


with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    for line_nr, line_raw in enumerate(input_):
        line = line_raw.strip('\n')
        if line_nr == 0:
            seeds_txt = pattern_start.findall(line)
            for id_ in seeds_txt:
                seed = deepcopy(seed_template)
                seed['seed'] = int(id_)
                seeds.append(seed)
        elif not line:
            continue
        else:
            conversion = pattern.match(line)
            if not conversion:
                
                for seed in seeds:
                    if seed[current_target] is None:
                        seed[current_target] = seed[current_source]

                used_seeds = []
                order_index += 1
                current_source = current_target
                current_target = order[order_index]
            else:
                if len(used_seeds) == len(seeds):
                    continue
                dst = int(conversion.group(1))
                src = int(conversion.group(2))
                cnt = int(conversion.group(3))
                for seed in seeds:
                    if seed not in used_seeds and seed[current_source] in range(src, src+cnt):
                        used_seeds.append(seed)
                        seed[current_target] = seed[current_source] - src + dst

for seed in seeds:
    if seed["location"] is None:
        seed["location"] = seed["humidity"]
    print(seed)

print(min([seed["location"] for seed in seeds]))
