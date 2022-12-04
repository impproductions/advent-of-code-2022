from pathlib import Path

from pprint import pprint

path = Path(__file__).resolve().parent / "input.txt"
with path.open() as file:
    input = file.read().splitlines()

data = [[list(map(int, elf.split('-')))
         for elf in pair.split(',')] for pair in input]


def get_overlap(range1, range2):
    internal_extremes = [min(range1[1], range2[1]), max(range1[0], range2[0])]
    left, right = min(internal_extremes), max(internal_extremes)
    overlap = right - left if left in range(*range1) and left in range(*range2) else left-right

    return overlap + 1


def get_length(range):
    return range[1]-range[0]+1


def part1():
    return sum([1 for first, second in data if get_overlap(first, second) == min(get_length(first), get_length(second))])


def part2():
    return sum([1 for first, second in data if get_overlap(first, second) > 0])


print(part1())
print(part2())
