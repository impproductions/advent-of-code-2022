from pathlib import Path


# def print_lines(points: dict[tuple, str]):
#     min_x, max_x = min([p[0] for p in occupied]), max([p[0] for p in occupied])
#     min_y, max_y = min([p[1] for p in occupied]), max([p[1] for p in occupied])
#     for y in range(min_y, max_y+1):
#         line = ""
#         for x in range(min_x, max_x+1):
#             line += points.get((x, y), ".")
#         print(line)


path = Path(__file__).parent / "input.txt"
with path.open() as file:
    input = file.read().splitlines()

occupied = {(500, 0): "+"}

for path in input:
    split_path = path.split(" -> ")
    for i, point in enumerate(split_path):
        if i < 1:
            continue
        px, py = [int(c) for c in split_path[i-1].split(",")]
        cx, cy = [int(c) for c in split_path[i].split(",")]
        for i in range(*sorted((py, cy+1))):
            occupied[(cx, i)] = "#"
        for i in range(*sorted((px, cx+1))):
            occupied[(i, cy)] = "#"

min_x, max_x = min([p[0] for p in occupied]), max([p[0] for p in occupied])
max_y = max([p[1] for p in occupied])


def check_spot(pos, has_floor):
    next = pos
    if not has_floor and not next[0] in range(min_x, max_x+1):
        return "void"
    if occupied.get(next) == None:
        if next[1] == max_y+2:
            return "rest"
        return next

    return "empty"


def get_next_free(pos, has_floor):
    next = check_spot((pos[0], pos[1] + 1), has_floor)
    if next != "empty":
        return next

    next = check_spot((pos[0]-1, pos[1] + 1), has_floor)
    if next != "empty":
        return next

    next = check_spot((pos[0]+1, pos[1] + 1), has_floor)
    if next != "empty":
        return next

    return "rest"


def drop_grain(has_floor):
    current_pos = (500, 0)
    while current_pos != "rest":
        next = get_next_free(current_pos, has_floor)
        if next == "void":
            return False
        if next == "rest":
            if occupied.get(current_pos, None) == "+":
                occupied[current_pos] = "o"
                return False
            occupied[current_pos] = "o"
        current_pos = next

    return True


def drop_sand(has_floor):
    can_continue = True
    while can_continue:
        can_continue = drop_grain(has_floor)


def part1():
    drop_sand(False)

    return sum([1 for cell in occupied.values() if cell == "o"])


def part2():
    drop_sand(True)

    return sum([1 for cell in occupied.values() if cell == "o"])


print(part1())
print(part2())
