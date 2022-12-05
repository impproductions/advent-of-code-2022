from pathlib import Path

path = Path(__file__).resolve().parent / "input.txt"
with path.open() as file:
    input = file.read().split("\n\n")


def parse_instructions():
    instructions = []
    for instruction in input[1].split("\n"):
        p1, p2 = instruction.split(" from ")
        amt, frm, to = int(p1.split("move ")[1]), *[int(n) - 1 for n in p2.split(" to ")]
        instructions.append((amt, frm, to))

    return instructions

def parse_crate_configuration():
    relevant_chars = [input[0][i + 1] for i in range(0, len(input[0]), 4)]
    crate_count = int(relevant_chars[-1])
    return [list(reversed([c for c in relevant_chars[i::crate_count][:-1] if c != " "])) for i in range(crate_count)]

initial_configuration = parse_crate_configuration()
instructions = parse_instructions()


def move(amt, frm, to, crates, reverse_moving_stack):
    crates = crates[:]
    residual, to_move = crates[frm][:-amt], crates[frm][-amt:]
    crates[frm] = residual
    if reverse_moving_stack:
        to_move.reverse()
    crates[to] = crates[to] + list(to_move)
    return crates


def do_procedure(instructions, crates, reverse_moving_stack):
    for instruction in instructions:
        crates = move(*instruction, crates, reverse_moving_stack)
    return crates


def part1():
    crates = do_procedure(instructions, initial_configuration, reverse_moving_stack=True)
    return "".join([crate[-1] for crate in crates])


def part2():
    crates = do_procedure(instructions, initial_configuration, reverse_moving_stack=False)
    return "".join([crate[-1] for crate in crates])


print(part1())
print(part2())
