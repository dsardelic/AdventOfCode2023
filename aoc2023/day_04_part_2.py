def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return final_card_count(ifile.readlines())


def final_card_count(lines):
    card_counts = [1] * len(lines)
    for card_no, line in enumerate(lines, 1):
        winning_numbers, my_numbers = (
            numbers_str.split(" ")
            for numbers_str in line.strip("\n")
            .replace("  ", " ")
            .split(": ")[1]
            .split(" | ")
        )
        for i in range(sum(my_number in winning_numbers for my_number in my_numbers)):
            card_counts[card_no + i] += card_counts[card_no - 1]
    return sum(card_counts)


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
