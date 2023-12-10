def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        diagram = ifile.read().split("\n")
    return distance_to_farthest_point(diagram)


def distance_to_farthest_point(diagram):
    start = next(
        (x, y)
        for x, line in enumerate(diagram)
        for y, char in enumerate(line)
        if char == "S"
    )
    distances = [[float("inf") for _ in line] for line in diagram]
    distances[start[0]][start[1]] = 0
    p1, p2 = find_start_neighbors(diagram, start)
    distances[p1[0]][p1[1]] = 1
    distances[p2[0]][p2[1]] = 1
    queue = [(p2, start), (p1, start)]
    while True:
        p, prev = queue.pop()
        neighbor = find_loop_neighbor(p, prev, diagram)
        if distances[neighbor[0]][neighbor[1]] != float("inf"):
            return distances[neighbor[0]][neighbor[1]]
        distances[neighbor[0]][neighbor[1]] = distances[p[0]][p[1]] + 1
        queue.insert(0, (neighbor, p))


def find_start_neighbors(diagram, start):
    return tuple(
        neighbor
        for (offset_x, offset_y), required_tiles in (
            ((-1, 0), {"F", "|", "7"}),
            ((1, 0), {"L", "|", "J"}),
            ((0, -1), {"F", "-", "L"}),
            ((0, 1), {"7", "-", "J"}),
        )
        if (neighbor := (start[0] + offset_x, start[1] + offset_y))
        and -1 < neighbor[0] < len(diagram)
        and -1 < neighbor[1] < len(diagram[0])
        and diagram[neighbor[0]][neighbor[1]] in required_tiles
    )


def find_loop_neighbor(pos, prev, diagram):
    x, y = pos
    # fmt: off
    match diagram[x][y]:
        case "|": candidates = ((x - 1, y), (x + 1, y))
        case "-": candidates = ((x, y - 1), (x, y + 1))
        case "L": candidates = ((x - 1, y), (x, y + 1))
        case "J": candidates = ((x, y - 1), (x - 1, y))
        case "7": candidates = ((x, y - 1), (x + 1, y))
        case "F": candidates = ((x + 1, y), (x, y + 1))
    # fmt: on
    return candidates[1] if candidates[0] == prev else candidates[0]


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    # print(solution(f"input/{__file__[-16:][:6]}_example1.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
