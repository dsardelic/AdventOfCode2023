import collections
import dataclasses
import itertools

Cube = collections.namedtuple("Cube", ("x", "y", "z"))


@dataclasses.dataclass(frozen=True)
class Brick:
    span_x: range
    span_y: range
    span_z: range

    @property
    def min_height(self):
        return self.span_z.start

    @property
    def max_height(self):
        return self.span_z.stop - 1

    def contains(self, cube: Cube):
        return cube.x in self.span_x and cube.y in self.span_y and cube.z in self.span_z

    def lowest_cubes(self):
        return (
            Cube(x, y, self.span_z.start)
            for x, y in itertools.product(self.span_x, self.span_y)
        )

    def supports(self, brick):
        return any(
            brick.contains(Cube(x, y, self.span_z.stop))
            for x, y in itertools.product(self.span_x, self.span_y)
        )

    def drop_z_by_one(self):
        return Brick(
            self.span_x, self.span_y, range(self.span_z.start - 1, self.span_z.stop - 1)
        )


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        bricks = [
            Brick(*(range(*t) for t in zip(start_cube, stop_cube)))
            for line in ifile
            if (brick_edges := line.strip("\n").split("~"))
            and (start_cube := (int(token) for token in brick_edges[0].split(",")))
            and (stop_cube := (int(token) + 1 for token in brick_edges[1].split(",")))
        ]
    bricks_per_max_height = collections.defaultdict(
        set,
        {
            height: {brick for brick in bricks if brick.max_height == height}
            for height in {brick.max_height for brick in bricks}
        },
    )
    drop_bricks(bricks, bricks_per_max_height)
    supported_bricks_per_brick, supporting_bricks_per_brick = resolve_support_system(
        bricks, bricks_per_max_height
    )
    return len(
        tuple(
            disintegrable_bricks(
                bricks, supported_bricks_per_brick, supporting_bricks_per_brick
            )
        )
    )


def drop_bricks(bricks, bricks_per_max_height):
    bricks_waiting_to_fall = collections.deque(
        [
            (bricks.index(brick), brick)
            for brick in sorted(bricks, key=lambda brick: -brick.min_height)
            if brick.min_height >= 2
        ]
    )
    while bricks_waiting_to_fall:
        brick_index, brick = bricks_waiting_to_fall.pop()
        simulation_brick = brick.drop_z_by_one()
        if not any(
            other_brick.contains(simulation_brick_cube)
            for simulation_brick_cube in simulation_brick.lowest_cubes()
            for other_brick in bricks_per_max_height[simulation_brick.min_height]
        ):
            bricks_per_max_height[brick.max_height].remove(brick)
            bricks[brick_index] = simulation_brick
            bricks_per_max_height[simulation_brick.max_height].add(simulation_brick)
            if simulation_brick.min_height > 1:
                bricks_waiting_to_fall.appendleft((brick_index, simulation_brick))


def resolve_support_system(bricks, bricks_per_max_height):
    bricks_per_min_height = collections.defaultdict(
        set,
        {
            height: {brick for brick in bricks if brick.min_height == height}
            for height in {brick.min_height for brick in bricks}
        },
    )
    supported_bricks_per_brick = collections.defaultdict(set)
    supporting_bricks_per_brick = collections.defaultdict(set)
    for height, supporting_bricks in bricks_per_max_height.items():
        supported_bricks = bricks_per_min_height[height + 1]
        for supporting_brick, supported_brick in itertools.product(
            supporting_bricks, supported_bricks
        ):
            if supporting_brick.supports(supported_brick):
                supported_bricks_per_brick[supporting_brick].add(supported_brick)
                supporting_bricks_per_brick[supported_brick].add(supporting_brick)
    return supported_bricks_per_brick, supporting_bricks_per_brick


def disintegrable_bricks(
    bricks, supported_bricks_per_brick, supporting_bricks_per_brick
):
    return (
        brick
        for brick in bricks
        if not (supported_bricks := supported_bricks_per_brick.get(brick))
        or all(
            len(supporting_bricks_per_brick[supported_brick]) > 1
            for supported_brick in supported_bricks
        )
    )


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
