from pathlib import Path
from math import ceil, floor
from pprint import pprint

path = Path(__file__).parent / "input.txt"
with path.open() as file:
    input = file.read().splitlines()

moves = [tuple(map(int, line.replace("R ", "0,+")
                   .replace("L ", "0,-")
                   .replace("U ", "1,+")
                   .replace("D ", "1,-")
                   .split(","))) for line in input]


def sign(n):
    if n == 0:
        return 0
    if n < 0:
        return -1
    if n > 0:
        return 1


def cap(n):
    return sign(n) * min(abs(n), 1)


def follow(H, T):
    new_pos = T
    hx, hy = H
    tx, ty = T
    dx, dy = (hx-tx, hy-ty)

    if abs(dx) == 2 or abs(dy) == 2:
        new_pos = (tx + cap(dx), ty + cap(dy))

    return tuple(new_pos)


def simulate_rope(length):
    visited = set()
    rope = [[0,0]] + [(0, 0) for i in range(1, length)]

    for move in moves:
        axis, amt = move

        # execute the movement 1 step at a time
        for _ in range(abs(amt)):
            # move the head
            rope[0][axis] += sign(amt)

            # for every element of the rope, up to the tail
            for pos in range(1, len(rope)):
                rope[pos] = follow(rope[pos-1], rope[pos])

            # track the last element of the rope
            visited.add(rope[length-1])

    return len(visited)


def part1():
    return simulate_rope(2)


def part2():
    return simulate_rope(10)


print(part1())
print(part2())
