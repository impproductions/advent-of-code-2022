from pathlib import Path


path = Path(__file__).parent / "input.txt"
with path.open() as file:
    input = file.read().splitlines()


class Queue():
    def __init__(self):
        self.list: list[tuple[tuple[int, int], int]] = []

    def add(self, new_element: tuple[tuple[int, int], int]):
        at_index = len(self.list) - 1
        for i, element in enumerate(self.list):
            if new_element[1] <= element[1]:
                at_index = i - 1
                break
        self.list = self.list[:at_index + 1] + \
            [new_element] + self.list[at_index + 1:]

    def pop(self):
        if len(self.list) == 0:
            return None
        return self.list.pop(0)


def to_number(char: str):
    if char == "S":
        return 0
    elif char == "E":
        return 27
    else:
        return ord(char) - 96


def get_accessible(coords: tuple[int], map: dict[tuple[int, int], int]):
    x, y = coords
    accessible = []
    for x1, y1 in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        if x1 in range(0, width) and y1 in range(0, height):
            # to be accessible, elevation has to be at most 1 higher (this includes all the lower elevations)
            if map[(x1, y1)] in range(0, map[coords] + 2):
                accessible.append((x1, y1))

    return accessible


width = len(input[0])
height = len(input)
size = (width, height)
map = {(y, x): to_number(elevation) for x, line in enumerate(input)
       for y, elevation in enumerate(line)}
graph = {(x, y): get_accessible((x, y), map) for x, y in map}

min_elevation = min(map.values())
max_elevation = max(map.values())


def get_minimum_distance(start_value: int, end_value: int):
    distances = []
    for start in [key for key in map if map[key] <= start_value]:
        queue = Queue()
        visited = set()
        current = (start, 0)
        queue.add(current)
        values = {}

        while map[current[0]] != end_value:
            # visit next queued node
            current = queue.pop()

            # if no nodes are queued, this is a dead end
            if current == None:
                break

            # skip visited nodes
            if current[0] in visited:
                continue

            # mark as visited
            visited.add(current[0])

            # queue connected nodes
            for next in graph[current[0]]:
                if not next in visited:
                    queue.add((next, current[1] + 1))
                    values[next] = current[1] + 1

        # store walked distance if the path connects to the end
        if current != None:
            distances.append(current[1])

    return min(distances)


def part1():
    return get_minimum_distance(min_elevation, max_elevation)


def part2():
    return get_minimum_distance(1, max_elevation)


print(part1())
print(part2())
