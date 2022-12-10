from pathlib import Path

path = Path(__file__).parent / "input.txt"
with path.open() as file:
    input = file.read().splitlines()

instructions = [[line] if line[0] == "n" else (line.split(" ")[0], int(line.split(" ")[1])) for line in input]

def run():
    i, cycle, waited_time = 0, 0, 0
    x, significant, render = 1, 0, ""

    while i < len(instructions):
        instruction = instructions[i]
        if (cycle % 40 == 39):
            render += "\n"
        else:
            if cycle % 40 in range(x-1, x+2):
                render += "#"
            else:
                render += " "
        if ((cycle + 1) - 20) % 40 == 0:
            significant += (cycle + 1) * x
        if instruction[0] == "noop":
            i += 1
        elif instruction[0] == "addx":
            if waited_time < 1:
                waited_time += 1
            else:
                waited_time = 0
                x += instruction[1]
                i += 1
        cycle += 1
    
    return significant, render

significant, render = run()

def part1():
    return significant

def part2():
    return render


print(part1())
print(part2())
