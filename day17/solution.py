from pathlib import Path


path = Path(__file__).parent / "input.txt"
with path.open() as file:
    input = file.read()

pieces_path = Path(__file__).parent / "pieces.txt"
with pieces_path.open() as file:
    pieces_file = file.read()

pieces = [[[1 if c == "#" else 0 for c in line]
           for line in piece.split("\n")][::-1] for piece in pieces_file.split("\n\n")]
wind = input
space = []
LEFT = "<"
RIGHT = ">"


def overlaps(piece, section):
    if len(piece) > len(section):
        return True
    if len(piece[0]) > len(section[0]):
        return True
    return any(piece[y][x] + section[y][x] > 1 for y in range(len(piece)) for x in range(len(piece[0])))


def extend_space(amt):
    space.extend([[0] * 7] * amt)


def spawn_piece(piece):
    return piece, (len(space)-len(piece), 2)


def place_piece(piece, coords):
    row, col = coords
    for y in range(len(piece)):
        space[row+y] = space[row+y][:col]\
            + [piece[y][x] + space[row+y][col+x]
                for x in range(len(piece[0]))] + space[row+y][col + len(piece[0]):]


def trim_top():
    topmost = get_height()
    if len(space) > topmost:
        for _ in range(len(space)-1,  get_height() - 1, -1):
            space.pop()


def get_height():
    for i in range(len(space)-1, -1, -1):
        if any(p > 0 for p in space[i]):
            return i + 1
    return 0


def nudge_piece_h(piece, from_coords, direction):
    from_row, from_col = from_coords
    increment = (1 if direction == RIGHT else -1)
    v_window = space[from_row:from_row+len(piece)]
    window = [col[from_col+increment:from_col +
                  increment + len(piece[0])] for col in v_window]

    if overlaps(piece, window):
        return piece, from_coords

    to_coords = (from_row, from_col + increment)

    return piece, to_coords


def nudge_piece_v(piece, from_coords):
    from_row, from_col = from_coords
    v_window = space[from_row-1:from_row-1+len(piece)]
    window = [col[from_col:from_col + len(piece[0])] for col in v_window]

    if overlaps(piece, window):
        return piece, from_coords

    to_coords = (from_row-1, from_col)

    return piece, to_coords


def drop_piece(piece_index, h_counter):
    piece = pieces[piece_index]
    extend_space(len(piece) + 3)
    spawned = spawn_piece(piece)
    prev_coords = spawned[1]
    movement = 0  # 0 h 1 v

    while True:
        if movement == 0:
            spawned = nudge_piece_h(*spawned, wind[h_counter % len(wind)])
            movement = 1
            h_counter += 1
        elif movement == 1:
            spawned = nudge_piece_v(*spawned)
            movement = 0
            if spawned[1] == prev_coords:
                # when it stops vertically, it is at rest
                break
        prev_coords = spawned[1]

    place_piece(*spawned)
    trim_top()

    return h_counter


def part1():
    qty = 2022
    h_counter = 0
    for i in range(qty):
        h_counter = drop_piece(i % 5, h_counter)

    return get_height()


def part2():
    # some pattern is bound to repeat from some point onward,
    # since it depends on two cyclic values (the piece and the wind direction)
    # so first drop pieces until some pattern start repeating,
    # then the total is equal to the sum of 3 parts:
    # the height up until the first repeated pattern
    # + the height of the repeated pattern * the amount of repetitions
    # + the height of the last truncated repeat

    pieces_quantity = 1000000000000
    # how much height is added by each pattern
    pattern_heights = {}

    # all repeated patterns
    repeated_patterns = []

    first_repeated = None
    repeated_height, unique_height = None, None
    # the amount of pieces in the repeated part and in the unique (starting) part
    repeated_length, unique_length = None, None

    # this height is arbitrary, I couldn't figure out how to calculate a
    # mathematically "safe" value
    pattern_height = sum([len(piece) for piece in pieces]) * 5

    h_counter = 0

    for i in range(pieces_quantity):
        pattern = ()
        current_height = get_height()

        if current_height >= pattern_height:
            pattern = tuple([tuple(space[-i]) for i in range(1,
                           pattern_height+1, 1) if len(space) >= pattern_height-1])

        h_counter = drop_piece(i % 5, h_counter)

        if pattern != ():
            if pattern_heights.get(pattern) != None:
                if first_repeated == None:
                    first_repeated = pattern
                    unique_length = i-1
                    unique_height = current_height
                elif first_repeated == pattern and repeated_length == None:
                    repeated_length = i - (unique_length + 1)
                    repeated_height = current_height - unique_height

        if first_repeated != None and repeated_length == None:
            repeated_patterns.append(pattern)

        difference = get_height() - current_height
        pattern_heights[pattern] = difference

        if repeated_length != None:
            # we have all the informations we need from the repeated part, so exit the loop
            break

    repetitions = (pieces_quantity - unique_length) // repeated_length
    rest_length = (pieces_quantity - unique_length) % repeated_length - 1
    rest_height = sum((pattern_heights[c] for c in repeated_patterns[:rest_length]))

    # calculate the height for each part
    total = unique_height + repetitions * repeated_height + rest_height

    return total


print(part1())
space = []
print(part2())
