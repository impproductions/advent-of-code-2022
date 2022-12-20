from pathlib import Path
from pprint import pprint
from functools import cache

# class Queue():
#     def __init__(self):
#         self.list: list[tuple[str, int]] = []

#     def add(self, new_element: tuple[str, int]):
#         at_index = len(self.list) - 1
#         for i, element in enumerate(self.list):
#             if new_element[1] <= element[1]:
#                 at_index = i - 1
#                 break
#         self.list = self.list[:at_index + 1] + \
#             [new_element] + self.list[at_index + 1:]

#     def pop(self):
#         if len(self.list) == 0:
#             return None
#         return self.list.pop(0)

# def get_minimum_distances(start_value, graph):
#     distances = set()
#     queue = Queue()
#     visited = set()
#     current = (start_value, 0)
#     queue.add(current)

#     values = {}

#     while True:
#         # visit next queued node
#         current = queue.pop()

#         # if no nodes are queued, this is a dead end
#         if current == None:
#             break


#         # skip visited nodes
#         if current[0] in visited:
#             continue

#         # mark as visited
#         visited.add(current[0])

#         # queue connected nodes
#         for next in graph[current[0]]:
#             if not next in visited:
#                 queue.add((next, current[1] + 1))
#                 values[next] = current[1] + 1

#         distances.add(current)

#     return distances

path = Path(__file__).parent / "example.txt"
with path.open() as file:
    input = file.read().splitlines()

flows = {line.split("; ")[0].split(" has ")[
    0][-2:]: int(line.split("; ")[0].split("=")[1]) for line in input}
connections = {line.split("; ")[0].split(" has ")[0][-2:]: line.split("; ")[
    1].replace("valves", "valve").split("valve ")[1].split(", ") for line in input}
opened = frozenset()
to_open = {node for node in flows if flows[node] > 0}

# distances = { (node1, node2): dist for node1 in flows for node2, dist in get_minimum_distances(node1, connections) if (node1 == "AA" or node2 == "AA") or (flows[node1] > 0 and flows[node2] > 0) and node1 != node2}
# relevant_connections = { node: frozenset([c[0] for c in get_minimum_distances(node, connections) if c[0] != node and (flows[c[0]] > 0 or c[0] == "AA") ]) for node in flows if flows[node] > 0 or node == "AA"}


@cache
def visit(node: str, opened: frozenset, time_remaining: int, elephant: bool):
    score = 0
    if time_remaining <= 0:
        return visit("AA", opened, 26, False) if elephant else score

    # decide whether to open
    if not node in opened and flows[node] > 0:
        score = max(score, flows[node] * (time_remaining - 1) +
                    visit(node, opened | {node}, time_remaining - 1, elephant))

    # visit other nodes
    for next_node in connections[node]:
        if not next_node in opened:
            score = max(score, visit(next_node, opened,
                        time_remaining - 1, elephant))

    return score


def part1():
    return visit("AA", opened, 30, False)


def part2():
    return visit("AA", opened, 26, True)


print(part1())
print(part2())
