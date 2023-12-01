import string


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return sum(
            int(stripped_line[0] + stripped_line[-1])
            for line in ifile
            if (stripped_line := line.strip(string.ascii_lowercase + "\n"))
        )


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
