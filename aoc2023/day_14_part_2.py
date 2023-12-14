from collections import deque

CYCLES_COUNT = 1_000_000_000


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return platform_load(
            spin_platform(tuple(list(line) for line in ifile.read().split("\n")))
        )


def platform_load(platform):
    return sum(
        len(platform) - x
        for x in range(len(platform))
        for y in range(len(platform[0]))
        if platform[x][y] == "O"
    )


def spin_platform(platform):
    tilt_fn_cycle = (tilt_north, tilt_west, tilt_south, tilt_east)
    step_limit = 4 * CYCLES_COUNT
    is_looking_for_cycle = True
    state_to_cycle_lead_steps = {}
    step = 0
    while step < step_limit:
        step += 1
        tilt_fn = tilt_fn_cycle[(step - 1) % 4]
        tilt_fn(platform)
        if is_looking_for_cycle:
            rock_positions = tuple(
                (x, y)
                for x, row in enumerate(platform)
                for y, item in enumerate(row)
                if item == "O"
            )
            if cycle_lead_steps := state_to_cycle_lead_steps.get(
                (tilt_fn, rock_positions)
            ):
                remaining_steps = step_limit - cycle_lead_steps
                cycle_length = step - cycle_lead_steps
                # fast forward to how many steps remain
                step = step_limit - (remaining_steps % cycle_length)
                is_looking_for_cycle = False
            else:
                state_to_cycle_lead_steps[(tilt_fn, rock_positions)] = step
    return platform


def tilt_north(platform):
    row_count = len(platform)
    for y in range(len(platform[0])):
        falling_rocks_xs = deque(
            (x for x in range(row_count - 1, -1, -1) if platform[x][y] == "O")
        )
        while falling_rocks_xs:
            x = falling_rocks_xs.pop()
            if x > 0 and platform[x - 1][y] == ".":
                platform[x - 1][y] = "O"
                platform[x][y] = "."
                falling_rocks_xs.appendleft(x - 1)


def tilt_south(platform):
    row_count = len(platform)
    for y in range(len(platform[0])):
        falling_rocks_xs = deque((x for x in range(row_count) if platform[x][y] == "O"))
        while falling_rocks_xs:
            x = falling_rocks_xs.pop()
            if x < row_count - 1 and platform[x + 1][y] == ".":
                platform[x + 1][y] = "O"
                platform[x][y] = "."
                falling_rocks_xs.appendleft(x + 1)


def tilt_west(platform):
    col_count = len(platform[0])
    for x, row in enumerate(platform):
        falling_rocks_ys = deque(
            (y for y in range(col_count - 1, -1, -1) if row[y] == "O")
        )
        while falling_rocks_ys:
            y = falling_rocks_ys.pop()
            if y > 0 and platform[x][y - 1] == ".":
                platform[x][y - 1] = "O"
                platform[x][y] = "."
                falling_rocks_ys.appendleft(y - 1)


def tilt_east(platform):
    col_count = len(platform[0])
    for x, row in enumerate(platform):
        falling_rocks_ys = deque((y for y in range(col_count) if row[y] == "O"))
        while falling_rocks_ys:
            y = falling_rocks_ys.pop()
            if y < col_count - 1 and platform[x][y + 1] == ".":
                platform[x][y + 1] = "O"
                platform[x][y] = "."
                falling_rocks_ys.appendleft(y + 1)


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
