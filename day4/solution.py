from pathlib import Path

from pprint import pprint

path = Path(__file__).resolve().parent / "input.txt"
with path.open() as file:
    input = file.read().splitlines()

data = [[list(map(int, elf.split('-'))) for elf in pair.split(',')] for pair in input]

def get_overlap(range_pair):
    # ensure range1 starts before range2
    range1, range2 = sorted(range_pair)
    extension = min(range2) - (max(range1) + 1)
    hanging = max(range1) - max(range2)
    
    return -(min(extension, 0) + max(hanging, 0))

def get_length(r):
    return r[1]-r[0]+1

def part1():
    return len([1 for pair in data if get_overlap(pair) in [get_length(pair[0]), get_length(pair[1])]])
    
def part2():
    return len([1 for pair in data if get_overlap(pair) > 0])

print(part1())
print(part2())