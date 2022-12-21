from pathlib import Path

path = Path(__file__).parent / "example.txt"
with path.open() as file:
    input = file.read().splitlines()


def move_number(index, numbers, map):
    indices = numbers[:]

    move_amt = map[index]
    old_index = numbers[index]
    new_index = (old_index + (move_amt)) % (len(map)-1)
    moving_range = range(min(old_index, new_index),
                         max(old_index, new_index) + 1)
    for i in range(len(numbers)):
        adjustment = 0
        if numbers[i] in moving_range:
            adjustment = 1
            if old_index > new_index:
                adjustment = - 1
            indices[i] = (numbers[i] - adjustment) % len(map)

    indices[index] = new_index
    return indices


def rearrange_numbers(indices, map):
    result = [0] * len(map)
    for i, ind in enumerate(indices):
        result[ind] = map[i]
    return result


def mix(map, times=1, mul=1):
    map = [n * mul for n in map]
    original_arrangement = [i for i in range(len(map))]
    arrangement = original_arrangement

    for _ in range(times):
        for i in range(len(map)):
            arrangement = move_number(i, arrangement, map)

    return rearrange_numbers(arrangement, map)


def process_coordinates(mixed):
    zero_index = mixed.index(0)
    positions = [(zero_index + 1000) % len(mixed), (zero_index + 2000) %
                 len(mixed), (zero_index + 3000) % len(mixed)]

    return sum([mixed[pos] for pos in positions])


def part1():
    map = [int(line) for line in input]

    return process_coordinates(mix(map))


def part2():
    map = [int(line) for line in input]

    return process_coordinates(mix(map, 10, 811589153))


print(part1())
print(part2())
