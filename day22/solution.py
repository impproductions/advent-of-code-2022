from pathlib import Path
from pprint import pprint
import re
from dataclasses import dataclass


@dataclass
class State():
    position: tuple[int, int]
    rotation: int


def matrix_mult(first, second):
    return [[sum(a*b for a, b in zip(X_row, Y_col))
            for Y_col in zip(*second)] for X_row in first]


def rotate_m(vector, dir: int):
    matrices = [[[0, 1], [-1, 0]],
                [[0, -1], [1, 0]]]

    return tuple(matrix_mult([vector], matrices[dir])[0])


def rotate_n(times, vector, dir):
    result = vector
    for i in range(times):
        result = rotate_m(result, dir)
    return result


def print_grid(points=[]):
    matrix = [[" "] * get_row_bounds(i)[0] + [grid[(x, y)]
                                              for x, y in grid if y == i] for i in range(len(input) - 2)]
    for y, r in enumerate(matrix):
        row = ""
        for x, c in enumerate(r):
            if (x, y) in points:
                c = "X"
            if transform.position == (x, y):
                c = ">v<^"[transform.rotation]
            row += c
        print(row)


def get_row_bounds(row):
    on_row = [x for x in range(matrix_width) if grid.get((x, row), " ") != " "]
    return (min(on_row), max(on_row))


def get_col_bounds(col):
    on_col = [y for y in range(matrix_height)
              if grid.get((col, y), " ") != " "]
    return (min(on_col), max(on_col))


path = Path(__file__).parent / "input.txt"
with path.open() as file:
    input = file.read().splitlines()

instructions = [(int(inst[:-1]), inst[-1])
                for inst in re.findall(".*?[LR]", input[-1])]
instructions = instructions + \
    [(int(re.split("[LR]", input[-1])[-1]), instructions[-1][1])]
grid = {(x, y): char for y, line in enumerate(
    input[:-2]) for x, char in enumerate(line) if char != " "}
matrix_grid = input[:-2]
matrix_size = 50
matrix_height = len(matrix_grid)
matrix_width = max([len(row) for row in matrix_grid])
row_bounds = [get_row_bounds(i) for i in range(matrix_height)]
col_bounds = [get_col_bounds(i) for i in range(matrix_width)]
start = (row_bounds[0][0], 0)
transform = State(start, 0)
rocks = set([point for point in grid if grid[point] == "#"])


def rotate(dir):
    transform.rotation = (transform.rotation + (1 if dir == "R" else -1)) % 4


def wrap_movement(pos, axis):
    pos = list(pos)
    coord = pos[axis]
    min_coord, max_coord = row_bounds[pos[1]
                                      ] if axis == 0 else col_bounds[pos[0]]
    span = max_coord - min_coord
    pos[axis] = (coord - min_coord) % (span + 1) + min_coord

    return tuple(pos)


def move_by(amt, cubic_wrap=False):
    trail = []
    for i in range(amt):
        rot = transform.rotation
        towards = ((1 - rot % 2) * (-1 if rot >= 2 else 1),
                   (rot % 2) * (-1 if rot >= 2 else 1))
        to_x, to_y = towards
        x, y = transform.position
        trail.append((x, y))
        if not cubic_wrap:
            new_pos = wrap_movement((x + to_x, y + to_y), rot % 2)
        else:
            new_pos, rot = wrap_movement_cube((x + to_x, y + to_y), rot)
        if not new_pos in rocks:
            transform.position = new_pos
            transform.rotation = rot

def part1():
    for i, instr in enumerate(instructions):
        dir, rot = instr
        move_by(dir)
        if i < len(instructions)-1:
            rotate(rot)

    result = (transform.position[1]+1) * 1000 + \
        (transform.position[0]+1) * 4 + transform.rotation
    return result


def get_cube(matrix, size):
    cube = {}
    for y in range(len(matrix) // size):
        for x in range(max([len(row) for row in matrix]) // size):
            if x * size >= len(matrix[y * size]):
                continue
            if matrix[y * size][x * size] != " ":
                cube[(x, y)] = "."
    return cube


def point_to_face(point):
    x, y = point
    return (x // matrix_size, y // matrix_size)


def get_free_sides(face, cube):
    x, y = face
    dirs = {
        0: (x+1, y),
        1: (x, y+1),
        2: (x-1, y),
        3: (x, y-1)
    }
    return [free for free in dirs if cube.get(dirs[free], None) == None]


def get_tunnel(cube_face, direction, cube):
    tunnels = {
        ((1, 0), 0): ((2, 0), 0),
        ((1, 0), 1): ((1, 1), 0),
        ((1, 0), 2): ((0, 2), -2),
        ((1, 0), 3): ((0, 3), -3),
        ((2, 0), 0): ((1, 2), 2),
        ((2, 0), 1): ((1, 1), 1),
        ((2, 0), 2): ((1, 0), 0),
        ((2, 0), 3): ((0, 3), 0),
        ((1, 1), 0): ((2, 0), -1),
        ((1, 1), 1): ((1, 2), 0),
        ((1, 1), 2): ((0, 2), -1),
        ((1, 1), 3): ((1, 0), 0),
        ((0, 2), 0): ((1, 2), 0),
        ((0, 2), 1): ((0, 3), 0),
        ((0, 2), 2): ((1, 0), 2),
        ((0, 2), 3): ((1, 1), 1),
        ((1, 2), 0): ((2, 0), -2),
        ((1, 2), 1): ((0, 3), 1),
        ((1, 2), 2): ((0, 2), 0),
        ((1, 2), 3): ((1, 1), 0),
        ((0, 3), 0): ((1, 2), -1),
        ((0, 3), 1): ((2, 0), 0),
        ((0, 3), 2): ((1, 0), 3),
        ((0, 3), 3): ((0, 2), 0)
    }
    return tunnels[(cube_face, direction)]


def wrap_movement_cube(pos, dir):
    pos = list(pos)
    rot = dir
    axis = dir % 2
    coord = pos[axis]
    min_coord, max_coord = row_bounds[pos[1]
                                      ] if axis == 0 else col_bounds[pos[0]]

    if not coord in range(min_coord, max_coord + 1):
        pos[axis] = max(min(coord, max_coord), min_coord)
        tunnel = get_tunnel(point_to_face(tuple(pos)), dir,
                            get_cube(matrix_grid, matrix_size))

        to_face, rot = tunnel
        pos = to_face_coords(pos)
        pos = invert_pos_on_face(pos, dir % 2)
        pos = [c for c in rotate_n(abs(rot), pos, 0 if rot > 0 else 1)]
        pos = to_global_coords(pos, to_face)
        rot = (transform.rotation + rot) % 4

    return (tuple(pos), rot)


def to_face_coords(point):
    x, y = point
    return ((x % matrix_size) - ((matrix_size - 1) / 2)), (y % matrix_size) - ((matrix_size - 1) / 2)


def to_global_coords(point, face):
    x, y = point
    fx, fy = face
    return (int(x + matrix_size * fx + ((matrix_size - 1) / 2)), int(y + matrix_size * fy + ((matrix_size - 1) / 2)))


def invert_pos_on_face(point_on_face, axis):
    x, y = point_on_face
    new_pos = [x, y]
    new_pos[axis] = -point_on_face[axis]
    return tuple(new_pos)


def part2():
    transform.position = start
    transform.rotation = 0
    for i, instr in enumerate(instructions):
        dir, rot = instr
        move_by(dir, True)
        if i < len(instructions)-1:
            rotate(rot)

    result = (transform.position[1]+1) * 1000 + \
        (transform.position[0]+1) * 4 + transform.rotation
    return result


print(part1())
print(part2())
