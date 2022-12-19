from pathlib import Path
from functools import reduce

path = Path(__file__).parent / "example.txt"
with path.open() as file:
    input = file.read().splitlines()

cubes = set([tuple(int(s) for s in line.split(",")) for line in input])


def get_faces(cube):
    x, y, z = cube
    return set((
        (x+1, y, z),
        (x-1, y, z),
        (x, y+1, z),
        (x, y-1, z),
        (x, y, z+1),
        (x, y, z-1)
    ))


def get_free_faces(cube, cubes):
    return get_faces(cube) - cubes


def get_touching_faces(cube, cubes):
    return get_faces(cube) & cubes


def grow_bubble(bubble):
    return reduce(lambda p, c: p | get_free_faces(c, bubble), bubble, set())


def shrink_bubble(bubble, inside):
    return reduce(lambda p, c: p | get_touching_faces(c, inside), bubble, set())


def expand(bubble):
    limit = max([max(col)-min(col) for col in [[cube[i]
                for cube in bubble] for i in range(3)]]) // 2 + 1
    inside = bubble
    for i in range(limit):
        inside = inside | bubble
        bubble = grow_bubble(bubble) - inside

    return bubble, inside


def contract(bubble, inside, original):
    while len(bubble - original) > 0:
        bubble = shrink_bubble(bubble, inside) - original
        inside = inside - bubble

    return inside


def part1():
    return sum([len(get_free_faces(cube, cubes)) for cube in cubes])


def part2():
    bubble, inside = expand(cubes)
    solid = contract(bubble, inside, cubes)

    return sum([len(get_free_faces(cube, solid)) for cube in solid])


print(part1())
print(part2())
