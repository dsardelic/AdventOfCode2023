import dataclasses
import enum
import itertools


class Direction(enum.Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    @classmethod
    def from_char(cls, char):
        if char == "U":
            return Direction.UP
        if char == "D":
            return Direction.DOWN
        if char == "L":
            return Direction.LEFT
        if char == "R":
            return Direction.RIGHT
        raise RuntimeError("Invalid direction char:", char)


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def neighbor(self, direction, distance=1):
        return Point(
            self.x + distance * direction.value[0],
            self.y + distance * direction.value[1],
        )


def solution(input_rel_uri):
    translations = str.maketrans("0123", "RDLU")
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return trench_volume(
            (
                Direction.from_char(hex_code[6].translate(translations)),
                int(hex_code[1:6], 16),
            )
            for line in ifile
            if (hex_code := line.replace("(", "").replace(")", "").split(" ")[2])
        )


def trench_volume(input_data):
    """Using Trapezoid formula and Pick's theorem."""
    loop = resolve_loop(input_data)
    area = 0
    boundary_lattice_points_count = 0
    for p1, p2 in itertools.pairwise(loop):
        area += (p1.y + p2.y) * (p1.x - p2.x)
        boundary_lattice_points_count += abs(p2.x - p1.x) + abs(p2.y - p1.y)
    area = abs(area // 2)
    interior_lattice_points_count = area - boundary_lattice_points_count // 2 + 1
    return interior_lattice_points_count + boundary_lattice_points_count


def resolve_loop(input_data):
    point = Point(0, 0)
    loop = (point,)
    for direction, distance in input_data:
        neighbor = point.neighbor(direction, distance)
        loop += (neighbor,)
        point = neighbor
    return loop


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
