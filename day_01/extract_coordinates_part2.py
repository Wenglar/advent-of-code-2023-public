import re
import os


DIRPATH = os.path.dirname(__file__)
FILEPATH = os.path.abspath(os.path.join(DIRPATH, 'input.txt'))

example = [
    "two1nine",
    "eightwothree",
    "abcone2threexyz",
    "xtwone3four",
    "4nineeightseven2",
    "zoneight234",
    "7pqrstsixteen",
]

def decode_word_digits(txt):
    assert isinstance(txt, str)
    txt = txt.replace('one', 'o1e').replace('two', 't2o').replace('three', 't3e').replace('four', 'f4r') \
            .replace('five', 'f5e').replace('six', 's6x').replace('seven', 's7n').replace('eight', 'e8t') \
            .replace('nine', 'n9e')
    # print(txt)
    return(txt)

def get_number(txt):
    digits = re.findall('(\d)', txt)
    nr = digits[0] + digits[-1]
    # print(nr)
    return int(nr)


result = 0

with open(FILEPATH) as input_:
    # input_ = example
    for line in input_:
        result += get_number(decode_word_digits(line))

print(result)
