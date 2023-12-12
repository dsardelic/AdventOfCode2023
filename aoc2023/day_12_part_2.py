import functools
import re


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return sum(count_possible_arrangements(line) for line in ifile)


def count_possible_arrangements(line):
    statuses, groups = line.split(" ")
    groups = tuple(int(group) for group in groups.split(","))

    statuses = "?".join([statuses] * 5)
    groups = groups * 5

    statuses, groups = reduce_starting_from_beginning(statuses, groups)
    statuses, groups = reduce_starting_from_end(statuses, groups)
    if not groups:
        return 1
    return expand_node(statuses, groups)


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


@functools.cache
def expand_node(statuses, groups):
    if not (statuses and groups):
        return 0
    statuses = "." + statuses + "."
    regex = r"(?=[\?\.][#\?]{" + str(groups[0]) + r"}[\?\.])"
    matches = re.finditer(regex, statuses)
    if "#" in statuses:
        if len(groups) == 1:
            # enclose the first available '#'
            return sum(
                m.span()[0] < statuses.index("#")
                and m.span()[1] + 1 + groups[0] > statuses.index("#")
                and "#" not in statuses[m.span()[1] + 1 + groups[0] + 1 :]
                for m in matches
            )
        return sum(
            expand_node(
                statuses[m.span()[1] + 1 + groups[0] + 1 :].strip("."), groups[1:]
            )
            for m in matches
            if m.span()[0] < statuses.index("#")
        )
    if len(groups) == 1:
        return len(tuple(matches))
    return sum(
        expand_node(statuses[m.span()[1] + 1 + groups[0] + 1 :].strip("."), groups[1:])
        for m in matches
    )


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
