import math
from collections import defaultdict


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return sum(
            cube_set_power(line) for line in ifile.read().strip("\n").split("\n")
        )


def cube_set_power(game):
    cube_distribution = defaultdict(int)
    for hand in game.split(": ")[1].split("; "):
        for cube_count_and_color in hand.split(", "):
            cube_count, cube_color = cube_count_and_color.split(" ")
            cube_distribution[cube_color] = max(
                cube_distribution[cube_color], int(cube_count)
            )
    return math.prod(cube_distribution.values())


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
