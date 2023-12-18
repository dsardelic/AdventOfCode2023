"""Uses pretty much the same algorithm as the one on Day 10."""

import dataclasses
import enum


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
    with open(input_rel_uri, encoding="utf-8") as ifile:
        input_data = tuple(
            (Direction.from_char(tokens[0]), int(tokens[1]))
            for line in ifile.read().split("\n")
            if (tokens := line.replace("(", "").replace(")", "").split(" ")[:2])
        )
    return trench_volume(input_data)


def trench_volume(input_data):
    loop, edge_type_per_point = loop_and_edges(input_data)
    enclosed = inner_edge(loop, edge_type_per_point)
    flood(enclosed, loop)
    return len(loop) + len(enclosed)


def loop_and_edges(input_data):
    point = Point(0, 0)
    loop = (point,)
    edge_type_per_point = {}
    previous_direction = input_data[-1][0]
    # assume Point(0, 0) is an edge
    for direction, length in input_data:
        # resolve edge at graph edge beginning
        edge_type_per_point[point] = edge_type(previous_direction, direction)
        for _ in range(length):
            neighbor = point.neighbor(direction)
            loop += (neighbor,)
            point = neighbor
        previous_direction = direction
    # assume clockwise loop, otherwise should be reversed
    return loop[:-1], edge_type_per_point


def inner_edge(loop, edge_type_per_point):
    result = set()
    moving_direction = Direction.RIGHT
    inward_direction = Direction.DOWN
    for point in loop:
        if (enclosed_point := point.neighbor(inward_direction)) not in loop:
            result.add(enclosed_point)
        # pylint: disable=redefined-variable-type
        match edge_type_per_point.get(point), moving_direction:
            case None, _:
                continue
            case "L", Direction.LEFT:
                moving_direction = Direction.UP
                inward_direction = Direction.RIGHT
            case "L", Direction.DOWN:
                moving_direction = Direction.RIGHT
                inward_direction = Direction.DOWN
            case "J", Direction.DOWN:
                moving_direction = Direction.LEFT
                inward_direction = Direction.UP
            case "J", Direction.RIGHT:
                moving_direction = Direction.UP
                inward_direction = Direction.RIGHT
            case "7", Direction.RIGHT:
                moving_direction = Direction.DOWN
                inward_direction = Direction.LEFT
            case "7", Direction.UP:
                moving_direction = Direction.LEFT
                inward_direction = Direction.UP
            case "F", Direction.UP:
                moving_direction = Direction.RIGHT
                inward_direction = Direction.DOWN
            case "F", Direction.LEFT:
                moving_direction = Direction.DOWN
                inward_direction = Direction.LEFT
        # pylint: enable=redefined-variable-type
        if (enclosed_point := point.neighbor(inward_direction)) not in loop:
            result.add(enclosed_point)
    return result


def edge_type(old_direction, new_direction):
    match old_direction, new_direction:
        case (Direction.UP, Direction.RIGHT) | (Direction.LEFT, Direction.DOWN):
            result = "F"
        case (Direction.RIGHT, Direction.DOWN) | (Direction.UP, Direction.LEFT):
            result = "7"
        case (Direction.DOWN, Direction.RIGHT) | (Direction.LEFT, Direction.UP):
            result = "L"
        case (Direction.DOWN, Direction.LEFT) | (Direction.RIGHT, Direction.UP):
            result = "J"
        case _, _:
            raise RuntimeError("Resolve edge:", old_direction, new_direction)
    return result


def flood(enclosed, loop):
    remaining = set(enclosed)
    while remaining:
        more_remaining = {
            neighbor
            for point in remaining
            for direction in (
                Direction.UP,
                Direction.DOWN,
                Direction.LEFT,
                Direction.RIGHT,
            )
            if (neighbor := point.neighbor(direction))
            and neighbor not in loop
            and neighbor not in enclosed
        }
        enclosed |= more_remaining
        remaining = more_remaining


if __name__ == "__main__":
    print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    # print(solution(f"input/{__file__[-16:][:6]}.txt"))
