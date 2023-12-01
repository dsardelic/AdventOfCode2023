import re

mappings = {
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "0": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return sum(
            int(mappings[digits[0]] + mappings[digits[-1]])
            for line in ifile
            if (
                digits := re.findall(
                    r"(?=(1|2|3|4|5|6|7|8|9|0|"
                    r"one|two|three|four|five|six|seven|eight|nine))",
                    line,
                )
            )
        )


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example1.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
