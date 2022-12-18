from pathlib import Path
from dataclasses import dataclass

@dataclass
class Node():
    value: int
    connections: list

path = Path(__file__).parent / "example.txt"
with path.open() as file:
    input = file.read().splitlines()

valves = {line.split("; ")[0].split(" has ")[0][-2:]: Node(value = int(line.split("; ")[0].split("=")[1]), connections = line.split("; ")[1].replace("valves", "valve").split("valve ")[1].split(", ")) for line in input}
print(valves)

def part1():
    pass


def part2():
    pass

for i in range(1,1152921504606846976):
    if i % 100000000 == 0:
        print(1152921504606846976 / i)
    pass

print (4 ** 30)

print(part1())
print(part2())
