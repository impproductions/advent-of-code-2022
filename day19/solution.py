from pathlib import Path
from math import prod


path = Path(__file__).parent / "example.txt"
with path.open() as file:
    input = file.read().splitlines()


def parse_input(input):
    reference = ["ore", "clay", "obsidian", "geode"]

    blueprints = []
    for line in input:
        blueprint_dict = {robot[0]: {cost.split(" ")[1].replace(".", ""): int(cost.split(" ")[0])
                                     for cost in robot[1].split(" and ")}
                          for robot in [robot_line.split(" robot costs ")
                                        for robot_line in line.split(" Each ")[1:]]}
        blueprint = [[blueprint_dict[robot].get(reference[i], 0)
                      for i in range(4)] for robot in blueprint_dict]
        blueprints.append(blueprint)

    return blueprints


def score_state(state, elapsed_time, time_limit):
    resources, increments = state
    return [resources[i] + increments[i] * (time_limit - elapsed_time) for i in range(4)]


def get_new_states(blueprint, state):
    resources, increments = state
    new_states = []

    # add build states
    build_options = [i for i in range(4)
                     if all(resources[j] >= blueprint[i][j] for j in range(4))]

    for option in build_options:
        new_resources = [available - blueprint[option][i] + increments[i]
                         for i, available in enumerate(resources)]
        new_increments = [increment + 1 if i == option else increment
                          for i, increment in enumerate(increments)]
        new_states.append((new_resources, new_increments))

    # add wait state
    new_resources = [available + increments[i]
                     for i, available in enumerate(resources)]
    new_states.append((new_resources, increments))

    return new_states


def get_max_geodes(blueprint, time_limit, cutoff_amount = 100):
    states = [((0, 0, 0, 0), (1, 0, 0, 0))]
    for timer in range(time_limit):
        loop_states = [new_state for state in states
                       for new_state in get_new_states(blueprint, state)]

        # only keep the states with the highest score
        loop_states.sort(key=lambda s: score_state(s, timer, time_limit)[::-1])
        cutoff = min(cutoff_amount, len(loop_states))
        states = loop_states[-cutoff:]

    return max([resources[3] for resources, _ in states])


blueprints = parse_input(input)


def part1():
    quality_levels = [(i+1) * get_max_geodes(bp, 24)
                      for i, bp in enumerate(blueprints)]
    return sum(quality_levels)


def part2():
    geodes = [get_max_geodes(bp, 32) for bp in blueprints[:3]]
    return prod(geodes)


print(part1())
print(part2())
