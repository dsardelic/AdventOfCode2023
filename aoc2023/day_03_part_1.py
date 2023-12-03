import re
import string

symbols = set(string.punctuation) - {"."}


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return sum(part_numbers(ifile.read().split("\n")))


def part_numbers(schematic):
    row_len, col_len = len(schematic), len(schematic[0])

    def is_valid_field(x, y):
        return -1 < x < row_len and -1 < y < col_len

    def no_symbol_on(x, y):
        return not is_valid_field(x, y) or (
            is_valid_field(x, y) and schematic[x][y] not in symbols
        )

    def enclosement_spans(x, y_span):
        y_from, y_to = y_span
        return (
            (x - 1, (y_from - 1, y_to + 1)),
            (x, (y_from - 1, y_from)),
            (x, (y_to, y_to + 1)),
            (x + 1, (y_from - 1, y_to + 1)),
        )

    return (
        int(number_match.group(0))
        for x, row in enumerate(schematic)
        for number_match in re.finditer(r"\d+", row)
        if not all(
            no_symbol_on(x, y)
            for x, y_span in enclosement_spans(x, number_match.span())
            for y in range(*y_span)
        )
    )


if __name__ == "__main__":
    print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    # print(solution(f"input/{__file__[-16:][:6]}.txt"))
