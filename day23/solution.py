from pathlib import Path

path = Path(__file__).parent / "example.txt"
with path.open() as file:
    input = file.read().splitlines()

elves = set((x, y) for y, line in enumerate(input)
            for x, char in enumerate(line) if char == "#")


def count_empty():
    xs, ys = [x for x, y in elves], [y for x, y in elves]
    w, h = max(xs) + 1 - min(xs), max(ys) + 1 - min(ys)
    return (w * h) - len(elves)


def get_proposal(elf, round):
    directions = {
        (0, -1): ((-1, -1), (0, -1), (1, -1)),
        (0, 1): ((-1, 1), (0, 1), (1, 1)),
        (-1, 0): ((-1, -1), (-1, 0), (-1, 1)),
        (1, 0): ((1, -1), (1, 0), (1, 1)),
    }

    around = set(to_check for dir in directions for to_check in directions[dir]
                 if (to_check[0] + elf[0], to_check[1] + elf[1]) in elves)
    if len(around) == 0:
        return None

    for i in range(4):
        dir = list(directions.keys())[(i + round) % 4]
        target = (dir[0] + elf[0], dir[1] + elf[1])

        if len(around & set(directions[dir])) == 0:
            return target

    return None


def play(max=0):
    counter = 0
    while counter < max if max > 0 else True:
        proponents = {}
        for elf in elves:
            target = get_proposal(elf, counter)
            proponents[target] = proponents.get(target, []) + [elf]

        to_move = {target: proponents[target][0]
                   for target in proponents if len(proponents[target]) == 1}

        if len(to_move) == 0:
            break

        for target in to_move:
            elf = to_move[target]
            elves.remove(elf)
            elves.add(target)

        counter += 1
    return counter


def part1():
    play(10)
    return count_empty()


def part2():
    return play() + 1


# print(part1())
print(part2())
