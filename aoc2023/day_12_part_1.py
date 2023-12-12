import dataclasses
import re


@dataclasses.dataclass
class Node:
    def __init__(self, statuses, groups, value=0):
        self.statuses = statuses
        self.groups = groups
        self.children = []
        self._value = value

    @property
    def value(self):
        return (
            self._value if self._value else sum(child.value for child in self.children)
        )

    @value.setter
    def value(self, value):
        self._value = value


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return sum(count_possible_arrangements(line) for line in ifile)


def count_possible_arrangements(line):
    statuses, groups = line.split(" ")
    groups = tuple(int(group) for group in groups.split(","))
    statuses, groups = reduce_starting_from_beginning(statuses, groups)
    statuses, groups = reduce_starting_from_end(statuses, groups)
    if not groups:
        return 1
    root = Node(statuses, groups)
    expand_node(root)
    return root.value


def reduce_starting_from_beginning(statuses, groups):
    while statuses:
        statuses = statuses.lstrip(".")
        if statuses[0] == "#":
            statuses = statuses[groups[0] + 1 :]
            groups = groups[1:]
        else:
            break
    return statuses, groups


def reduce_starting_from_end(statuses, groups):
    while statuses:
        statuses = statuses.rstrip(".")
        if statuses[-1] == "#":
            if len(statuses) < groups[-1] + 1:
                return "", groups[:-1]
            statuses = statuses[: len(statuses) - groups[-1] - 1]
            groups = groups[:-1]
        else:
            break
    return statuses, groups


def expand_node(node):
    if not (node.statuses and node.groups):
        return
    node.statuses = "." + node.statuses + "."
    regex = r"(?=[\?\.][#\?]{" + str(node.groups[0]) + r"}[\?\.])"
    matches = re.finditer(regex, node.statuses)
    if "#" in node.statuses:
        if len(node.groups) == 1:
            node.value = sum(
                m.span()[0] < node.statuses.index("#")
                and m.span()[1] + node.groups[0] >= node.statuses.index("#")
                and "#" not in node.statuses[m.span()[1] + 1 + node.groups[0] + 1 :]
                for m in matches
            )
        else:
            for m in matches:
                if m.span()[0] < node.statuses.index("#"):
                    child = Node(
                        node.statuses[m.span()[1] + 1 + node.groups[0] + 1 :].strip(
                            "."
                        ),
                        node.groups[1:],
                    )
                    node.children.append(child)
                    expand_node(child)
    elif len(node.groups) == 1:
        node.value = len(tuple(matches))
    else:
        for m in matches:
            child = Node(
                node.statuses[m.span()[1] + 1 + node.groups[0] + 1 :].strip("."),
                node.groups[1:],
            )
            node.children.append(child)
            expand_node(child)


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
