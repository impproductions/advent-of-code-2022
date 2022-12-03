from os import path

file_path = path.join(path.dirname(path.abspath(__file__)) + "/input.txt")
with open(file_path, "r") as f:
    data = f.read().splitlines()

# convert letters to their respective priorities
sacks = [[ord(c)-96 if c.islower() else ord(c)-38 for c in l] for l in data]


def part1():
    return sum([
        next(iter(
            set(sack[:len(sack) // 2]) & set(sack[(len(sack) // 2):])
        )) for sack in sacks
    ])


def part2():
    groups = [sacks[i:i+3] for i in range(0, len(sacks), 3)]

    return sum([next(iter(
        set(elf_1) & set(elf_2) & set(elf_3)
    )) for elf_1, elf_2, elf_3 in groups])


print(part1())
print(part2())
