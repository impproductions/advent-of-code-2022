from os import path

file_path = path.join(path.dirname(path.abspath(__file__)) +"/input.txt")
with open(file_path, "r") as f:
    data = f.read().splitlines()

opponent_options = "ABC"
player_options = "XYZ"

# convert all moves to the respective indices
rounds = [[opponent_options.index(game.split(" ")[0]), player_options.index(game.split(" ")[1])] for game in data]

def result(o, p):
    return (2 - ((o - p + 1) % 3)) * 3

def score(o, p):
    return result(o, p) + p + 1

def get_player_move(o, p_result): # for p2
    return (o + p_result + 2) % 3

def part1():
    return sum([score(o, p) for o, p in rounds])

def part2():
    return sum([score(o, get_player_move(o, p)) for o, p in rounds])

print(part1())
print(part2())