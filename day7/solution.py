from pathlib import Path


class Node():
    def __init__(self, value, parent, children, size):
        self.value = value
        self.parent = parent
        self.children = children
        self.size = size


path = Path(__file__).parent / "example.txt"
with path.open() as file:
    input = file.read()


def parse_command(command):
    lines = command.strip().split("\n")
    input = lines[0].split(" ")
    output = lines[1:] if len(lines) > 1 else []

    return (input, output)


commands = [parse_command(command) for command in input.split("$ ")[2:]]


def create_tree():
    root = Node("/", None, [], 0)
    current_node = root
    nodes = [root]
    for input, output in commands:
        command = input[0]
        if command == "ls":
            for output_line in output:
                split_output = output_line.split(" ")
                if split_output[0] != "dir":
                    current_node.size += int(split_output[0])

            # increment all sizes working back up to the root node
            back_propagation_head = current_node
            while back_propagation_head.parent != None:
                back_propagation_head.parent.size += current_node.size
                back_propagation_head = back_propagation_head.parent

        elif command == "cd":
            argument = input[1]
            if argument == "..":
                current_node = current_node.parent
            else:
                current_node.children.append(
                    Node(argument, current_node, [], 0))
                current_node = current_node.children[-1]
                nodes.append(current_node)

    return nodes


nodes = create_tree()


def part1():
    return sum([n.size for n in nodes if n.size < 100000])


def part2():
    missing_space = 30000000 - (70000000 - nodes[0].size)
    first_bigger_folder = nodes[0].size

    for node in nodes:
        if node.size >= missing_space and node.size <= first_bigger_folder:
            first_bigger_folder = node.size

    return first_bigger_folder


print(part1())
print(part2())
