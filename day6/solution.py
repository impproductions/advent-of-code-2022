from pathlib import Path

path = Path(__file__).parent / "example.txt"
with path.open() as file:
    input = file.read()

def find_marker_end(length):
    for i in range(0, len(input)-length):
        if len(set(input[i:i+length])) == length:
            return i + length

def part1():
    return find_marker_end(4)

def part2():
    return find_marker_end(14)

print(part1())
print(part2())
