import dataclasses
import enum

STEP_COUNT = 64

Parity = enum.Enum("Parity", ("ODD", "EVEN"))


@dataclasses.dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def offset_neighbor(self, offset):
        return Point(self.x + offset[0], self.y + offset[1])


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        grid = tuple(line.strip("\n") for line in ifile)
    return count_reachable_plots(grid)


def count_reachable_plots(grid):
    if not STEP_COUNT:
        return 0

    start = next(
        Point(x, y)
        for x, row in enumerate(grid)
        for y, value in enumerate(row)
        if value == "S"
    )
    start_neighbors = tuple(
        neighbor
        for offset in ((-1, 0), (1, 0), (0, -1), (0, 1))
        if (
            (neighbor := start.offset_neighbor(offset))
            and is_valid_point(neighbor, grid)
        )
    )
    if STEP_COUNT == 1:
        return len(start_neighbors)

    reachable_offsets = (
        ((-2, 0), ((-1, 0),)),
        ((-1, -1), ((0, -1), (-1, 0))),
        ((-1, 1), ((0, 1), (-1, 0))),
        ((0, -2), ((0, -1),)),
        ((0, 2), ((0, 1),)),
        ((1, -1), ((0, -1), (1, 0))),
        ((1, 1), ((0, 1), (1, 0))),
        ((2, 0), ((1, 0),)),
    )
    parity_to_reachables = {0: {start}, 1: set(start_neighbors)}
    parity_to_last_reached = {0: {start}, 1: set(start_neighbors)}
    for step in range(2, STEP_COUNT + 1):
        new_reached = set()
        for reached in parity_to_last_reached[step % 2]:
            for candidate_offset, via_offsets in reachable_offsets:
                candidate = reached.offset_neighbor(candidate_offset)
                if not is_valid_point(candidate, grid):
                    continue
                # check if path(s) to the candidate are viable
                if any(
                    is_valid_point(via_point, grid)
                    for via in via_offsets
                    if (via_point := reached.offset_neighbor(via))
                ):
                    parity_to_reachables[step % 2].add(candidate)
                    new_reached.add(candidate)
        if not new_reached:
            break
        parity_to_last_reached[step % 2] = new_reached
    return len(parity_to_reachables[step % 2])


def value_at(point: Point, grid):
    return grid[point.x][point.y]


def is_valid_point(point, grid):
    return (
        -1 < point.x < len(grid)
        and -1 < point.y < len(grid[0])
        and value_at(point, grid) != "#"
    )


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
