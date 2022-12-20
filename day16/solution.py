from pathlib import Path
from functools import cache

path = Path(__file__).parent / "input.txt"
with path.open() as file:
    input = file.read().splitlines()

flows = {line.split("; ")[0].split(" has ")[
    0][-2:]: int(line.split("; ")[0].split("=")[1]) for line in input}
connections = {line.split("; ")[0].split(" has ")[0][-2:]: line.split("; ")[
    1].replace("valves", "valve").split("valve ")[1].split(", ") for line in input}
opened = frozenset()


@cache
def visit(node: str, opened: frozenset, time_remaining: int, elephant: bool):
    score = 0
    if time_remaining <= 0:
        return visit("AA", opened, 26, False) if elephant else score

    # decide whether to open
    if not node in opened and flows[node] > 0:
        score = max(score, flows[node] * (time_remaining - 1) +
                    visit(node, opened | {node}, time_remaining - 1, elephant))

    # visit other nodes
    for next_node in connections[node]:
        if not next_node in opened:
            score = max(score, visit(next_node, opened,
                        time_remaining - 1, elephant))

    return score


def part1():
    return visit("AA", opened, 30, False)


def part2():
    return visit("AA", opened, 26, True)


print(part1())
print(part2())
