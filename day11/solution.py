from pathlib import Path
from math import prod
from dataclasses import dataclass

@dataclass
class Monkey():
    items: list[int]
    operation: str
    test: int
    passed: int
    failed: int
    business = 0


path = Path(__file__).parent / "input.txt"
with path.open() as file:
    input = file.read()


def parse_input(input: str):
    monkeys: list[Monkey] = []
    for monkey in [monkey.split("\n")[1:6] for monkey in input.split("Monkey ")[1:]]:
        monkeys.append(Monkey(
            items=list(map(int, monkey[0].split(": ")[1].split(", "))),
            operation=monkey[1].split("old ")[1],
            test=int(monkey[2].split(" ")[-1]),
            passed=int(monkey[3].split(" ")[-1]),
            failed=int(monkey[4].split(" ")[-1])
        ))
    common_modulo = prod(monkey.test for monkey in monkeys)
    return monkeys, common_modulo


def do_operation(operation: str, input: int):
    operator, operand = operation.split(" ")
    if operand == "old":
        operand = input
    if operator == "*":
        return input * int(operand)
    elif operator == "+":
        return input + int(operand)


def turn(monkey: Monkey, monkeys: list[Monkey], common_modulo: int, divider=1):
    monkey.business += len(monkey.items)

    for item in monkey.items:
        worry_level = do_operation(monkey.operation, item) // divider
        worry_level = worry_level % common_modulo
        target = monkey.passed if worry_level % monkey.test == 0 else monkey.failed
        monkeys[target].items.append(worry_level)

    monkey.items = []
    return monkey


def play(turns: int, part1: bool):
    monkeys, common_modulo = parse_input(input)
    for _ in range(turns):
        for j in range(len(monkeys)):
            turn(monkeys[j], monkeys, common_modulo, 3 if part1 else 1)

    business = sorted([monkey.business for monkey in monkeys])[::-1]
    return business[0] * business[1]


def part1():
    return play(20, True)


def part2():
    return play(10000, False)


print(part1())
print(part2())
