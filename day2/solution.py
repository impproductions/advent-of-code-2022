from os import path;

file_path = path.relpath("./input.txt")
with open(file_path, "r") as f:
    data = f.read().splitlines()

opponent_options = "ABC"
player_options = "XYZ"

rounds = [[opponent_options.index(game.split(" ")[0]), player_options.index(game.split(" ")[1])] for game in data]

def result(o_move_index, p_move_index):
    return (2 - ((o_move_index - p_move_index + 1) % 3)) * 3

def score(o_move_index, p_move_index):
    return result(o_move_index, p_move_index) + p_move_index + 1

def get_player_move(o_move_index, p_desired_result): # for p2
    return (o_move_index + p_desired_result + 2) % 3

def part1():
    return sum([score(o, p) for o, p in rounds])

def part2():
    return sum([score(o, get_player_move(o, p)) for o, p in rounds])

print(part1())
print(part2())