import re


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        instructions, node_to_neighbors_lines = ifile.read().split("\n\n")

    instructions = tuple(
        int(char) for char in instructions.replace("L", "0").replace("R", "1")
    )

    node_to_neighbors = {
        match_.group(1): (match_.group(2), match_.group(3))
        for line in node_to_neighbors_lines.split("\n")
        if (match_ := re.match(r"(\w{3}) = \((\w{3}), (\w{3})\)", line))
    }

    step_count = 0
    node = "AAA"
    while (
        node := node_to_neighbors[node][instructions[step_count % len(instructions)]]
    ) != "ZZZ":
        step_count += 1
    return step_count + 1


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    # print(solution(f"input/{__file__[-16:][:6]}_example1.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
