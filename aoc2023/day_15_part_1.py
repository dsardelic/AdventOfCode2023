def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return sum(hash_(token) for token in ifile.read().split(","))


def hash_(step):
    s = 0
    for char in step:
        s = (s + ord(char)) * 17 % 256
    return s


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
