from pathlib import Path

path = Path(__file__).parent / "example.txt"
with path.open() as file:
    input = file.read().splitlines()


def get_value_map():
    states = {}

    for point in grid:
        x, y = point
        h_rounds = []
        for i in range(h_cycle):
            r = 1 if area[y][(x-i) % h_cycle] == ">" else 0
            l = 1 if area[y][(x-(h_cycle-i)) % h_cycle] == "<" else 0
            h_rounds.append(r + l)

        v_rounds = []
        for i in range(v_cycle):
            u = 1 if area[(y-(v_cycle-i)) % v_cycle][x] == "^" else 0
            d = 1 if area[(y-i) % v_cycle][x] == "v" else 0
            v_rounds.append(u + d)

        states[point] = {i: h_rounds[i % h_cycle] + v_rounds[i % v_cycle]
                         for i in range(h_cycle * v_cycle)}
    return states


def get_neighborhood(pos):
    x, y = pos
    return {(x, y), (x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)}


area = [line[1:-1] for line in input[1:-1]]
grid = {(x, y): 0 if char == "." else 1 for y, line in enumerate(area)
        for x, char in enumerate(line) if char != "#"}
h_cycle, v_cycle = len(area[0]), len(area)

states = get_value_map()


def travel(start, finish, start_round):
    round = start_round
    always_free = {(0, -1), (h_cycle-1, v_cycle)}

    to_explore = {start}
    while True:
        free = set(p for p in states
                   if states.get(p, {}).get(round % (h_cycle * v_cycle), 9) == 0) | always_free

        nbh = set(nbh_point for point in iter(to_explore)
                  for nbh_point in get_neighborhood(point))
        to_explore = nbh & free

        if finish in to_explore:
            break
        round += 1
    return round


def part1():
    return travel((0, 0), (h_cycle-1, v_cycle-1), 0) + 1


def part2():
    there = travel((0, -1), (h_cycle-1, v_cycle), 0)
    back = travel((h_cycle-1, v_cycle), (0, -1), there + 1)
    and_back_again = travel((0, -1), (h_cycle-1, v_cycle), back + 1)

    return and_back_again


print(part1())
print(part2())
