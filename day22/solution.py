from pathlib import Path
from dataclasses import dataclass
from math import sqrt, cos, sin, radians
import re


@dataclass
class State():
    position: tuple[int, int]
    rotation: int


path = Path(__file__).parent / "input.txt"
with path.open() as file:
    input = file.read().splitlines()


def matrix_mult(first, second):
    return [[sum(a * b for a, b in zip(x_row, y_col))
            for y_col in zip(*second)] for x_row in first]


def rotate_point(vector, increment):
    angle = radians(90 * abs(increment))
    sign = 1 if increment > 0 else -1 if increment < 0 else 0
    matrix = [[int(cos(angle)), -sign * int(sin(angle))],
              [sign * int(sin(angle)), int(cos(angle))]]

    return tuple(matrix_mult([vector], matrix)[0])


def get_face(point):
    x, y = point
    return (x // grid_size, y // grid_size)


def get_row_bounds(row):
    on_row = [x for x in range(grid_h) if space.get((x, row), " ") != " "]
    return (min(on_row), max(on_row))


def get_col_bounds(col):
    on_col = [y for y in range(grid_w)
              if space.get((col, y), " ") != " "]
    return (min(on_col), max(on_col))


def rotate(dir):
    transform.rotation = (transform.rotation + (1 if dir == "R" else -1)) % 4


def wrap_movement(pos, axis):
    pos = list(pos)
    min_coord, max_coord = row_bounds[pos[1]] \
        if axis == 0 else col_bounds[pos[0]]
    span = max_coord - min_coord
    pos[axis] = (pos[axis] - min_coord) % (span + 1) + min_coord

    return tuple(pos)


def wrap_movement_cube(pos, dir):
    pos = list(pos)
    rot, axis = dir, dir % 2
    coord = pos[axis]
    min_coord, max_coord = row_bounds[pos[1]] \
        if axis == 0 else col_bounds[pos[0]]

    if not coord in range(min_coord, max_coord + 1):
        pos[axis] = max(min(coord, max_coord), min_coord)
        destination_face, rot = get_tunnel(get_face(tuple(pos)), dir)
        pos = to_face_coords(pos)
        pos = invert_pos_on_face(pos, axis)
        pos = rotate_point(pos, -rot)
        pos = to_global_coords(pos, destination_face)
        rot = (transform.rotation + rot) % 4

    return (tuple(pos), rot)


def move_by(amt, cubic_wrap=False):
    for _ in range(amt):
        rot = transform.rotation
        towards = rotate_point((1, 0), -rot)
        x, y = transform.position
        to_x, to_y = towards

        if not cubic_wrap:
            new_pos = wrap_movement((x + to_x, y + to_y), rot % 2)
        else:
            new_pos, rot = wrap_movement_cube((x + to_x, y + to_y), rot)

        if space.get(new_pos) == ".":
            transform.position = new_pos
            transform.rotation = rot


def get_face(point):
    x, y = point
    return (x // grid_size, y // grid_size)


def get_tunnel(cube_face, direction):
    tunnels = {
        ((1, 0), 2): ((0, 2), -2),
        ((1, 0), 3): ((0, 3), -3),
        ((2, 0), 0): ((1, 2), 2),
        ((2, 0), 1): ((1, 1), 1),
        ((2, 0), 3): ((0, 3), 0),
        ((1, 1), 0): ((2, 0), -1),
        ((1, 1), 2): ((0, 2), -1),
        ((0, 2), 2): ((1, 0), 2),
        ((0, 2), 3): ((1, 1), 1),
        ((1, 2), 0): ((2, 0), -2),
        ((1, 2), 1): ((0, 3), 1),
        ((0, 3), 0): ((1, 2), -1),
        ((0, 3), 1): ((2, 0), 0),
        ((0, 3), 2): ((1, 0), 3),
    }
    return tunnels[(cube_face, direction)]


def to_face_coords(point):
    x, y = point
    return ((x % grid_size) - ((grid_size - 1) / 2)), (y % grid_size) - ((grid_size - 1) / 2)


def to_global_coords(point, face):
    x, y = point
    fx, fy = face
    return (int(x + grid_size * fx + ((grid_size - 1) / 2)), int(y + grid_size * fy + ((grid_size - 1) / 2)))


def invert_pos_on_face(point_on_face, axis):
    new_pos = list(point_on_face)
    new_pos[axis] = -point_on_face[axis]
    return tuple(new_pos)


def go(fold=False):
    transform.position = start
    transform.rotation = 0
    for i, instr in enumerate(instructions):
        if i % 2 == 0:
            move_by(instr, fold)
        else:
            rotate(instr)

    return (transform.position[1]+1) * 1000 + \
        (transform.position[0]+1) * 4 + transform.rotation


instructions = [int(inst) if i % 2 == 0 else inst
                for i, inst in enumerate(re.findall("[LR]|\d+", input[-1]))]

space = {(x, y): char for y, line in enumerate(input[:-2])
         for x, char in enumerate(line) if char != " "}
grid = input[:-2]
grid_size = int(sqrt(len(space) // 6))
grid_w, grid_h = len(grid), max([len(row) for row in grid])
cube = {(x, y): "." for y in range(len(grid) // grid_size) for x in range(grid_h)
        if x * grid_size < len(grid[y * grid_size]) and grid[y * grid_size][x * grid_size] != " "}
row_bounds = [get_row_bounds(i) for i in range(grid_w)]
col_bounds = [get_col_bounds(i) for i in range(grid_h)]
start = (row_bounds[0][0], 0)
transform = State(start, 0)


def part1():
    return go()


def part2():
    return go(fold=True)


print(part1())
print(part2())
