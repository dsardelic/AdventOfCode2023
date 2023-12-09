import itertools


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return sum(
            reduce_sequence(sequence)
            for line in ifile.read().split("\n")
            if (sequence := tuple(int(value) for value in line.split(" ")))
        )


def reduce_sequence(sequence):
    ret = 0
    sequences = [sequence]
    while any(sequence := tuple(y - x for x, y in itertools.pairwise(sequence))):
        sequences.append(sequence)
    for sequence in reversed(  # pylint: disable=redefined-argument-from-local
        sequences
    ):
        ret = sequence[0] - ret
    return ret


if __name__ == "__main__":
    print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    # print(solution(f"input/{__file__[-16:][:6]}.txt"))
