from collections import defaultdict


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return sum(get_possible_game_ids(ifile.read().strip("\n").split("\n")))


def get_possible_game_ids(games):
    for game in games:
        is_game_possible = True
        game_id_substring, game_hands_substring = game.split(": ")
        game_id = int(game_id_substring.split(" ")[1])
        for hand in game_hands_substring.split("; "):
            cube_distribution = defaultdict(int)
            for cube_count_and_color in hand.split(", "):
                cube_count, cube_color = cube_count_and_color.split(" ")
                cube_distribution[cube_color] = int(cube_count)
            if (
                cube_distribution["red"] > 12
                or cube_distribution["green"] > 13
                or cube_distribution["blue"] > 14
            ):
                is_game_possible = False
                break
        if is_game_possible:
            yield game_id


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
