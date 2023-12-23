import dataclasses


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def offset_neighbor(self, offset):
        return Point(self.x + offset[0], self.y + offset[1])


@dataclasses.dataclass
class Node:
    point: Point
    neighbors: dict[tuple[int, int], tuple[Point, int]] = dataclasses.field(
        default_factory=dict
    )  # map outgoing offset (i.e. direction from self) to neighbor and distance


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
    point_to_node = {
        point: Node(point)
        for x, row in enumerate(grid)
        for y, value in enumerate(row)
        if (point := Point(x, y))
        and is_valid_point(point, grid)
        and sum(
            is_valid_point(neighbor, grid)
            for offset in ((-1, 0), (1, 0), (0, -1), (0, 1))
            if (neighbor := point.offset_neighbor(offset))
        )
        > 2
    }
    point_to_node[source] = Node(source)
    point_to_node[destination] = Node(destination)
    create_node_edges(
        [(source, (1, 0), source, source.offset_neighbor((1, 0)), 1, set())],
        grid,
        point_to_node,
    )
    return max_distance(source, destination, set(), point_to_node)


def value_at(grid, point):
    return grid[point.x][point.y]


def is_valid_point(point, grid):
    return (
        -1 < point.x < len(grid)
        and -1 < point.y < len(grid[0])
        and value_at(grid, point) != "#"
    )


def create_node_edges(stack, grid, point_to_node):
    while stack:
        (
            source_point,
            source_outgoing_offset,
            previous_point,
            current_point,
            current_distance,
            visited,
        ) = stack.pop()
        if current_point in visited:
            continue
        if current_point in point_to_node:
            node = point_to_node[current_point]
            node_outgoing_offset = (
                previous_point.x - current_point.x,
                previous_point.y - current_point.y,
            )
            node.neighbors[node_outgoing_offset] = (source_point, current_distance)
            point_to_node[source_point].neighbors[source_outgoing_offset] = (
                current_point,
                current_distance,
            )
            for offset in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if offset not in node.neighbors and is_valid_point(
                    (neighbor_point := current_point.offset_neighbor(offset)), grid
                ):
                    stack.append(
                        (
                            current_point,
                            offset,
                            current_point,
                            neighbor_point,
                            1,
                            visited | {current_point},
                        )
                    )
        else:
            for offset in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if (
                    is_valid_point(
                        (neighbor_point := current_point.offset_neighbor(offset)), grid
                    )
                    and neighbor_point != previous_point
                ):
                    stack.append(
                        (
                            source_point,
                            source_outgoing_offset,
                            current_point,
                            neighbor_point,
                            current_distance + 1,
                            visited | {current_point},
                        )
                    )


def max_distance(source: Point, destination: Point, visited: set[Point], point_to_node):
    if source == destination:
        return 0
    result = -float("inf")
    visited.add(source)
    for neighbor, distance in point_to_node[source].neighbors.values():
        if neighbor not in visited:
            result = max(
                result,
                distance + max_distance(neighbor, destination, visited, point_to_node),
            )
    visited.remove(source)
    return result


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example1.txt"))
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
