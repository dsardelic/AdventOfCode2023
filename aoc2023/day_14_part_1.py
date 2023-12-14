from collections import deque


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return tilted_platform_load(
            tuple(list(line) for line in ifile.read().split("\n"))
        )


def tilted_platform_load(platform):
    platform_len = len(platform)

    def tilted_column_load(platform, y):
        falling_rocks_xs = deque(
            (x for x in range(platform_len - 1, -1, -1) if platform[x][y] == "O")
        )
        while falling_rocks_xs:
            x = falling_rocks_xs.pop()
            if x > 0 and platform[x - 1][y] == ".":
                platform[x - 1][y] = "O"
                platform[x][y] = "."
                falling_rocks_xs.appendleft(x - 1)
        return sum(
            platform_len - x for x in range(platform_len) if platform[x][y] == "O"
        )

    return sum(tilted_column_load(platform, y) for y in range(len(platform[0])))


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
