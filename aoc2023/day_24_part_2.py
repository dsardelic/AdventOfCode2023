import dataclasses

import sympy


@dataclasses.dataclass
class Hailstone:
    x0: int
    y0: int
    z0: int
    dx: int
    dy: int
    dz: int


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        hailstones = tuple(
            Hailstone(
                *(
                    int(token)
                    for token in line.strip("\n").replace(" @ ", ", ").split(", ")
                )
            )
            for line in ifile
        )

    x0, y0, z0, dx, dy, dz, t1, t2, t3 = sympy.symbols(
        ("x0", "y0", "z0", "dx", "dy", "dz", "t1", "t2", "t3")
    )

    # assume top 3 hailstones have different collision times
    solved_unknowns = sympy.solve(
        (
            x0 + dx * t1 - (hailstones[0].x0 + hailstones[0].dx * t1),
            y0 + dy * t1 - (hailstones[0].y0 + hailstones[0].dy * t1),
            z0 + dz * t1 - (hailstones[0].z0 + hailstones[0].dz * t1),
            x0 + dx * t2 - (hailstones[1].x0 + hailstones[1].dx * t2),
            y0 + dy * t2 - (hailstones[1].y0 + hailstones[1].dy * t2),
            z0 + dz * t2 - (hailstones[1].z0 + hailstones[1].dz * t2),
            x0 + dx * t3 - (hailstones[2].x0 + hailstones[2].dx * t3),
            y0 + dy * t3 - (hailstones[2].y0 + hailstones[2].dy * t3),
            z0 + dz * t3 - (hailstones[2].z0 + hailstones[2].dz * t3),
        ),
    )

    return sum(solved_unknowns[0][variable] for variable in (x0, y0, z0))


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
