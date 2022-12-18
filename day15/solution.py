from pathlib import Path


path = Path(__file__).parent / "input.txt"
with path.open() as file:
    input = file.read().splitlines()


sensors = {}
distances = {}
beacons = set()
beacons_per_line: dict[int, int] = {}
bounds = (0, 4000001)


for line in input:
    s_pos = tuple([int(coord[2:]) for coord in line.split(": ")[0]
                   .split(" at ")[1].split(", ")])
    b_pos = tuple([int(coord[2:]) for coord in line.split(": ")[1]
                   .split(" at ")[1].split(", ")])
    sensors[s_pos] = b_pos
    if not b_pos in beacons:
        beacons_per_line[b_pos[1]] = beacons_per_line.get(b_pos[1], 0) + 1
        beacons.add(b_pos)
    distances[s_pos] = abs(b_pos[0] - s_pos[0]) + abs(b_pos[1] - s_pos[1])


def get_extremes(sensor, line_y):
    sensor_x, sensor_y = sensor
    y_dist = abs(line_y - sensor_y)
    x_dist = distances[sensor] - y_dist
    return (sensor_x - x_dist, sensor_x + x_dist)


def get_extremes_in_range(line_y):
    extremes = []
    for sensor in distances:
        sensor_x, sensor_y = sensor
        dist = distances[sensor]
        if abs(line_y - sensor_y) <= dist:
            extremes.append(get_extremes(sensor, line_y))
    return extremes


def get_union(ranges):
    ranges = sorted(ranges[:])
    start, end = ranges[0]
    union_ranges = [ranges[0]]

    for i, (left, right) in enumerate(ranges):
        if i > 0:
            if left <= end + 1:
                if right <= end:
                    continue
                elif right > end:
                    end = right
                    union_ranges[-1] = (start, right)
            elif left > end + 1:
                start = left
                end = right
                union_ranges.append((start, end))

    return union_ranges


def check_line(line_y):
    in_range_extremes = get_extremes_in_range(line_y)
    union_ranges = get_union(list(in_range_extremes))
    filled_positions = sum([r - l + 1 for l, r in union_ranges])

    amt = filled_positions - beacons_per_line.get(line_y, 0)
    x = union_ranges[0][1] + 1

    return amt, x


def part1():
    return check_line(2000000)[0]


def part2():
    for i in range(0, 4000001):
        amt, x = check_line(i)
        if x < 4000001:
            print(x)
            return 4000000 * x + i


print(part1())
print(part2())
