from os import path

file_path = path.join(path.dirname(path.abspath(__file__)) + "/input.txt")
with open(file_path, "r") as f:
    data = f.read().splitlines()

input = [[ord(c)-96 if c.islower() else ord(c)-38 for c in l] for l in data]

def part1():
    return sum([next(iter(set(sack[:len(sack) // 2]) & set(sack[(len(sack) // 2):]))) for sack in input])

def part2():
    groups = [input[i:i+3] for i in range(0, len(input), 3)]
    return sum([next(iter(set(group[0]) & set(group[1]) & set(group[2]))) for group in groups])

print(part1())
print(part2())
