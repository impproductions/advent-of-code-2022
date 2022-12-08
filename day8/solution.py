from pathlib import Path
from math import ceil, floor
from pprint import pprint

path = Path(__file__).parent / "input.txt"
with path.open() as file:
    input = file.read()

grid = [[int(char) for char in line] for line in input.splitlines()]
height, width = len(grid), len(grid[0])
x_bounds, y_bounds = range(1, len(grid[0])-1), range(1, len(grid)-1)


def look_around(x, y):
    visible = 0
    l, r, t, b = 0, 0, 0, 0
    tree_height = grid[y][x]

    # look left
    for xl in range(x-1, -1, -1):
        watched_height = grid[y][xl]
        l = x - xl
        if tree_height <= watched_height:
            break
        if l == x:
            visible = 1

    # look right
    for xr in range(x+1, len(grid[y])):
        watched_height = grid[y][xr]
        r = xr - x
        if tree_height <= watched_height:
            break
        if r == len(grid[y]) - (x+1):
            visible = 1

    # look up
    for yt in range(y-1, -1, -1):
        watched_height = grid[yt][x]
        t = y - yt
        if tree_height <= watched_height:
            break
        if t == y:
            visible = 1

    # look down
    for yb in range(y+1, len(grid)):
        watched_height = grid[yb][x]
        b = yb - y
        if tree_height <= watched_height:
            break
        if b == len(grid) - (y+1):
            visible = 1

    return visible, l * r * t * b


def part1():
    outer_amount = height * 2 + (width-2) * 2
    visible = [look_around(x, y)[0] for x in x_bounds for y in y_bounds]

    return sum(visible) + outer_amount


def part2():
    scores = [look_around(x, y)[1] for x in x_bounds for y in y_bounds]

    return max(scores)


print(part1())
print(part2())
