def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        diagram = [list(line) for line in ifile.read().split("\n")]
    return count_enclosed(diagram)


def count_enclosed(diagram):
    enclosed = set()
    loop = resolve_loop(diagram)
    direction = "N"
    offset = (0, 1)  # offset towards the inside of the loop
    for x, y in loop:
        if (enclosed_or_part_of_loop := (x + offset[0], y + offset[1])) not in loop:
            enclosed.add(enclosed_or_part_of_loop)
        # fmt: off
        match diagram[x][y], direction:
            case "L", "W": direction, offset = "N", (0, 1)
            case "L", "S": direction, offset = "E", (1, 0)
            case "J", "S": direction, offset = "W", (-1, 0)
            case "J", "E": direction, offset = "N", (0, 1)
            case "7", "E": direction, offset = "S", (0, -1)
            case "7", "N": direction, offset = "W", (-1, 0)
            case "F", "N": direction, offset = "E", (1, 0)
            case "F", "W": direction, offset = "S", (0, -1)
            case ("-", _) | ("|", _): continue
        # fmt: on
        if (enclosed_or_part_of_loop := (x + offset[0], y + offset[1])) not in loop:
            enclosed.add(enclosed_or_part_of_loop)
    flood(enclosed, loop)
    return len(enclosed)


def flood(enclosed, loop):
    remaining = set(enclosed)
    while remaining:
        more_remaining = {
            neighbor
            for x, y in remaining
            for offset_x, offset_y in ((-1, 0), (1, 0), (0, -1), (0, 1))
            if (neighbor := (x + offset_x, y + offset_y))
            and neighbor not in loop
            and neighbor not in enclosed
        }
        enclosed |= more_remaining
        remaining = more_remaining


def resolve_loop(diagram):
    start = next(
        (x, y)
        for x, line in enumerate(diagram)
        for y, tile in enumerate(line)
        if tile == "S"
    )

    # Resolve loop beginning at start
    loop = (start,)
    neighbor = find_start_neighbors(start, diagram)[0]  # any neighbor will do
    while neighbor not in loop:
        loop += (neighbor,)
        neighbor = find_loop_neighbor(neighbor, loop, diagram)

    # Let loop origin be the position closest to (0, 0).
    # The tile on that position must be F.
    # The "current" direction on that position is therefore towards north.
    loop_origin = min((pos for pos in loop if diagram[pos[0]][pos[1]] in "FS"), key=sum)

    # Replace S with the original tile
    if diagram[loop_origin[0]][loop_origin[0]] == "S":
        diagram[loop_origin[0]][loop_origin[0]] = "F"
    else:
        restore_start_tile(start, diagram, loop)

    # Let's choose to observe the loop clockwise.
    # The loop origin's neighbor is therefore immediately towards east.
    # If that's not the case, reverse the loop, but still beginning at start.
    loop_origin_neighbor_index = (loop.index(loop_origin) + 1) % len(loop)
    if loop[loop_origin_neighbor_index] != (loop_origin[0], loop_origin[1] + 1):
        loop = (start,) + loop[:0:-1]

    # Rearrange loop to start from its origin.
    loop_origin_index = loop.index(loop_origin)
    loop = loop[loop_origin_index:] + loop[:loop_origin_index]

    return loop


def find_start_neighbors(start, diagram):
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


def find_loop_neighbor(pos, loop, diagram):
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
    return candidates[1] if candidates[0] in loop else candidates[0]


def restore_start_tile(start, diagram, loop):
    pos_before_start = loop[loop.index(start) - 1]
    # fmt: off
    match start[0] - pos_before_start[0], start[1] - pos_before_start[1]:
        case -1, 0: incoming_direction = "N"
        case 1, 0: incoming_direction = "S"
        case 0, -1: incoming_direction = "W"
        case 0, 1: incoming_direction = "E"

    pos_after_start = loop[loop.index(start) + 1]
    match pos_after_start[0] - start[0], pos_after_start[1] - start[1]:
        case -1, 0: outgoing_direction = "N"
        case 1, 0: outgoing_direction = "S"
        case 0, -1: outgoing_direction = "W"
        case 0, 1: outgoing_direction = "E"

    match incoming_direction, outgoing_direction:
        case "N", "N": diagram[start[0]][start[1]] = "|"
        case "N", "E": diagram[start[0]][start[1]] = "F"
        case "N", "W": diagram[start[0]][start[1]] = "7"
        case "E", "N": diagram[start[0]][start[1]] = "J"
        case "E", "E": diagram[start[0]][start[1]] = "-"
        case "E", "S": diagram[start[0]][start[1]] = "7"
        case "W", "N": diagram[start[0]][start[1]] = "L"
        case "W", "W": diagram[start[0]][start[1]] = "-"
        case "W", "S": diagram[start[0]][start[1]] = "F"
        case "S", "E": diagram[start[0]][start[1]] = "L"
        case "S", "W": diagram[start[0]][start[1]] = "J"
        case "S", "S": diagram[start[0]][start[1]] = "|"
    # fmt: on


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example2.txt"))
    # print(solution(f"input/{__file__[-16:][:6]}_example3.txt"))
    # print(solution(f"input/{__file__[-16:][:6]}_example4.txt"))
    # print(solution(f"input/{__file__[-16:][:6]}_example5.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
