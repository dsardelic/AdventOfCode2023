import enum

SymmetryType = enum.Enum("SymmetryType", "VERTICAL HORIZONTAL")


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return sum(
            score(*symmetry(shape_line_group.split("\n")))
            for shape_line_group in ifile.read().split("\n\n")
        )


def score(symmetry_type, count):
    return count if symmetry_type == SymmetryType.VERTICAL else 100 * count


def symmetry(shape):
    for x in range(1, len(shape)):
        if ret := horizontal_symmetry(x, shape):
            return ret
    for y in range(1, len(shape[0])):
        if ret := vertical_symmetry(y, shape):
            return ret
    return None


def horizontal_symmetry(x, shape):
    x1, x2 = x - 1, x
    while x1 >= 0 and x2 < len(shape):
        if distance_between_rows(x1, x2, shape):
            return None
        x1, x2 = x1 - 1, x2 + 1
    return SymmetryType.HORIZONTAL, x


def vertical_symmetry(y, shape):
    y1, y2 = y - 1, y
    while y1 >= 0 and y2 < len(shape[0]):
        if distance_between_cols(y1, y2, shape):
            return None
        y1, y2 = y1 - 1, y2 + 1
    return SymmetryType.VERTICAL, y


def distance_between_rows(x1, x2, shape):
    return sum(el1 != el2 for el1, el2 in zip(shape[x1], shape[x2]))


def distance_between_cols(y1, y2, shape):
    return sum(shape[x][y1] != shape[x][y2] for x in range(len(shape)))


if __name__ == "__main__":
    print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    # print(solution(f"input/{__file__[-16:][:6]}.txt"))
