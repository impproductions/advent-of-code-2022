from pathlib import Path


path = Path(__file__).parent / "input.txt"
with path.open() as file:
    input = file.read().splitlines()

start = (500, 0)
occupied = {start: "+"}

for path in input:
    split_path = path.split(" -> ")
    for i, point in enumerate(split_path):
        if i >= 1:
            px, py = [int(c) for c in split_path[i-1].split(",")]
            cx, cy = [int(c) for c in split_path[i].split(",")]
            for i in range(*sorted((py, cy+1))):
                occupied[(cx, i)] = "#"
            for i in range(*sorted((px, cx+1))):
                occupied[(i, cy)] = "#"

min_x, max_x = min([p[0] for p in occupied]), max([p[0] for p in occupied])
max_y = max([p[1] for p in occupied])


def check_spot(next, has_floor):
    if not has_floor and not next[0] in range(min_x, max_x+1):
        return "void"
    if occupied.get(next) == None:
        if next[1] == max_y+2:
            return "rest"
        return next

    return "wall"


def get_next_free(pos, has_floor):
    next = check_spot((pos[0], pos[1] + 1), has_floor)
    if next != "wall":
        return next

    next = check_spot((pos[0]-1, pos[1] + 1), has_floor)
    if next != "wall":
        return next

    next = check_spot((pos[0]+1, pos[1] + 1), has_floor)
    if next != "wall":
        return next

    return "rest"


def drop_sand(has_floor):
    while True:
        current_pos = start
        while current_pos != "rest":
            next = get_next_free(current_pos, has_floor)
            if next == "void":
                return
            elif next == "rest":
                if occupied.get(current_pos, None) == "+":
                    return
                occupied[current_pos] = "o"
            current_pos = next


def part1():
    drop_sand(False)

    return sum(1 for cell in occupied.values() if cell == "o")


def part2():
    drop_sand(True)

    return sum(1 for cell in occupied.values() if cell == "o" or cell == "+")


print(part1())
print(part2())
