import math
import re


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return sum(gear_ratios(ifile.read().split("\n")))


def gear_ratios(schematic):
    row_len, col_len = len(schematic), len(schematic[0])

    surrounding_fields_offsets = (
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    )

    part_number_per_coordinate = {
        (x, y): int(number_match.group(0))
        for x, row in enumerate(schematic)
        for number_match in re.finditer(r"\d+", row)
        for y in range(*number_match.span())
    }

    return (
        math.prod(surrounding_part_numbers)
        for x, row in enumerate(schematic)
        for y, field in enumerate(row)
        if field == "*"
        and len(
            surrounding_part_numbers := {
                part_number_per_coordinate[(part_x, part_y)]
                for offset in surrounding_fields_offsets
                if -1 < (part_x := x + offset[0]) < row_len
                and -1 < (part_y := y + offset[1]) < col_len
                and part_number_per_coordinate.get((part_x, part_y))
            }
        )
        == 2
    )


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
