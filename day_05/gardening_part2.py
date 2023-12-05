import re
import os
from typing import List, Set, Dict, Union
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


@dataclass
class SeedRange():
    start: int
    end: int

@dataclass
class ConversionRange():
    start: int
    size: int
    target_start: int

    @property
    def end(self) -> int:
        return self.start + self.size - 1

    @property
    def target_end(self) -> int:
        return self.target_start + self.size - 1


def envelops(enveloper: Union[SeedRange, ConversionRange], envelopee: Union[SeedRange, ConversionRange]):
    """ Does `enveloper` envelop the `envelopee` fully? """
    output = False

    if envelopee.start >= enveloper.start and envelopee.end <= enveloper.end:
        output = True

    return output

def contains_end(container: Union[SeedRange, ConversionRange], element: Union[SeedRange, ConversionRange]):
    """ Is end of `element` contained in `container`? """
    output = False

    if element.end >= container.start and element.end <= container.end:
        output = True

    return output

def prune_ranges(ranges: List[SeedRange]):
    output: List[SeedRange] = []

    while ranges:
        range1 = ranges.pop(0)
        for idx, range2 in enumerate(ranges):
            if idx == 0:
                continue
            if envelops(range1, range2):
                # range2 gets erased and is overwritten by range1 for further analysis
                ranges[idx] = range1
                break
            elif envelops(range2, range1):
                # range1 is already popped, range2 will be popped upon analysis later
                break
            elif contains_end(range1, range2):
                # range2.end is in range1 -> range1.start is in range2 -> range1.end can enhance range2
                ranges[idx].end = range1.end
                break
            elif contains_end(range2, range1):
                # range1.end is in range2 -> range1.start can enhance range2
                ranges[idx].start = range1.start
                break
        else:
            # no intersection -> pass along
            output.append(range1)

    return output

def apply_conversion(conversion: ConversionRange, ranges: List[SeedRange]):
    output = []
    idx = 0

    while idx < len(ranges):
        if envelops(conversion, ranges[idx]):
            # Convert the whole range, remove it from input and add it to output -> don't update index
            range_conv = ranges.pop(idx)
            range_conv.start = range_conv.start - conversion.start + conversion.target_start
            range_conv.end = range_conv.end - conversion.start + conversion.target_start
            output.append(range_conv)
        elif envelops(ranges[idx], conversion):
            # Split the range into 3, convert the middle one and leave the outer parts -> don't update index
            range_conv = ranges.pop(idx)
            range1 = SeedRange(range_conv.start, conversion.start-1)
            range2 = SeedRange(conversion.end+1, range_conv.end)
            ranges.extend([range1, range2])
            range_conv.start = conversion.target_start
            range_conv.end = conversion.target_end
            output.append(range_conv)
        elif contains_end(conversion, ranges[idx]):
            # Split the range into two, convert the end part and leave the start part
            range_conv = deepcopy(ranges[idx])
            ranges[idx].end = conversion.start - 1
            range_conv.start = conversion.target_start
            range_conv.end = range_conv.end - conversion.start + conversion.target_start
            output.append(range_conv)
            idx += 1
        elif contains_end(ranges[idx], conversion):
            # Split the range into two, convert the start part and leave the end part
            range_conv = deepcopy(ranges[idx])
            ranges[idx].start = conversion.end + 1
            range_conv.end = conversion.target_end
            range_conv.start = range_conv.start - conversion.start + conversion.target_start
            output.append(range_conv)
            idx += 1
        else:
            idx += 1

    return (ranges, output)


pattern_start = re.compile(r'\d+')
pattern = re.compile(r'(\d+) (\d+) (\d+)')


origin: List[SeedRange] = []
target: List[SeedRange] = []

result = 0


with open(FILEPATH, encoding='utf-8') as input_:
    # input_ = example
    for line_nr, line_raw in enumerate(input_):
        print(f"Line: {line_nr}")
        line = line_raw.strip('\n')
        if line_nr == 0:
            seeds_txt = pattern_start.findall(line)
            for i in range(len(seeds_txt) // 2):
                start = int(seeds_txt[2*i])
                size = int(seeds_txt[2*i+1])
                origin.append(SeedRange(start, start + size - 1))
            print(origin)
        elif not line:
            # copy ranges that were not converted
            target.extend(origin)
            # reduce overlapping ranges and copy into new origin
            origin = prune_ranges(target)
            print(origin)
            # clear target
            target = []
        else:
            conversion_txt = pattern.match(line)
            if not conversion_txt:
                continue
            conversion = ConversionRange(
                target_start=int(conversion_txt.group(1)),
                start=int(conversion_txt.group(2)),
                size=int(conversion_txt.group(3)),
            )

            (origin, output) = apply_conversion(conversion, origin)
            if output:
                target.extend(output)

# one last merge and prune
target.extend(origin)
origin = prune_ranges(target)
print(origin)

target = []

print(min([r.start for r in origin]))
