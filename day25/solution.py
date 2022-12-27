from pathlib import Path
from math import ceil, log
from pprint import pprint

path = Path(__file__).parent / "input.txt"
with path.open() as file:
    input = file.read().splitlines()

ref = {"0": 0, "1": 1, "2": 2, "=": -2, "-": -1}


def to_base5(n):
    result = ""
    while n > 0:
        result += str(n % 5)
        n = n // 5
    return result[::-1] or "0"


def to_snafu(n):
    n = to_base5(n)
    result = ""
    remainder = 0

    for d in n[::-1]:
        result = list(ref.keys())[(remainder + int(d)) % 5] + result
        remainder = 1 if (int(d) + remainder) > 2 else 0

    return "1" * remainder + str(result)


def to_base10(n):
    return sum([5 ** i * ref[d] for i, d in enumerate(n[::-1])])


def part1():
    return to_snafu(sum([to_base10(n) for n in input]))


print(part1())
