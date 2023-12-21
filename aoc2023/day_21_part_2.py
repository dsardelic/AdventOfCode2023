import dataclasses
import enum

STEP_COUNT = 26501365

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


def count_reachable_plots(grid):  # pylint: disable=too-many-locals
    # Due to the very specific nature of input data:
    #    1) no rocks in neither row nor column of the start position,
    #    2) grid border consists only of plots,
    #    3) initial grid size of 131 x 131,
    #    4) 26501365 ≡ 65 (mod 131),
    # the number of reachable plots after each (65 + n * 131) steps
    # with n being the number of expansion grids in each direction
    # converges to a quadratic function f(n) = an^2 + bn + c.
    # The idea is to find 3 of its points, namely those corresponding to:
    #      i. f(0) = 65 + 131 * 0,
    #     ii. f(1) = 65 + 131 * 1,
    #    iii. f(2) = 65 + 131 * 2,
    # steps, and then calculate the quadratic equation coefficients.
    # The solution is then equal to f(26501365 // 131).

    f_ns, f_ys = [], []

    grid = tuple(row * 5 for row in grid) * 5
    start = Point(len(grid) // 2, len(grid) // 2)
    start_neighbors = tuple(
        neighbor
        for offset in ((-1, 0), (1, 0), (0, -1), (0, 1))
        if (
            (neighbor := start.offset_neighbor(offset))
            and is_valid_point(neighbor, grid)
        )
    )
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
        parity_to_last_reached[step % 2] = new_reached

        if step in {65, 65 + 131, 65 + 131 * 2}:
            if step == 65 + 131 * 0:
                f_ns.append(0)
                f_ys.append(len(parity_to_reachables[step % 2]))
            elif step == 65 + 131 * 1:
                f_ns.append(1)
                f_ys.append(len(parity_to_reachables[step % 2]))
            elif step == 65 + 131 * 2:
                f_ns.append(2)
                f_ys.append(len(parity_to_reachables[step % 2]))
                break

    # Using Lagrange's interpolating polynomial formula
    a, b, c = coefficients(f_ns, f_ys)
    n = 26501365 // 131
    return int(a * n**2 + b * n + c)


def coefficients(f_ns, f_ys):
    a, b, c = 0, 0, 0
    for y, x, x1, x2 in (
        (f_ys[0], f_ns[0], f_ns[1], f_ns[2]),
        (f_ys[1], f_ns[1], f_ns[0], f_ns[2]),
        (f_ys[2], f_ns[2], f_ns[0], f_ns[1]),
    ):
        k = y / (x - x1) / (x - x2)
        a += k
        b += -k * (x1 + x2)
        c += k * x1 * x2
    return a, b, c


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
