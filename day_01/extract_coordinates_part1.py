import re
import os


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

example = [
    "1abc2",
    "pqr3stu8vwx",
    "a1b2c3d4e5f",
    "treb7uchet"
]

def get_number(txt):
    digits = re.findall('(\d)', txt)
    nr = digits[0] + digits[-1]
    return int(nr)


result = 0

with open(FILEPATH) as input_:
    # input_ = example
    for line in input_:
        result += get_number(line)

print(result)
