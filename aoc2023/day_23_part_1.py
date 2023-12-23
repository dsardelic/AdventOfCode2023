import collections
import dataclasses


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def offset_neighbor(self, offset):
        return Point(self.x + offset[0], self.y + offset[1])


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        grid = tuple(line.strip("\n") for line in ifile)
    source = next(
        Point(0, y) for y in range(len(grid[0])) if value_at(grid, Point(0, y)) == "."
    )
    destination = next(
        Point(len(grid) - 1, y)
        for y in range(len(grid[0]))
        if value_at(grid, Point(len(grid) - 1, y)) == "."
    )
    return longest_path_length(grid, source, destination)


def longest_path_length(grid, source, destination):
    distance_grid = [[-1] * len(grid[0]) for _ in range(len(grid))]
    distance_grid[source.x][source.y] = 0
    queue = collections.deque([(source, {source}, 0)])
    while queue:
        point, visited, curr_distance = queue.pop()
        match value_at(grid, point):
            case "^":
                neighbors = (point.offset_neighbor((-1, 0)),)
            case ">":
                neighbors = (point.offset_neighbor((0, 1)),)
            case "v":
                neighbors = (point.offset_neighbor((1, 0)),)
            case "<":
                neighbors = (point.offset_neighbor((0, -1)),)
            case ".":
                neighbors = (
                    point.offset_neighbor(offset)
                    for offset in ((-1, 0), (1, 0), (0, -1), (0, 1))
                )
        valid_neighbors = {
            neighbor for neighbor in neighbors if is_valid_point(neighbor, grid)
        }
        for neighbor in valid_neighbors.difference(visited):
            if curr_distance + 1 >= value_at(distance_grid, neighbor):
                distance_grid[neighbor.x][neighbor.y] = curr_distance + 1
                queue.appendleft((neighbor, visited | {neighbor}, curr_distance + 1))
    return value_at(distance_grid, destination)


def value_at(grid, point):
    return grid[point.x][point.y]


def is_valid_point(point, grid):
    return (
        -1 < point.x < len(grid)
        and -1 < point.y < len(grid[0])
        and value_at(grid, point) != "#"
    )


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example1.txt"))
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
