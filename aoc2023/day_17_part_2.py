import dataclasses
import enum
import queue

MINIMUM_STEPS_BEFORE_TURN = 4
MAXIMUM_STEPS_BEFORE_TURN = 10


class Direction(enum.Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def is_valid(self, heat_losses):
        return -1 < self.x < len(heat_losses) and -1 < self.y < len(heat_losses[0])

    def neighbor(self, direction: Direction):
        return Point(self.x + direction.value[0], self.y + direction.value[1])

    def manhattan_distance_from(self, point):
        return abs(self.x - point.x) + abs(self.y - point.y)


@dataclasses.dataclass(frozen=True)
class Node(Point):
    inbound_direction: Direction
    step_count: int

    def equals_point(self, point):
        return isinstance(point, Point) and self.x == point.x and self.y == point.y

    def neighbors(self, heat_losses):
        match (
            self.inbound_direction,
            self.step_count == MAXIMUM_STEPS_BEFORE_TURN,
            self.step_count >= MINIMUM_STEPS_BEFORE_TURN,
        ):
            case Direction.UP, True, _:
                combinations = ((Direction.LEFT, 1), (Direction.RIGHT, 1))
            case Direction.UP, False, True:
                combinations = (
                    (Direction.UP, self.step_count + 1),
                    (Direction.LEFT, 1),
                    (Direction.RIGHT, 1),
                )
            case Direction.UP, False, False:
                combinations = ((Direction.UP, self.step_count + 1),)
            case Direction.DOWN, True, _:
                combinations = ((Direction.LEFT, 1), (Direction.RIGHT, 1))
            case Direction.DOWN, False, True:
                combinations = (
                    (Direction.DOWN, self.step_count + 1),
                    (Direction.LEFT, 1),
                    (Direction.RIGHT, 1),
                )
            case Direction.DOWN, False, False:
                combinations = ((Direction.DOWN, self.step_count + 1),)
            case Direction.LEFT, True, _:
                combinations = ((Direction.UP, 1), (Direction.DOWN, 1))
            case Direction.LEFT, False, True:
                combinations = (
                    (Direction.LEFT, self.step_count + 1),
                    (Direction.UP, 1),
                    (Direction.DOWN, 1),
                )
            case Direction.LEFT, False, False:
                combinations = ((Direction.LEFT, self.step_count + 1),)
            case Direction.RIGHT, True, _:
                combinations = ((Direction.UP, 1), (Direction.DOWN, 1))
            case Direction.RIGHT, False, True:
                combinations = (
                    (Direction.RIGHT, self.step_count + 1),
                    (Direction.UP, 1),
                    (Direction.DOWN, 1),
                )
            case Direction.RIGHT, False, False:
                combinations = ((Direction.RIGHT, self.step_count + 1),)

        return (
            Node(n_point.x, n_point.y, n_direction, n_step_count)
            for n_direction, n_step_count in combinations
            if (n_point := self.neighbor(n_direction)) and n_point.is_valid(heat_losses)
        )


@dataclasses.dataclass(order=True)
class PrioritizedItem:
    priority: int
    heat_loss: int
    node: Node = dataclasses.field(compare=False)


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        heat_losses = tuple(
            heat_losses_row
            for line in ifile
            if (heat_losses_row := tuple(int(x) for x in line.strip("\n")))
        )
    return distance_from_origin(
        heat_losses, Point(len(heat_losses) - 1, len(heat_losses[0]) - 1)
    )


def distance_from_origin(heat_losses, target):
    """Using A* algorithm"""
    p_queue = queue.PriorityQueue()
    p_queue.put(PrioritizedItem(0, 0, Node(0, 0, Direction.RIGHT, 0)))
    p_queue.put(PrioritizedItem(0, 0, Node(0, 0, Direction.DOWN, 0)))
    visited = set()
    while not p_queue.empty():
        p_item = p_queue.get()
        if p_item.node.equals_point(target):
            if p_item.node.step_count >= MINIMUM_STEPS_BEFORE_TURN:
                return p_item.heat_loss
            continue
        for neighbor in p_item.node.neighbors(heat_losses):
            if neighbor in visited:
                continue
            neighbor_heat_loss = p_item.heat_loss + heat_losses[neighbor.x][neighbor.y]
            remaining_heat_loss_heuristic = neighbor.manhattan_distance_from(target)
            p_queue.put(
                PrioritizedItem(
                    neighbor_heat_loss + remaining_heat_loss_heuristic,
                    neighbor_heat_loss,
                    neighbor,
                )
            )
            visited.add(neighbor)
    return None


if __name__ == "__main__":
    print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}_example1.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
