import collections
import dataclasses
import enum


class Direction(enum.Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def neighbor(self, direction: Direction):
        return Point(self.x + direction.value[0], self.y + direction.value[1])


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        grid = tuple(line.strip("\n") for line in ifile)
    grid_row_len, grid_col_len = len(grid), len(grid[0])
    starting_configurations = []
    starting_configurations += [
        (Point(x, 0), Direction.RIGHT) for x in range(grid_row_len)
    ]
    starting_configurations += [
        (Point(x, grid_col_len - 1), Direction.LEFT) for x in range(grid_row_len)
    ]
    starting_configurations += [
        (Point(0, y), Direction.DOWN) for y in range(grid_col_len)
    ]
    starting_configurations += [
        (Point(grid_row_len - 1, y), Direction.UP) for y in range(grid_col_len)
    ]
    return max(
        len(energized_points(grid, starting_point, inbound_direction))
        for (starting_point, inbound_direction) in starting_configurations
    )


def energized_points(grid, starting_point, inbound_direction):
    grid_row_len, grid_col_len = len(grid), len(grid[0])

    def is_valid_point(point):
        return -1 < point.x < grid_row_len and -1 < point.y < grid_col_len

    result = {starting_point}
    queue = collections.deque([(starting_point, inbound_direction)])
    visited = {(starting_point, inbound_direction)}
    while queue:
        point, inbound_direction = queue.pop()
        for direction in outbound_directions(grid[point.x][point.y], inbound_direction):
            if is_valid_point(neighbor := point.neighbor(direction)):
                result.add(neighbor)
                if (neighbor, direction) not in visited:
                    queue.appendleft((neighbor, direction))
                    visited.add((neighbor, direction))

    return result


def outbound_directions(tile_type, inbound_direction):
    match tile_type, inbound_direction:
        case ".", _:
            result = (inbound_direction,)
        case "/", Direction.UP:
            result = (Direction.RIGHT,)
        case "/", Direction.DOWN:
            result = (Direction.LEFT,)
        case "/", Direction.LEFT:
            result = (Direction.DOWN,)
        case "/", Direction.RIGHT:
            result = (Direction.UP,)
        case "\\", Direction.UP:
            result = (Direction.LEFT,)
        case "\\", Direction.DOWN:
            result = (Direction.RIGHT,)
        case "\\", Direction.LEFT:
            result = (Direction.UP,)
        case "\\", Direction.RIGHT:
            result = (Direction.DOWN,)
        case ("|", Direction.UP) | ("|", Direction.DOWN):
            result = (inbound_direction,)
        case ("|", Direction.LEFT) | ("|", Direction.RIGHT):
            result = (Direction.UP, Direction.DOWN)
        case ("-", Direction.LEFT) | ("-", Direction.RIGHT):
            result = (inbound_direction,)
        case ("-", Direction.UP) | ("-", Direction.DOWN):
            result = (Direction.LEFT, Direction.RIGHT)
    return result


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
