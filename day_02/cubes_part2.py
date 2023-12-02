import re
import os


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

example = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
]

def get_rgb(txt):
    r = re.findall('(\d+) red', txt)
    g = re.findall('(\d+) green', txt)
    b = re.findall('(\d+) blue', txt)

    output = [0, 0, 0]
    if r:
        output[0] = int(r[0])
    if g:
        output[1] = int(g[0])
    if b:
        output[2] = int(b[0])

    return output

def is_possible(rgb):
    output = True
    if rgb[0] > 12 or rgb[1] > 13 or rgb[2] > 14:
        output = False

    return output

def get_least_possible(rgbs):
    rs = []
    gs = []
    bs = []

    for rgb in rgbs:
        rs.append(rgb[0])
        gs.append(rgb[1])
        bs.append(rgb[2])

    return [max(rs), max(gs), max(bs)]


result = 0

with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    for id_, line_raw in enumerate(input_, start=1):
        line = line_raw.replace('\n', '')
        if not line:
            continue
        game = line.split(':')[1].split(';')

        min_possible = get_least_possible([get_rgb(draw) for draw in game])
        power = min_possible[0] * min_possible[1] * min_possible[2]
        # print(id_, power)
        result += power

print(result)