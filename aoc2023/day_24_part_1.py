import dataclasses
import functools
import itertools


@dataclasses.dataclass
class Hailstone:
    x0: int
    y0: int
    dx: int
    dy: int

    # hailstone's X-Y plane direction is generally calculated as: y(x) = a * x + b
    # edge cases are lines such as x = 3 (for a = ±∞) or y = -2 (for a = 0)

    @functools.cached_property
    def a(self):
        if self.dx:
            return self.dy / self.dx
        if self.dy > 0:
            return float("inf")
        return -float("inf")

    @functools.cached_property
    def b(self):
        x1, y1 = self.x0 + self.dx, self.y0 + self.dy
        numerator = x1 * self.y0 - self.x0 * y1
        if self.dx:
            return numerator / self.dx
        if numerator > 0:
            return float("inf")
        return -float("inf")

    @classmethod
    def parse_from_line(cls, hailstone_data):
        def parse_numbers(string, delimiter):
            return (int(token) for token in string.split(delimiter))

        coordinates_data, deltas_data = hailstone_data.split(" @ ")
        x0, y0, _ = parse_numbers(coordinates_data, ", ")
        dx, dy, _ = parse_numbers(deltas_data, ", ")
        return Hailstone(x0, y0, dx, dy)

    def collision_point(self, other):
        if other.a == self.a:
            result = None
        elif (self.a == float("inf") and other.a == -float("inf")) or (
            self.a == -float("inf") and other.a == float("inf")
        ):
            result = None
        elif not self.a:
            if other.a in {float("inf"), -float("inf")}:
                result = (other.x0, self.y0)
            else:
                result = ((self.y0 - other.b) / other.a, self.y0)
        elif not other.a:
            if self.a in {float("inf"), -float("inf")}:
                result = (self.x0, other.y0)
            else:
                result = ((other.y0 - self.b) / self.a, other.y0)
        elif self.a in {float("inf"), -float("inf")}:
            result = (self.x0, other.a * self.x0 + other.b)
        elif other.a in {float("inf"), -float("inf")}:
            result = (other.x0, self.a * other.x0 + self.b)
        else:
            collision_x = (other.b - self.b) / (self.a - other.a)
            collision_y = self.a * collision_x + self.b
            result = (collision_x, collision_y)
        return result

    def timestamp_at(self, x, y):
        if not self.a:
            return (x - self.x0) / self.dx
        if self.a in {float("inf"), -float("inf")}:
            return (y - self.y0) / self.dy
        return (x - self.x0) / self.dx


def solution(input_rel_uri, min_boundary, max_boundary):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        hailstones = tuple(
            Hailstone.parse_from_line(line.strip("\n")) for line in ifile
        )
    return sum(
        is_within_area(collision_point, min_boundary, max_boundary)
        for hailstone1, hailstone2 in itertools.combinations(hailstones, 2)
        if (collision_point := hailstone1.collision_point(hailstone2))
        if hailstone1.timestamp_at(*collision_point) > 0
        and hailstone2.timestamp_at(*collision_point) > 0
    )


def is_within_area(collision_point, min_boundary, max_boundary):
    return all(
        min_boundary <= coordinate <= max_boundary for coordinate in collision_point
    )


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt", 7, 27))
    print(solution(f"input/{__file__[-16:][:6]}.txt", 200000000000000, 400000000000000))
