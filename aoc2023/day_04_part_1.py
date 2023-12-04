def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return sum(pile_worth(line) for line in ifile)


def pile_worth(line):
    winning_numbers, my_numbers = (
        numbers_str.split(" ")
        for numbers_str in line.strip("\n")
        .replace("  ", " ")
        .split(": ")[1]
        .split(" | ")
    )
    guessed_numbers_count = sum(
        my_number in winning_numbers for my_number in my_numbers
    )
    return 2 ** (guessed_numbers_count - 1) if guessed_numbers_count else 0


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
