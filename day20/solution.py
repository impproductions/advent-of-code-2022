from pathlib import Path

path = Path(__file__).parent / "example.txt"
with path.open() as file:
    input = file.read().splitlines()


def find(index, list):
    for i, pair in enumerate(list):
        if pair[0] == index:
            return i
    return -1


def mix(data: list, times=1, multiplier=1):
    data = [(p[0], p[1] * multiplier) for p in data]
    mixed = data[:]

    for _ in range(times):
        for id, amt in data:
            to_move_index = find(id, mixed)
            removed = mixed.pop(to_move_index)
            mixed.insert((to_move_index + amt) % (len(data) - 1), removed)

    return mixed


def process_coordinates(mixed):
    zero_index = mixed.index(0)
    positions = [(zero_index + 1000) % len(mixed), (zero_index + 2000) %
                 len(mixed), (zero_index + 3000) % len(mixed)]

    return sum([mixed[pos] for pos in positions])

# tag each number so they can be found after mixing
data = [(i, int(line)) for i, line in enumerate(input)]

def part1():
    mixed = [p[1] for p in mix(data)]
    return process_coordinates(mixed)


def part2():
    mixed = [p[1] for p in mix(data, 10, 811589153)]
    return process_coordinates(mixed)


print(part1())
print(part2())
